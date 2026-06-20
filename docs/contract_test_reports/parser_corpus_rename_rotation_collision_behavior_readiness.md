# Parser Corpus Rename/Rotation Collision Behavior Readiness Contract Test Report

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/508

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/158

Related pipeline tracker: https://github.com/Tahjali11/Mythic-Edge/issues/388

Parent private-evidence issue: https://github.com/Tahjali11/Mythic-Edge/issues/434

## Contract

`docs/contracts/parser_corpus_rename_rotation_collision_behavior_readiness.md`

## Implementation Under Test

Docs-only contract decision on `main`:

- `docs/contracts/parser_corpus_rename_rotation_collision_behavior_readiness.md`

No Codex C implementation package, manifest promotion, session-ledger edit,
fixture creation, parser behavior change, private/live check, #388/#381
activation, or production-surface change is under test for this review.

## Report Lifecycle

`report_lifecycle`: `final_approval`

## Contract Summary

The contract reviews `drift_debug.rename_or_rotation_collision` after adjacent
behavior-readiness rows changed. It selects `preserve_report_only`, keeps the
current row at `covered_report_only`, and explicitly forbids adding
`parser_behavior_verified` now.

The contract also preserves these non-claims:

- no live file-system truth;
- no watcher correctness;
- no rename/recycle collision handling;
- no duplicate/replay prevention;
- no parser drift recovery truth;
- no release, production, analytics, AI, coaching, tracker-completion, or full
  corpus-parity claim.

## Internal Project Area Reviewed

Primary: Corpus / Provenance.

Supporting: Quality / Governance for readiness-language and workflow-boundary
discipline.

No parser, runtime, analytics, workbook, webhook, Apps Script, AI/coaching, CI,
merge, deploy, release, production, or private-evidence execution authority is
created by this contract.

## Bridge-Code Status Reviewed

`deferred_future_boundary`

This contract authorizes no bridge code. Future split, uplift,
parser-evidence-pipeline, or private-evidence paths require a separate issue
and contract.

## Checks Run

```bash
gh issue view 508 --repo Tahjali11/Mythic-Edge --json number,title,state,body,url,labels
python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
python3 tools/check_agent_docs.py
git diff --check
python3 tools/select_validation.py --base origin/main --paths-from-stdin
python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
```

The path-scoped `select_validation.py`, `check_secret_patterns.py`, and
`check_protected_surfaces.py` runs used:

```text
docs/contracts/parser_corpus_rename_rotation_collision_behavior_readiness.md
docs/contract_test_reports/parser_corpus_rename_rotation_collision_behavior_readiness.md
```

## Results

- GitHub issue #508 is open and matches the selected family and preservation
  path.
- Corpus parity report passed and reported:
  `partial_coverage_map_ready (45 families; committed=6, synthetic=22,
  report_only=11, blocked=6 [private=2, external=4], missing=0,
  parser_behavior_ready=no)`.
- Current manifest row for `rename_rotation_collision_boundary_report_v1`
  remains `covered_report_only` with `coverage_basis:
  ["fixture_metadata_only"]` and empty `parser_event_families`.
- Current session-ledger row keeps dedicated collision fixtures, file-identity
  claims, rename collision claims, recycle collision claims,
  duplicate/replay-prevention claims, private smoke claims, and production
  watcher claims at zero.
- `python3 tools/check_agent_docs.py` passed with 0 errors and 0 warnings.
- `git diff --check` passed.
- `python3 tools/select_validation.py --base origin/main --paths-from-stdin`
  returned `selection_status: ok`.
- Path-scoped secret/private-marker scan over the contract and report passed
  with 0 forbidden findings and 0 warnings.
- Path-scoped protected-surface scan over the contract and report passed with
  0 forbidden findings and 0 warnings.

## Finding Lifecycle Summary

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| none | none | `not_reproduced` | no active findings | not_blocking | No blocking finding identified in this review. | Contract, issue #508, corpus manifest/session ledger, corpus parity CLI, agent-doc check, diff check, selector, secret scan, and protected-surface scan all match the preservation path. | F |

## Confirmed Contract Matches

- The contract exists at the expected path.
- It selects `preserve_report_only`.
- It keeps `drift_debug.rename_or_rotation_collision` at
  `covered_report_only`.
- It explicitly says `parser_behavior_verified` may not be added now.
- It authorizes no implementation, manifest promotion, session-ledger edit,
  fixture creation, parser behavior change, private/live check, or status
  transition.
- It keeps #388/#381 inactive.
- It preserves `parser_behavior_ready=false` and
  `pipeline_activation_ready_for_issue_388=false`.
- It keeps adjacent `log_runtime.rotation`, `log_runtime.unknown_entry`,
  `drift_debug.missing_message_type`, and
  `drift_debug.recycle_or_rollback` evidence separate.
- It preserves privacy and non-claim boundaries for raw/private logs, local
  paths, hashes, byte-size lists, capture-date rows, runtime artifacts,
  workbook exports, credentials, tokens, API keys, and webhook URLs.

## Contract Mismatches

None.

## Missing Tests

None for this contract-only preservation decision.

No implementation package is authorized, so no new parser/runtime tests are
required. Future split or uplift work would need its own focused tests under a
new issue and contract.

## Drift Notes

- Repo drift: none found for this contract review.
- Corpus metadata drift: none found. The manifest and session ledger still
  represent the row as report-only boundary metadata.
- Issue lifecycle drift: none found. Issue #508 is open; trackers #158, #388,
  and #434 remain open by contract.
- Product-surface drift: none found. No parser, tailer, stream, diagnostics,
  drift, workbook, webhook, Apps Script, analytics, AI/coaching, CI, merge,
  deploy, release, or production behavior is changed or authorized.

## Recommendation

Approve.

The safe next role is Codex F: Module Submitter for the docs-only contract and
this contract-test report.

## Next Workflow Action

Next role: Codex F: Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #508.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/508

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/158

Related pipeline tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/388

Parent private-evidence issue:
https://github.com/Tahjali11/Mythic-Edge/issues/434

Base branch:
main

Target branch:
main

Reviewed artifacts:
- docs/contracts/parser_corpus_rename_rotation_collision_behavior_readiness.md
- docs/contract_test_reports/parser_corpus_rename_rotation_collision_behavior_readiness.md

Goal:
Submit the docs-only #508 contract package as a draft PR targeting main. Stage
only the reviewed #508 contract and contract-test report. Do not stage unrelated
files.

Validation to rerun:
- python3 tools/check_agent_docs.py
- git diff --check
- python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
- path-scoped secret/private-marker scan for the reviewed files
- path-scoped protected-surface scan for the reviewed files

Do not:
- activate #388/#381;
- close #158, #388, #434, or #508;
- promote blocked or report-only rows;
- claim live file-system truth, watcher correctness, rename/recycle collision
  handling, duplicate/replay prevention, parser drift recovery truth, release
  readiness, production behavior, analytics truth, AI truth, coaching truth,
  tracker completion, or full corpus parity;
- change parser/runtime/workbook/webhook/App Script/analytics/AI/coaching/CI
  behavior.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/508"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  related_pipeline_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  parent_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contracts/parser_corpus_rename_rotation_collision_behavior_readiness.md"
  target_artifact: "docs/contract_test_reports/parser_corpus_rename_rotation_collision_behavior_readiness.md"
  risk_tier: "High"
  base_branch: "main"
  target_branch: "main"
  branch: "main"
  selected_family: "drift_debug.rename_or_rotation_collision"
  current_status: "covered_report_only"
  selected_path: "preserve_report_only"
  parser_behavior_verified_may_be_added_now: false
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  validation:
    - "gh issue view 508 --repo Tahjali11/Mythic-Edge --json number,title,state,body,url,labels"
    - "python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json"
    - "python3 tools/check_agent_docs.py"
    - "git diff --check"
    - "python3 tools/select_validation.py --base origin/main --paths-from-stdin"
    - "python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin"
    - "python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin"
  stop_conditions:
    - "Do not activate #388/#381."
    - "Do not close tracker #158, #388, #434, or #508."
    - "Do not promote blocked or report-only rows."
    - "Do not claim live file-system truth, watcher correctness, rename collision handling, recycle collision handling, duplicate/replay prevention, parser drift recovery truth, release readiness, production behavior, analytics truth, AI truth, coaching truth, tracker completion, or full corpus parity."
    - "Do not change parser/runtime/workbook/webhook/App Script/analytics/AI/coaching/CI behavior."
```
