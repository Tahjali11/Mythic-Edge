# Private Local V1 Fixture, Placeholder, And Decode Warning Triage Comparison

## Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/266
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/136
- Source issues:
  - https://github.com/Tahjali11/Mythic-Edge/issues/252
  - https://github.com/Tahjali11/Mythic-Edge/issues/260
  - https://github.com/Tahjali11/Mythic-Edge/issues/262
  - https://github.com/Tahjali11/Mythic-Edge/issues/264

## Contract

`docs/contracts/private_local_v1_fixture_placeholder_decode_warning_triage.md`

## Internal Project Area

Quality / Governance, with Generated / Local Artifacts as the supporting area.

## Truth Owner

The repo secret/private-marker scanner owns deterministic repository
content-safety classification and redacted scanner reporting. This handoff owns
only the #266 selected warning-family classification and follow-up routing.

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
- Starting status: one untracked #266 contract artifact,
  `docs/contracts/private_local_v1_fixture_placeholder_decode_warning_triage.md`
- No unrelated dirty tracked files were observed before editing.

## Files Inspected

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/contracts/private_local_v1_fixture_placeholder_decode_warning_triage.md`
- `docs/contracts/private_local_v1_private_artifact_scanner_env_ignore_posture.md`
- `docs/contracts/private_local_v1_high_risk_scanner_findings_triage.md`
- `docs/contracts/private_local_v1_raw_private_artifact_scanner_triage.md`
- `docs/contracts/private_local_v1_artifact_path_ambiguous_marker_warning_triage.md`
- `docs/implementation_handoffs/private_local_v1_artifact_path_ambiguous_marker_warning_triage_comparison.md`
- `docs/contract_test_reports/private_local_v1_artifact_path_ambiguous_marker_warning_triage.md`
- `docs/contracts/repo_wide_secret_private_marker_scanner.md`
- `tests/fixtures/golden_fixture_manifest.json`
- `tools/check_secret_patterns.py`
- `tools/check_local_environment.py`
- `tools/check_protected_surfaces.py`
- `tools/select_validation.py`
- `tests/test_check_secret_patterns.py`
- `tests/test_check_local_environment.py`
- `tests/test_check_protected_surfaces.py`
- GitHub issue #266, tracker #136, source issues #252, #260, #262, and #264
- PR #265 merge status and check status
- Selected scanner findings through structured category/path/symbol inventory,
  without copying raw matched values or raw excerpts into this report

## Current Behavior Compared To Contract

The contract asks #266 to classify the remaining focused warning-only
all-repo scanner debt after the #252 env-ignore posture work, #260 high-risk
scanner triage, #262 raw/private artifact triage, and #264 artifact-path /
ambiguous-marker warning triage.

Current behavior matches the contract baseline:

| Scanner mode | Result |
| --- | --- |
| all-repo advisory | non-clean, exit code 0 |
| changed-path scanner against `origin/codex/analytics-foundation` | clean |
| path-scoped scanner strictness | preserved |

The selected #266 tranche remains present and warning-only:

| Category | Severity | Count |
| --- | --- | ---: |
| `sanitized_fixture_marker` | warning | 174 |
| `placeholder_secret_reference` | warning | 9 |
| `decode_replacement_used` | warning | 3 |

Previously triaged scanner categories remain out of scope except as context:

- high-risk scanner categories from #260
- raw/private artifact categories from #262
- `artifact_path_reference` and `ambiguous_private_marker` from #264

## Implementation Option Chosen

Report-only triage and routing.

Reason: the selected warning families are already warning-only, concentrated
in approved fixture locations, redaction/scanner tests, sanitizer vocabulary,
scanner policy text, and binary/PDF documentation files. Editing fixtures,
tests, sanitizer wording, or PDFs just to reduce warning counts would risk
weakening evidence value or changing docs-generation policy. The smallest
contract-aligned Codex C action is to classify the warning families, preserve
scanner behavior, and route any cleanup into focused follow-up work.

## Files Changed

- Added
  `docs/implementation_handoffs/private_local_v1_fixture_placeholder_decode_warning_triage_comparison.md`

The untracked Codex B contract artifact was preserved and not edited:

- `docs/contracts/private_local_v1_fixture_placeholder_decode_warning_triage.md`

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
- Fixture changed: no
- PDF/docs binary changed: no
- Docs changed: yes
- Report-only: yes
- Scanner-policy-only: no

## All-Repo Scanner Warning Summary

Refreshed summary during this pass:

```text
mode: all-repo-advisory
result: failed
exit_code: 0
scanned_paths: 759
skipped_paths: 0
forbidden: 540
warnings: 901
```

Selected #266 warnings:

```text
selected_total: 186
```

## Selected Counts By Category And Severity

| Category | Severity | Count |
| --- | --- | ---: |
| `decode_replacement_used` | warning | 3 |
| `placeholder_secret_reference` | warning | 9 |
| `sanitized_fixture_marker` | warning | 174 |

## Selected Counts By Path Family

| Category | Path family | Count |
| --- | --- | ---: |
| `decode_replacement_used` | `docs/` | 3 |
| `placeholder_secret_reference` | `tests/` | 7 |
| `placeholder_secret_reference` | `docs/contracts/` | 1 |
| `placeholder_secret_reference` | `src/mythic_edge_parser/sanitize.py` | 1 |
| `sanitized_fixture_marker` | `tests/fixtures/evidence_schema_snapshots/` | 140 |
| `sanitized_fixture_marker` | `tests/fixtures/` | 34 |

## Highest-Count Selected Paths

These are repo-relative paths and counts only. No raw matched value or raw line
excerpt is recorded here.

| Category | Count | Path |
| --- | ---: | --- |
| `sanitized_fixture_marker` | 140 | `tests/fixtures/evidence_schema_snapshots/player_log_evidence_ledger_schema_snapshot.v1.json` |
| `sanitized_fixture_marker` | 12 | `tests/fixtures/parser_regression_bo3_slice.log` |
| `sanitized_fixture_marker` | 7 | `tests/fixtures/flush_timing_corpus_slice.log` |
| `sanitized_fixture_marker` | 7 | `tests/fixtures/parser_regression_match_slice.log` |
| `sanitized_fixture_marker` | 5 | `tests/fixtures/draft_parser_family_slice.log` |
| `sanitized_fixture_marker` | 3 | `tests/fixtures/router_smoke_slice.log` |
| `placeholder_secret_reference` | 3 | `tests/test_check_secret_patterns.py` |
| `placeholder_secret_reference` | 2 | `tests/test_app_outputs.py` |
| `decode_replacement_used` | 1 | `docs/Mythic_Edge_Deep_Dive_Guide.pdf` |
| `decode_replacement_used` | 1 | `docs/Mythic_Edge_Learning_Guide.pdf` |
| `decode_replacement_used` | 1 | `docs/Tailer_py_Deep_Dive.pdf` |

## Placeholder Warning Symbol Summary

These are path and symbol names only. No placeholder value is copied.

| Path | Count | Symbol or test family |
| --- | ---: | --- |
| `docs/contracts/repo_wide_secret_private_marker_scanner.md` | 1 | scanner policy text |
| `src/mythic_edge_parser/sanitize.py` | 1 | sanitizer module vocabulary |
| `tests/test_app_outputs.py` | 2 | webhook target redaction tests |
| `tests/test_check_secret_patterns.py` | 3 | scanner credential/placeholder ordering tests |
| `tests/test_evidence_schema_drift_report.py` | 1 | private caller redaction test |
| `tests/test_golden_replay_harness.py` | 1 | forbidden fixture content redaction test |

## Classification Matrix

| Category | Path family | Count | Classification | Resolution |
| --- | --- | ---: | --- | --- |
| `sanitized_fixture_marker` | `tests/fixtures/evidence_schema_snapshots/` | 140 | `expected_sanitized_fixture_evidence` | Evidence schema snapshot fixture intentionally preserves parser-observable shape for schema/provenance tests. No payload rewrite in #266. Future metadata polish can route through a fixture governance issue if needed. |
| `sanitized_fixture_marker` | `tests/fixtures/` | 34 | `expected_sanitized_fixture_evidence` | Parser regression, flush timing, draft parser family, and router smoke slices are approved sanitized fixture evidence. The golden fixture manifest documents sanitized source class, redaction categories, update policy, and limitations for key fixture families. |
| `placeholder_secret_reference` | `tests/` | 7 | `expected_placeholder_or_example` | Tests intentionally use placeholder-shaped values to prove scanner, sanitizer, output redaction, fixture rejection, and ordering behavior. No test rewrite in this report-only pass. |
| `placeholder_secret_reference` | `docs/contracts/` | 1 | `expected_placeholder_or_example` | Scanner policy text intentionally describes placeholder handling. No policy rewrite in #266. |
| `placeholder_secret_reference` | `src/mythic_edge_parser/sanitize.py` | 1 | `expected_placeholder_or_example` | Sanitizer source vocabulary intentionally names redaction/placeholder behavior. Rewriting source wording is not needed and could reduce clarity. |
| `decode_replacement_used` | `docs/` | 3 | `decode_readability_warning` | Scanner replacement-decoded three PDF docs. This is a docs readability/scanner-confidence warning, not proof of private content. Do not regenerate, delete, or replace PDFs without a focused docs/PDF contract. |

## Concrete Cleanup Candidates

No concrete file edit was made in this report-only pass.

Potential future fixes:

1. Create a focused fixture governance issue if schema snapshots or log-slice
   fixtures need more explicit provenance metadata before a readiness claim.
2. Create a focused scanner-test readability issue if placeholder-shaped test
   inputs should move into helper builders.
3. Create a focused sanitizer-doc/source wording issue only if reviewers want
   placeholder vocabulary separated from scanner-sensitive text.
4. Create a docs/PDF maintenance issue if the three PDF docs should be
   regenerated, replaced, or excluded by an explicit scanner file-type policy.

## Path-Scoped Scanner Strictness Status

Preserved. No scanner rules, scanner exit semantics, allowlists, downgrades,
category semantics, or path-scoped strictness behavior changed.

## All-Repo Advisory Status

Preserved. The all-repo scanner remains advisory and non-clean. This pass does
not claim all-repo cleanliness or private-local-v1 private artifact readiness.

## Validation Run

```powershell
git status --short --branch --untracked-files=all
# passed; branch codex/analytics-foundation with two untracked #266 docs artifacts

py tools\check_secret_patterns.py --all
# advisory result remained non-clean as expected:
# scanned_paths 759, forbidden 540, warnings 901, process exit code 0

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

path-scoped secret/private-marker scan over the #266 contract and handoff
# passed; scanned_paths 2, forbidden 0, warnings 0

path-scoped protected-surface scan over the #266 contract and handoff
# passed; changed_paths 2, forbidden 0, warnings 0

direct whitespace/ascii/final-newline check over the #266 docs
# passed
```

## Protected-Surface Status

Passed for the #266 docs paths and base-diff scan. No protected runtime,
parser, analytics, workbook, webhook, Apps Script, Sheets, OpenAI, AI, or
production behavior was changed.

## Secret/Private-Marker Status

Passed for the #266 docs paths.

No raw matched values, raw private paths, raw log-like lines, runtime payloads,
transport-failure payloads, generated data contents, private JSONL payloads,
SQLite contents, workbook exports, endpoint values, workbook identifiers,
credential values, environment values, PDF decode text, fixture payload text,
or local-only artifact contents were added to this report.

## Generated/Private Artifact Status

No generated or private artifacts were intentionally created, copied,
sanitized, imported, moved, deleted, inspected, or committed by this
report-only pass.

## What Remains Unverified

- Codex E independent contract-test review.
- Whether fixture metadata should be expanded before a final
  private-local-v1 readiness claim.
- Whether placeholder-shaped tests should later use helper builders.
- Whether sanitizer placeholder vocabulary should be rewritten or left as
  clear source documentation.
- Whether the three PDF docs should be regenerated, replaced, or covered by a
  scanner file-type policy.
- Full all-repo scanner cleanup.
- #252 private-local-v1 private artifact readiness.
- #260, #262, and #264 lifecycle reconciliation.
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
- no PDF documentation regenerated, deleted, or replaced

## Next Workflow Action

Next recommended role: Codex E: Module Reviewer / contract-test thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #266.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/266

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/136

Source issues:
- https://github.com/Tahjali11/Mythic-Edge/issues/252
- https://github.com/Tahjali11/Mythic-Edge/issues/260
- https://github.com/Tahjali11/Mythic-Edge/issues/262
- https://github.com/Tahjali11/Mythic-Edge/issues/264

Branch:
codex/analytics-foundation

Contract:
docs/contracts/private_local_v1_fixture_placeholder_decode_warning_triage.md

Implementation handoff:
docs/implementation_handoffs/private_local_v1_fixture_placeholder_decode_warning_triage_comparison.md

Expected review artifact:
docs/contract_test_reports/private_local_v1_fixture_placeholder_decode_warning_triage.md

Goal:
Review the Codex C #266 fixture, placeholder, and decode warning triage against the contract. Verify selected warning counts, path-family classifications, raw-value redaction, fixture/PDF safety boundaries, path-scoped scanner strictness, all-repo advisory/no-gate posture, and explicit follow-up routing.

Review focus:
- Check classification of sanitized_fixture_marker, placeholder_secret_reference, and decode_replacement_used warning families.
- Confirm no raw matched values, raw private paths, raw log-like lines, runtime payloads, transport-failure payloads, generated data contents, private JSONL payloads, SQLite contents, workbook exports, endpoints, workbook identifiers, credentials, environment values, PDF decode text, fixture payload text, or local-only artifact contents were copied into docs or reports.
- Decide whether report-only classification is sufficient for this #266 pass or whether Codex D should rewrite selected docs/tests/fixture metadata.
- Pay special attention to fixture provenance metadata, placeholder-shaped test values, sanitizer source vocabulary, and the three PDF decode warnings.
- Confirm no scanner coverage was weakened and no path-scoped scanner strictness was relaxed.
- Confirm all-repo scanner remains advisory and non-clean.
- Confirm #252 private-local-v1 readiness, #260/#262/#264 lifecycle completion, and tracker #136 completion are not claimed.

Validation:
- git status --short --branch --untracked-files=all
- py tools\check_secret_patterns.py --all
- py tools\check_secret_patterns.py --base origin/codex/analytics-foundation
- py -m pytest -q tests\test_check_secret_patterns.py tests\test_check_local_environment.py tests\test_check_protected_surfaces.py
- git diff --check
- py tools\check_agent_docs.py
- py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation
- path-scoped protected-surface and secret/private-marker scans over the #266 contract and handoff files

Do not:
- print or copy raw matched values, raw private paths, raw log-like lines, runtime payloads, transport-failure payloads, generated data contents, private JSONL payloads, SQLite contents, workbook exports, endpoints, workbook identifiers, credentials, environment values, PDF decode text, fixture payload text, or local-only artifact contents;
- weaken scanner coverage;
- suppress findings without explicit policy rationale and tests;
- fix all all-repo scanner categories;
- regenerate, delete, or replace PDF docs without a focused docs/PDF contract;
- make all-repo scanner a failing gate;
- add CI gates;
- change parser/runtime/analytics/local app/workbook/webhook/App Script/Sheets/OpenAI/AI/production behavior;
- change credential policy or environment-variable contracts;
- target main;
- stage, commit, push, open a PR, merge, close #252, close #260, close #262, close #264, close #266, or mark tracker #136 complete unless explicitly asked.

Final review output must include:
- role performed;
- issue/tracker/source issues;
- contract and handoff reviewed;
- findings first, ordered by severity;
- classification accuracy status;
- raw-value redaction status;
- fixture/PDF boundary status;
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
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/266"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/136"
  source_issues:
    - "https://github.com/Tahjali11/Mythic-Edge/issues/252"
    - "https://github.com/Tahjali11/Mythic-Edge/issues/260"
    - "https://github.com/Tahjali11/Mythic-Edge/issues/262"
    - "https://github.com/Tahjali11/Mythic-Edge/issues/264"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/private_local_v1_fixture_placeholder_decode_warning_triage.md"
  target_artifact: "docs/implementation_handoffs/private_local_v1_fixture_placeholder_decode_warning_triage_comparison.md"
  risk_tier: "Medium"
  branch: "codex/analytics-foundation"
  validation:
    - "git status --short --branch --untracked-files=all -> two untracked #266 docs artifacts"
    - "py tools/check_secret_patterns.py --all -> advisory non-clean, forbidden 540, warnings 901, exit code 0"
    - "py tools/check_secret_patterns.py --base origin/codex/analytics-foundation -> passed"
    - "py -m pytest -q tests/test_check_secret_patterns.py tests/test_check_local_environment.py tests/test_check_protected_surfaces.py -> 97 passed, 1 skipped"
    - "git diff --check -> passed"
    - "py tools/check_agent_docs.py -> passed"
    - "py tools/check_protected_surfaces.py --base origin/codex/analytics-foundation -> passed"
    - "path-scoped secret/private-marker scan over #266 docs -> passed"
    - "path-scoped protected-surface scan over #266 docs -> passed"
    - "direct whitespace/ascii/final-newline check over #266 docs -> passed"
  stop_conditions:
    - "Do not print or copy raw matched values or private artifacts."
    - "Do not weaken scanner coverage or suppress findings without explicit policy rationale and tests."
    - "Do not fix all all-repo scanner categories under #266."
    - "Do not make all-repo scanner a failing gate or add CI gates."
    - "Do not regenerate, delete, or replace PDF docs without a focused docs/PDF contract."
    - "Do not change parser/runtime/analytics/local app/workbook/webhook/App Script/Sheets/OpenAI/AI/production behavior."
    - "Do not change credential policy or environment-variable contracts."
    - "Do not target main, close #252, close #260, close #262, close #264, close #266, or close tracker #136."
```
