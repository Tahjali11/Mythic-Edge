# Private Local V1 Artifact-Path And Ambiguous-Marker Warning Triage Comparison

## Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/264
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/136
- Source issues:
  - https://github.com/Tahjali11/Mythic-Edge/issues/252
  - https://github.com/Tahjali11/Mythic-Edge/issues/260
  - https://github.com/Tahjali11/Mythic-Edge/issues/262

## Contract

`docs/contracts/private_local_v1_artifact_path_ambiguous_marker_warning_triage.md`

## Internal Project Area

Quality / Governance, with Generated / Local Artifacts as the supporting area.

## Truth Owner

The repo secret/private-marker scanner owns deterministic repository
content-safety classification and redacted scanner reporting. This handoff owns
only the #264 selected warning-family classification and follow-up routing.

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
- Starting status: one untracked #264 contract artifact,
  `docs/contracts/private_local_v1_artifact_path_ambiguous_marker_warning_triage.md`
- No unrelated dirty tracked files were observed before editing.

## Files Inspected

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/contracts/private_local_v1_artifact_path_ambiguous_marker_warning_triage.md`
- `docs/contracts/private_local_v1_private_artifact_scanner_env_ignore_posture.md`
- `docs/contracts/private_local_v1_high_risk_scanner_findings_triage.md`
- `docs/implementation_handoffs/private_local_v1_high_risk_scanner_findings_triage_comparison.md`
- `docs/contract_test_reports/private_local_v1_high_risk_scanner_findings_triage.md`
- `docs/contracts/private_local_v1_raw_private_artifact_scanner_triage.md`
- `docs/implementation_handoffs/private_local_v1_raw_private_artifact_scanner_triage_comparison.md`
- `docs/contract_test_reports/private_local_v1_raw_private_artifact_scanner_triage.md`
- `docs/contracts/repo_wide_secret_private_marker_scanner.md`
- `docs/local_artifacts_manifest.json`
- `tools/check_secret_patterns.py`
- `tools/check_local_environment.py`
- `tools/check_protected_surfaces.py`
- `tools/select_validation.py`
- `tests/test_check_secret_patterns.py`
- `tests/test_check_local_environment.py`
- `tests/test_check_protected_surfaces.py`
- GitHub issue #264, tracker #136, source issues #252, #260, and #262
- Selected scanner findings through structured category/path inventory,
  without copying raw matched values or raw excerpts into this report

## Current Behavior Compared To Contract

The contract asks #264 to classify warning-only all-repo scanner debt after the
#252 env-ignore posture work, the #260 high-risk scanner triage package, and
the #262 raw/private artifact scanner triage package.

Current behavior matches the contract baseline:

| Scanner mode | Result |
| --- | --- |
| all-repo advisory | non-clean, exit code 0 |
| changed-path scanner against `origin/codex/analytics-foundation` | clean |
| path-scoped scanner strictness | preserved |

The selected #264 tranche remains present and warning-only:

| Category | Severity | Count |
| --- | --- | ---: |
| `artifact_path_reference` | warning | 635 |
| `ambiguous_private_marker` | warning | 80 |

Deferred warning categories remain out of scope except as context:

- `sanitized_fixture_marker`
- `placeholder_secret_reference`
- `decode_replacement_used`

## Implementation Option Chosen

Report-only triage and routing.

Reason: the selected warning families span governance contracts, historical
handoffs, contract-test reports, synthetic tests, fixtures, scanner source,
policy docs, and one source path-handling reference. Broad rewrites would risk
erasing useful workflow evidence, weakening redaction coverage, or changing
parser-adjacent vocabulary to reduce advisory counts. The smallest
contract-aligned Codex C action is to classify the warning families, preserve
scanner behavior, and route any real cleanup into focused follow-up work.

## Files Changed

- Added
  `docs/implementation_handoffs/private_local_v1_artifact_path_ambiguous_marker_warning_triage_comparison.md`

The untracked Codex B contract artifact was preserved and not edited:

- `docs/contracts/private_local_v1_artifact_path_ambiguous_marker_warning_triage.md`

## Exact Sections Changed

This report adds:

- issue, tracker, source issue, contract, and role metadata
- files inspected
- current scanner behavior compared to contract
- implementation option chosen
- selected warning-family scanner summary
- category/path-family classification matrix
- concrete cleanup candidates and deferrals
- validation results
- protected-surface, secret/private-marker, and generated artifact status
- Codex E prompt and workflow handoff block

## Code/Test/Doc Status

- Code changed: no
- Tests changed: no
- Docs changed: yes
- Report-only: yes
- Scanner-policy-only: no

## All-Repo Scanner Warning Summary

Refreshed summary during this pass:

```text
mode: all-repo-advisory
result: failed
exit_code: 0
scanned_paths: 756
skipped_paths: 0
forbidden: 540
warnings: 901
```

Selected #264 warnings:

```text
selected_total: 715
```

## Selected Counts By Category And Severity

| Category | Severity | Count |
| --- | --- | ---: |
| `ambiguous_private_marker` | warning | 80 |
| `artifact_path_reference` | warning | 635 |

## Selected Counts By Path Family

| Category | Path family | Count |
| --- | --- | ---: |
| `ambiguous_private_marker` | `docs/contracts/` | 73 |
| `ambiguous_private_marker` | `docs/implementation_handoffs/` | 4 |
| `ambiguous_private_marker` | `tests/` | 2 |
| `ambiguous_private_marker` | `docs/contract_test_reports/` | 1 |
| `artifact_path_reference` | `docs/contracts/` | 221 |
| `artifact_path_reference` | `docs/implementation_handoffs/` | 182 |
| `artifact_path_reference` | `docs/contract_test_reports/` | 172 |
| `artifact_path_reference` | `tests/` | 42 |
| `artifact_path_reference` | `docs/` | 8 |
| `artifact_path_reference` | `tools/check_secret_patterns.py` | 5 |
| `artifact_path_reference` | `tests/fixtures/` | 4 |
| `artifact_path_reference` | `src/mythic_edge_parser/app/` | 1 |

## Highest-Count Selected Paths

These are repo-relative paths and counts only. No raw matched value or raw line
excerpt is recorded here.

| Category | Count | Path |
| --- | ---: | --- |
| `artifact_path_reference` | 24 | `docs/contracts/player_log_evidence_ledger_runtime_status_exposure.md` |
| `artifact_path_reference` | 18 | `docs/contract_test_reports/player_log_evidence_ledger_schema_snapshot_builder.md` |
| `ambiguous_private_marker` | 10 | `docs/contracts/parser_gre_game_state.md` |
| `artifact_path_reference` | 9 | `docs/contract_test_reports/code_hardening_golden_fixture_policy.md` |
| `ambiguous_private_marker` | 9 | `docs/contracts/parser_gre_connect_resp.md` |
| `artifact_path_reference` | 8 | `docs/contract_test_reports/player_log_evidence_ledger_runtime_status_exposure.md` |
| `artifact_path_reference` | 8 | `docs/contracts/parser_diagnostics_mode.md` |
| `artifact_path_reference` | 8 | `tests/test_runtime_field_evidence.py` |
| `ambiguous_private_marker` | 7 | `docs/contracts/player_log_evidence_ledger_tier3_mulligans.md` |
| `ambiguous_private_marker` | 7 | `docs/contracts/player_log_evidence_ledger_tier3_play_draw.md` |

## Classification Matrix

| Category | Path family | Count | Classification | Resolution |
| --- | --- | ---: | --- | --- |
| `artifact_path_reference` | `docs/contracts/` | 221 | `expected_policy_or_contract_text` | Contracts intentionally describe local artifact boundaries, parser evidence boundaries, diagnostics, generated-data posture, workbook/export boundaries, and scanner behavior. Keep as policy evidence unless a focused contract rewrite is opened. |
| `artifact_path_reference` | `docs/implementation_handoffs/` | 182 | `expected_handoff_or_review_text` | Handoffs preserve prior validation commands, scanner summaries, and lifecycle context. Bulk normalization should be a docs-cleanup follow-up, not a #264 behavior edit. |
| `artifact_path_reference` | `docs/contract_test_reports/` | 172 | `expected_handoff_or_review_text` | Review reports preserve contract-test evidence and prior scanner summaries. Keep visible as workflow history unless release-readiness requires a dedicated cleanup pass. |
| `artifact_path_reference` | `tests/` | 42 | `expected_synthetic_or_sanitized_fixture` | Tests intentionally exercise redaction, status, protected-surface, and scanner behavior using synthetic or sanitized marker shapes. No test rewrite in this report-only pass. |
| `artifact_path_reference` | `docs/` | 8 | `expected_policy_or_contract_text` | General docs include local artifact manifest or governance context. These references are policy/manifest evidence, not committed private artifact contents. |
| `artifact_path_reference` | `tools/check_secret_patterns.py` | 5 | `scanner_false_positive` | Scanner implementation must name rule categories and redaction behavior. Rewriting would reduce clarity without reducing real private artifact risk. |
| `artifact_path_reference` | `tests/fixtures/` | 4 | `expected_synthetic_or_sanitized_fixture` | Fixture metadata intentionally records safe fixture boundaries. No raw private artifact is introduced by this pass. |
| `artifact_path_reference` | `src/mythic_edge_parser/app/` | 1 | `scanner_false_positive` | The lone source warning is path-handling vocabulary in application source, not private artifact content. No source edit in #264. |
| `ambiguous_private_marker` | `docs/contracts/` | 73 | `expected_policy_or_contract_text` | Parser and Player.log evidence contracts intentionally discuss log/evidence vocabulary and private-artifact boundaries. Preserve wording unless a future contract rewrites examples. |
| `ambiguous_private_marker` | `docs/implementation_handoffs/` | 4 | `expected_handoff_or_review_text` | Handoffs preserve prior workflow and validation context. No raw matched value is copied here. |
| `ambiguous_private_marker` | `tests/` | 2 | `expected_synthetic_or_sanitized_fixture` | Router tests use synthetic marker-like values to exercise parsing/routing behavior. No parser or test behavior changed. |
| `ambiguous_private_marker` | `docs/contract_test_reports/` | 1 | `expected_handoff_or_review_text` | Review report text is historical workflow evidence and remains warning-only. |

## Concrete Cleanup Candidates

No concrete file edit was made in this report-only pass.

Potential future fixes:

1. Create a focused docs/governance cleanup issue if historical handoffs and
   reports should be normalized before a private-local-v1 readiness claim.
2. Create a focused scanner-source/readability issue only if reviewers want
   rule category naming moved out of warning-sensitive contexts.
3. Create a focused test-fixture cleanup issue if synthetic marker strings
   should be generated through builders rather than inline test text.
4. Create a focused parser/evidence contract issue if ambiguous Player.log
   vocabulary should be converted into symbolic fixture references.
5. Route any protected-surface or runtime-adjacent cleanup back through Codex
   A/B before implementation.

## Path-Scoped Scanner Strictness Status

Preserved. No scanner rules, scanner exit semantics, allowlists, downgrades,
category semantics, or path-scoped strictness behavior changed.

## All-Repo Advisory Status

Preserved. The all-repo scanner remains advisory and non-clean. This pass does
not claim all-repo cleanliness or private-local-v1 private artifact readiness.

## Validation Run

```powershell
git status --short --branch --untracked-files=all
# passed; branch codex/analytics-foundation with two untracked #264 docs artifacts

py tools\check_secret_patterns.py --all
# advisory result remained non-clean as expected:
# scanned_paths 756, forbidden 540, warnings 901, process exit code 0

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

path-scoped secret/private-marker scan over the #264 contract and handoff
# passed; scanned_paths 2, forbidden 0, warnings 0

path-scoped protected-surface scan over the #264 contract and handoff
# passed; changed_paths 2, forbidden 0, warnings 0

direct whitespace/ascii/final-newline check over the #264 docs
# passed
```

## Protected-Surface Status

Passed for the #264 docs paths and base-diff scan. No protected runtime,
parser, analytics, workbook, webhook, Apps Script, Sheets, OpenAI, AI, or
production behavior was changed.

## Secret/Private-Marker Status

Passed for the #264 docs paths.

No raw matched values, raw private paths, raw log-like lines, runtime payloads,
transport-failure payloads, generated data contents, private JSONL payloads,
SQLite contents, workbook exports, endpoint values, workbook identifiers,
credential values, environment values, or local-only artifact contents were
added to this report.

## Generated/Private Artifact Status

No generated or private artifacts were intentionally created, copied,
sanitized, imported, moved, deleted, inspected, or committed by this
report-only pass.

## What Remains Unverified

- Codex E independent contract-test review.
- Whether historical reports and handoffs should be normalized now or left as
  durable workflow evidence.
- Whether synthetic test marker strings should be converted to helper builders.
- Whether parser/evidence contract vocabulary should be rewritten to reduce
  warning volume.
- Whether all-repo warning counts should eventually have a baseline,
  allowlist, or release-readiness threshold.
- Full all-repo scanner cleanup.
- #252 private-local-v1 private artifact readiness.
- #260 and #262 lifecycle reconciliation.
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

Act as Codex E: Module Reviewer / contract-test thread for issue #264.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/264

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/136

Source issues:
- https://github.com/Tahjali11/Mythic-Edge/issues/252
- https://github.com/Tahjali11/Mythic-Edge/issues/260
- https://github.com/Tahjali11/Mythic-Edge/issues/262

Branch:
codex/analytics-foundation

Contract:
docs/contracts/private_local_v1_artifact_path_ambiguous_marker_warning_triage.md

Implementation handoff:
docs/implementation_handoffs/private_local_v1_artifact_path_ambiguous_marker_warning_triage_comparison.md

Expected review artifact:
docs/contract_test_reports/private_local_v1_artifact_path_ambiguous_marker_warning_triage.md

Goal:
Review the Codex C #264 artifact-path and ambiguous-marker warning triage against the contract. Verify selected warning counts, path-family classifications, raw-value redaction, path-scoped scanner strictness, all-repo advisory/no-gate posture, and explicit follow-up routing.

Review focus:
- Check classification of artifact_path_reference and ambiguous_private_marker warning families.
- Confirm no raw matched values, raw private paths, raw log-like lines, runtime payloads, transport-failure payloads, generated data contents, private JSONL payloads, SQLite contents, workbook exports, endpoints, workbook identifiers, credentials, environment values, or local-only artifact contents were copied into docs or reports.
- Decide whether report-only classification is sufficient for this #264 pass or whether Codex D should rewrite selected docs/tests.
- Pay special attention to historical handoff/report families, parser/evidence contract vocabulary, synthetic tests, scanner source, and the lone source path-handling reference.
- Confirm no scanner coverage was weakened and no path-scoped scanner strictness was relaxed.
- Confirm all-repo scanner remains advisory and non-clean.
- Confirm #252 private-local-v1 readiness, #260 lifecycle completion, #262 lifecycle completion, and tracker #136 completion are not claimed.

Validation:
- git status --short --branch --untracked-files=all
- py tools\check_secret_patterns.py --all
- py tools\check_secret_patterns.py --base origin/codex/analytics-foundation
- py -m pytest -q tests\test_check_secret_patterns.py tests\test_check_local_environment.py tests\test_check_protected_surfaces.py
- git diff --check
- py tools\check_agent_docs.py
- py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation
- path-scoped protected-surface and secret/private-marker scans over the #264 contract and handoff files

Do not:
- print or copy raw matched values, raw private paths, raw log-like lines, runtime payloads, transport-failure payloads, generated data contents, private JSONL payloads, SQLite contents, workbook exports, endpoints, workbook identifiers, credentials, environment values, or local-only artifact contents;
- weaken scanner coverage;
- suppress findings without explicit policy rationale and tests;
- handle sanitized_fixture_marker, placeholder_secret_reference, or decode_replacement_used except as context;
- make all-repo scanner a failing gate;
- add CI gates;
- change parser/runtime/analytics/local app/workbook/webhook/App Script/Sheets/OpenAI/AI/production behavior;
- change credential policy or environment-variable contracts;
- target main;
- stage, commit, push, open a PR, merge, close #252, close #260, close #262, close #264, or mark tracker #136 complete unless explicitly asked.

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
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/264"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/136"
  source_issues:
    - "https://github.com/Tahjali11/Mythic-Edge/issues/252"
    - "https://github.com/Tahjali11/Mythic-Edge/issues/260"
    - "https://github.com/Tahjali11/Mythic-Edge/issues/262"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/private_local_v1_artifact_path_ambiguous_marker_warning_triage.md"
  target_artifact: "docs/implementation_handoffs/private_local_v1_artifact_path_ambiguous_marker_warning_triage_comparison.md"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  validation:
    - "git status --short --branch --untracked-files=all -> two untracked #264 docs artifacts"
    - "py tools/check_secret_patterns.py --all -> advisory non-clean, forbidden 540, warnings 901, exit code 0"
    - "py tools/check_secret_patterns.py --base origin/codex/analytics-foundation -> passed"
    - "py -m pytest -q tests/test_check_secret_patterns.py tests/test_check_local_environment.py tests/test_check_protected_surfaces.py -> 97 passed, 1 skipped"
    - "git diff --check -> passed"
    - "py tools/check_agent_docs.py -> passed"
    - "py tools/check_protected_surfaces.py --base origin/codex/analytics-foundation -> passed"
    - "path-scoped secret/private-marker scan over #264 docs -> passed"
    - "path-scoped protected-surface scan over #264 docs -> passed"
    - "direct whitespace/ascii/final-newline check over #264 docs -> passed"
  stop_conditions:
    - "Do not print or copy raw matched values or private artifacts."
    - "Do not weaken scanner coverage or suppress findings without explicit policy rationale and tests."
    - "Do not handle deferred warning categories except as context."
    - "Do not make all-repo scanner a failing gate or add CI gates."
    - "Do not change parser/runtime/analytics/local app/workbook/webhook/App Script/Sheets/OpenAI/AI/production behavior."
    - "Do not change credential policy or environment-variable contracts."
    - "Do not target main, close #252, close #260, close #262, close #264, or close tracker #136."
```
