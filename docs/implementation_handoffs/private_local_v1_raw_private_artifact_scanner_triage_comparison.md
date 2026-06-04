# Private Local V1 Raw/Private Artifact Scanner Triage Comparison

## Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/262
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/136
- Source issues:
  - https://github.com/Tahjali11/Mythic-Edge/issues/252
  - https://github.com/Tahjali11/Mythic-Edge/issues/260

## Contract

`docs/contracts/private_local_v1_raw_private_artifact_scanner_triage.md`

## Internal Project Area

Quality / Governance, with Generated / Local Artifacts as the supporting area.

## Truth Owner

The repo secret/private-marker scanner owns deterministic repository
content-safety classification and redacted scanner reporting. This handoff owns
only the #262 selected raw/private artifact triage classification and follow-up
routing.

It does not own parser truth, analytics truth, workbook truth, webhook truth,
Apps Script truth, runtime status truth, fixture provenance truth, credential
policy, merge readiness, deploy readiness, issue closure, tracker completion,
or AI/model-provider truth.

## Bridge-Code Status

`shared_support`

## Role Performed

Codex C: Module Implementer / comparison thread.

## Branch And Git Status

- Branch: `codex/analytics-foundation`
- Starting status: one untracked #262 contract artifact,
  `docs/contracts/private_local_v1_raw_private_artifact_scanner_triage.md`
- No unrelated dirty tracked files were observed before editing.

## Files Inspected

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/contracts/private_local_v1_raw_private_artifact_scanner_triage.md`
- `docs/contracts/private_local_v1_high_risk_scanner_findings_triage.md`
- `docs/implementation_handoffs/private_local_v1_high_risk_scanner_findings_triage_comparison.md`
- `docs/contract_test_reports/private_local_v1_high_risk_scanner_findings_triage.md`
- `docs/contracts/private_local_v1_private_artifact_scanner_env_ignore_posture.md`
- `docs/contract_test_reports/private_local_v1_private_artifact_scanner_env_ignore_posture.md`
- `docs/local_artifacts_manifest.json`
- `docs/contracts/engineering_maturity_index_open_framework.md`
- `docs/contract_test_reports/engineering_maturity_baseline.md`
- `tools/check_secret_patterns.py`
- `tools/check_local_environment.py`
- `tools/check_protected_surfaces.py`
- `tools/select_validation.py`
- `tests/test_check_secret_patterns.py`
- `tests/test_check_local_environment.py`
- `tests/test_check_protected_surfaces.py`
- GitHub issue #262, tracker #136, source issues #252 and #260, and PRs #259
  and #261
- Selected scanner findings through structured category/path/line inventory,
  without copying raw matched values or raw excerpts into this report

## Current Behavior Compared To Contract

The contract asks #262 to classify the next raw/private all-repo scanner tranche
after the #252 env-ignore posture work and the #260 credential/webhook/workbook
marker tranche.

Current behavior matches the contract baseline:

| Scanner mode | Result |
| --- | --- |
| all-repo advisory | non-clean, exit code 0 |
| changed-path scanner against `origin/codex/analytics-foundation` | clean |
| path-scoped strictness | preserved |

The selected #262 tranche remains present:

| Category | Forbidden | Warnings |
| --- | ---: | ---: |
| `raw_player_log_content` | 335 | 0 |
| `runtime_status_payload` | 85 | 0 |
| `generated_data_dump` | 38 | 0 |
| transport-failure artifact category | 9 | 0 |
| `private_local_path` | 57 | 0 |

The warning-only categories listed in the contract remain out of scope except
as background context.

## Implementation Option Chosen

Report-only triage and routing.

Reason: the selected tranche spans parser tests, parser/evidence source,
diagnostics/status code, generated-data support code, tool docs, examples,
historical workflow reports, and Apps Script-adjacent tooling. A broad rewrite
would risk changing parser coverage, diagnostics semantics, path handling, or
historical governance artifacts. The smallest contract-aligned Codex C action
is to classify the families, preserve scanner behavior, and route concrete
remediation into focused follow-up work.

## Files Changed

- Added
  `docs/implementation_handoffs/private_local_v1_raw_private_artifact_scanner_triage_comparison.md`

The untracked Codex B contract artifact was preserved and not edited:

- `docs/contracts/private_local_v1_raw_private_artifact_scanner_triage.md`

## Exact Sections Changed

This report adds:

- issue, tracker, source issue, contract, and role metadata
- files inspected
- current scanner behavior compared to contract
- implementation option chosen
- selected raw/private all-repo scanner summary
- category/path-family classification matrix
- concrete fix candidates and deferrals
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
scanned_paths: 753
skipped_paths: 0
forbidden: 540
warnings: 901
```

Selected #262 findings:

```text
selected_total: 524
```

## Selected Counts By Category And Severity

| Category | Severity | Count |
| --- | --- | ---: |
| `raw_player_log_content` | forbidden | 335 |
| `runtime_status_payload` | forbidden | 85 |
| `generated_data_dump` | forbidden | 38 |
| transport-failure artifact category | forbidden | 9 |
| `private_local_path` | forbidden | 57 |

## Selected Counts By Path Family

| Category | Path family | Count |
| --- | --- | ---: |
| `raw_player_log_content` | `tests/` | 229 |
| `raw_player_log_content` | `src/mythic_edge_parser/app/` | 92 |
| `raw_player_log_content` | `src/mythic_edge_parser/parsers/` | 8 |
| `raw_player_log_content` | `docs/problem_representations/` | 5 |
| `raw_player_log_content` | `src/mythic_edge_parser/log/` | 1 |
| `runtime_status_payload` | `tests/` | 46 |
| `runtime_status_payload` | `src/mythic_edge_parser/app/` | 32 |
| `runtime_status_payload` | `tests/fixtures/` | 3 |
| `runtime_status_payload` | `tools/auto_launcher/` | 2 |
| `runtime_status_payload` | `tools/google_apps_script/` | 2 |
| `generated_data_dump` | `tests/` | 18 |
| `generated_data_dump` | `src/mythic_edge_parser/app/` | 14 |
| `generated_data_dump` | `tools/scryfall_parser/` | 3 |
| `generated_data_dump` | `tools/auto_launcher/` | 2 |
| `generated_data_dump` | `docs/` | 1 |
| transport-failure artifact category | `src/mythic_edge_parser/app/` | 6 |
| transport-failure artifact category | `docs/problem_representations/` | 1 |
| transport-failure artifact category | `tools/auto_launcher/` | 1 |
| transport-failure artifact category | `tools/check_protected_surfaces.py/` | 1 |
| `private_local_path` | `docs/contract_test_reports/` | 15 |
| `private_local_path` | `docs/implementation_handoffs/` | 14 |
| `private_local_path` | `docs/contracts/` | 7 |
| `private_local_path` | `tests/` | 8 |
| `private_local_path` | `src/mythic_edge_parser/app/` | 6 |
| `private_local_path` | `examples/` | 4 |
| `private_local_path` | `src/mythic_edge_parser/sanitize.py/` | 2 |
| `private_local_path` | `tools/auto_launcher/` | 1 |

## Classification Matrix

| Category | Path family | Count | Classification | Resolution |
| --- | --- | ---: | --- | --- |
| `raw_player_log_content` | `tests/` | 229 | `expected_synthetic_or_sanitized_fixture` | Parser regression tests intentionally exercise log-like marker shapes. No rewrite in #262; broad fixture-builder cleanup should be a follow-up if desired. |
| `raw_player_log_content` | `src/mythic_edge_parser/app/` | 92 | `defer_with_reason` | Evidence/provenance source contains parser-adjacent marker vocabulary. Editing could affect evidence semantics or parser support. Route through a focused evidence-ledger/parser fixture contract. |
| `raw_player_log_content` | `src/mythic_edge_parser/parsers/` | 8 | `scanner_false_positive` | Parser marker constants are source vocabulary, not committed private artifacts. Rewriting would reduce parser clarity and risk behavior drift. |
| `raw_player_log_content` | `src/mythic_edge_parser/log/` | 1 | `scanner_false_positive` | Log parsing support vocabulary is source behavior, not private artifact content. No edit in #262. |
| `raw_player_log_content` | `docs/problem_representations/` | 5 | `expected_policy_or_contract_text` | Historical problem-representation text discusses Player.log evidence boundaries. No raw content is copied here. |
| `runtime_status_payload` | `tests/` | 46 | `expected_synthetic_or_sanitized_fixture` | Tests exercise diagnostics/status/report shape behavior. No rewrite in #262. |
| `runtime_status_payload` | `tests/fixtures/` | 3 | `expected_synthetic_or_sanitized_fixture` | Schema snapshot fixture family is expected evidence validation support. No rewrite in #262. |
| `runtime_status_payload` | `src/mythic_edge_parser/app/` | 32 | `scanner_false_positive` | Source contains status field names, schema shape, and diagnostics support, not committed runtime payload files. No edit in #262. |
| `runtime_status_payload` | `tools/auto_launcher/` | 2 | `scanner_false_positive` | Local launcher/status helper source references status shape. No runtime behavior edit in #262. |
| `runtime_status_payload` | `tools/google_apps_script/` | 2 | `defer_with_reason` | Apps Script-adjacent status references require a protected-surface contract before edits. |
| `generated_data_dump` | `tests/` | 18 | `expected_synthetic_or_sanitized_fixture` | Card catalog and generated-data support tests intentionally exercise generated-data field shapes. No rewrite in #262. |
| `generated_data_dump` | `src/mythic_edge_parser/app/` | 14 | `scanner_false_positive` | Source contains card catalog, refresh, and support-data vocabulary, not committed generated dump files. No edit in #262. |
| `generated_data_dump` | `tools/scryfall_parser/` | 3 | `expected_placeholder_or_example` | Tooling documentation/example surface. No generated data dump is added by this pass. |
| `generated_data_dump` | `tools/auto_launcher/` | 2 | `scanner_false_positive` | Launcher source references generated support-data status. No edit in #262. |
| `generated_data_dump` | `docs/` | 1 | `expected_policy_or_contract_text` | Documentation discusses generated-data boundaries. No edit in #262. |
| transport-failure artifact category | `src/mythic_edge_parser/app/` | 6 | `scanner_false_positive` | Diagnostics/source field references are not committed transport artifacts. No webhook or diagnostics behavior edit in #262. |
| transport-failure artifact category | `docs/problem_representations/` | 1 | `expected_policy_or_contract_text` | Historical problem text discusses transport-failure artifact boundaries. |
| transport-failure artifact category | `tools/auto_launcher/` | 1 | `scanner_false_positive` | Tool source references local runtime/transport support, not a committed transport artifact. |
| transport-failure artifact category | `tools/check_protected_surfaces.py/` | 1 | `expected_policy_or_contract_text` | Protected-surface tooling needs to name the protected artifact family it detects. |
| `private_local_path` | `docs/contract_test_reports/` | 15 | `defer_with_reason` | Historical reports may contain path examples or prior evidence. Normalize under a dedicated docs cleanup contract if release-readiness requires count reduction. |
| `private_local_path` | `docs/implementation_handoffs/` | 14 | `defer_with_reason` | Historical handoffs may contain path examples or prior evidence. Normalize under a dedicated docs cleanup contract if release-readiness requires count reduction. |
| `private_local_path` | `docs/contracts/` | 7 | `expected_policy_or_contract_text` | Contracts discuss local path boundaries and must not be silently weakened. |
| `private_local_path` | `tests/` | 8 | `expected_synthetic_or_sanitized_fixture` | Sanitizer, runner, and status tests intentionally exercise local-path redaction behavior. |
| `private_local_path` | `src/mythic_edge_parser/app/` | 6 | `scanner_false_positive` | Source path-handling code and diagnostics references are not private local artifact contents. No edit in #262. |
| `private_local_path` | `src/mythic_edge_parser/sanitize.py/` | 2 | `scanner_false_positive` | Sanitizer implementation must describe path-redaction patterns. No edit in #262. |
| `private_local_path` | `examples/` | 4 | `defer_with_reason` | Example local-path text should be reviewed under a focused example/docs cleanup pass before release-readiness claims. |
| `private_local_path` | `tools/auto_launcher/` | 1 | `scanner_false_positive` | Launcher path-handling source is not private local artifact content. No edit in #262. |

## Concrete Fix Candidates

No concrete file edit was made in this report-only pass.

Potential future fixes:

1. Create a focused parser-test fixture-builder issue for raw-looking inline
   parser test snippets if the project wants to reduce all-repo advisory debt
   without weakening parser coverage.
2. Create a focused evidence-ledger/source vocabulary issue for parser-adjacent
   marker strings in evidence/provenance modules, if reviewers want those
   separated from raw-looking source constants.
3. Create a docs cleanup issue to normalize historical report/handoff local
   path examples to symbolic placeholders.
4. Create a protected-surface issue before editing Apps Script-adjacent status
   references.

## Path-Scoped Scanner Strictness Status

Preserved. No scanner rules, scanner exit semantics, allowlists, downgrades,
or path-scoped strictness behavior changed.

## All-Repo Advisory Status

Preserved. The all-repo scanner remains advisory and non-clean. This pass does
not claim all-repo cleanliness or private-local-v1 private artifact readiness.

## Validation Run

```powershell
git status --short --branch --untracked-files=all
# passed; branch codex/analytics-foundation with two untracked #262 docs artifacts

py tools\check_secret_patterns.py --all
# advisory result remained non-clean as expected: forbidden 540, warnings 901, exit code 0

py tools\check_secret_patterns.py --base origin/codex/analytics-foundation
# passed; scanned_paths 0, forbidden 0, warnings 0

py -m pytest -q tests\test_check_secret_patterns.py tests\test_check_local_environment.py tests\test_check_protected_surfaces.py
# passed; 97 passed, 1 skipped

git diff --check
# passed

py tools\check_agent_docs.py
# passed; errors 0, warnings 0

py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation
# passed; changed_paths 0, forbidden 0, warnings 0

@'
docs/contracts/private_local_v1_raw_private_artifact_scanner_triage.md
docs/implementation_handoffs/private_local_v1_raw_private_artifact_scanner_triage_comparison.md
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
# passed; scanned_paths 2, forbidden 0, warnings 0

@'
docs/contracts/private_local_v1_raw_private_artifact_scanner_triage.md
docs/implementation_handoffs/private_local_v1_raw_private_artifact_scanner_triage_comparison.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
# passed; changed_paths 2, forbidden 0, warnings 0

direct whitespace/ascii/final-newline check over the #262 docs
# passed
```

## Protected-Surface Status

Passed for the #262 docs paths and base-diff scan. No protected runtime,
parser, analytics, workbook, webhook, Apps Script, Sheets, OpenAI, AI, or
production behavior changed.

## Secret/Private-Marker Status

Passed for the #262 docs paths. No raw secret values, raw log-like lines,
runtime payloads, transport-failure payloads, generated data contents, private
local paths, private JSONL payloads, SQLite contents, workbook exports,
endpoint values, workbook identifiers, credential values, environment values,
or local-only artifacts were added to this report.

## Generated/Private Artifact Status

No generated or private artifacts were intentionally created, copied,
sanitized, imported, moved, deleted, inspected, or committed by this
report-only pass.

## What Remains Unverified

- Codex E independent contract-test review.
- Whether any historical report/handoff path examples should be normalized now
  or left as archived workflow evidence.
- Whether broad parser tests should be rewritten with fixture builders or kept
  as accepted synthetic regression coverage.
- Whether evidence-ledger source marker vocabulary needs a separate
  scanner-aware fixture/provenance cleanup.
- Whether Apps Script-adjacent status references need protected-surface
  cleanup.
- Full all-repo scanner cleanup.
- #252 private-local-v1 private artifact readiness.
- #260 lifecycle reconciliation.
- Tracker #136 completion.

## Forbidden Scope

Forbidden scope was not intentionally touched:

- no parser behavior changed
- no parser state final reconciliation changed
- no parser event classes changed
- no match/game identity or deduplication changed
- no diagnostics/status API behavior changed
- no analytics schema or migrations changed
- no workbook schema changed
- no webhook payload shape changed
- no Apps Script behavior changed
- no Google Sheets behavior changed
- no local app runtime behavior changed
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

Act as Codex E: Module Reviewer / contract-test thread for issue #262.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/262

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/136

Source issues:
- https://github.com/Tahjali11/Mythic-Edge/issues/252
- https://github.com/Tahjali11/Mythic-Edge/issues/260

Branch:
codex/analytics-foundation

Contract:
docs/contracts/private_local_v1_raw_private_artifact_scanner_triage.md

Implementation handoff:
docs/implementation_handoffs/private_local_v1_raw_private_artifact_scanner_triage_comparison.md

Expected review artifact:
docs/contract_test_reports/private_local_v1_raw_private_artifact_scanner_triage.md

Goal:
Review the Codex C #262 raw/private artifact scanner triage against the contract. Verify selected category counts, path-family classifications, raw-value redaction, path-scoped scanner strictness, all-repo advisory/no-gate posture, and explicit follow-up routing.

Review focus:
- Check classification of the selected raw/private artifact scanner families.
- Confirm no raw matched values, raw log-like lines, runtime payloads, transport-failure payloads, generated data contents, private local paths, private JSONL payloads, SQLite contents, workbook exports, endpoints, workbook identifiers, credentials, or environment values were copied into docs or reports.
- Decide whether report-only classification is sufficient for this #262 pass or whether Codex D should rewrite selected synthetic tests/docs.
- Pay special attention to historical docs path examples, evidence-ledger source marker vocabulary, and Apps Script-adjacent status references.
- Confirm no scanner coverage was weakened and no path-scoped scanner strictness was relaxed.
- Confirm #252 private-local-v1 readiness, #260 lifecycle completion, and tracker #136 completion are not claimed.

Validation:
- git status --short --branch --untracked-files=all
- py tools\check_secret_patterns.py --all
- py tools\check_secret_patterns.py --base origin/codex/analytics-foundation
- py -m pytest -q tests\test_check_secret_patterns.py tests\test_check_local_environment.py tests\test_check_protected_surfaces.py
- git diff --check
- py tools\check_agent_docs.py
- py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation
- path-scoped protected-surface and secret/private-marker scans over the #262 contract and handoff files

Do not:
- print or copy raw matched values, raw log-like lines, runtime payloads, transport-failure payloads, generated data contents, private local paths, private JSONL payloads, SQLite contents, workbook exports, endpoints, workbook identifiers, credentials, environment values, or local-only artifacts;
- weaken scanner coverage;
- suppress findings without explicit policy rationale and tests;
- handle warning-only categories except as context;
- make all-repo scanner a failing gate;
- add CI gates;
- change parser/runtime/analytics/local app/workbook/webhook/App Script/Sheets/OpenAI/AI/production behavior;
- change credential policy or environment-variable contracts;
- target main;
- stage, commit, push, open a PR, merge, close #262, close #252, close #260, or mark tracker #136 complete unless explicitly asked.

Final review output must include:
- role performed;
- issue/tracker/source issues;
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
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/262"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/136"
  source_issues:
    - "https://github.com/Tahjali11/Mythic-Edge/issues/252"
    - "https://github.com/Tahjali11/Mythic-Edge/issues/260"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/private_local_v1_raw_private_artifact_scanner_triage.md"
  target_artifact: "docs/implementation_handoffs/private_local_v1_raw_private_artifact_scanner_triage_comparison.md"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  validation:
    - "git status --short --branch --untracked-files=all -> two untracked #262 docs artifacts"
    - "py tools/check_secret_patterns.py --all -> advisory non-clean, forbidden 540, warnings 901, exit code 0"
    - "py tools/check_secret_patterns.py --base origin/codex/analytics-foundation -> passed"
    - "py -m pytest -q tests/test_check_secret_patterns.py tests/test_check_local_environment.py tests/test_check_protected_surfaces.py -> 97 passed, 1 skipped"
    - "git diff --check -> passed"
    - "py tools/check_agent_docs.py -> passed"
    - "py tools/check_protected_surfaces.py --base origin/codex/analytics-foundation -> passed"
    - "path-scoped secret/private-marker scan over #262 docs -> passed"
    - "path-scoped protected-surface scan over #262 docs -> passed"
    - "direct whitespace/ascii/final-newline check over #262 docs -> passed"
  stop_conditions:
    - "Do not print or copy raw matched values or private artifacts."
    - "Do not weaken scanner coverage or suppress findings without explicit policy rationale and tests."
    - "Do not handle warning-only categories except as context."
    - "Do not make all-repo scanner a failing gate or add CI gates."
    - "Do not change parser/runtime/analytics/local app/workbook/webhook/App Script/Sheets/OpenAI/AI/production behavior."
    - "Do not change credential policy or environment-variable contracts."
    - "Do not target main, close #252, close #260, or close tracker #136."
```
