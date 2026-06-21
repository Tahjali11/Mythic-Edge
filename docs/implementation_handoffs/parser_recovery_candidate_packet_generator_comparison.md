# Implementation Handoff: Parser Recovery Candidate Packet Generator

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/454

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/388

Parent private-evidence issue:
https://github.com/Tahjali11/Mythic-Edge/issues/434

## Contract

`docs/contracts/parser_recovery_candidate_packet_generator.md`

## Internal Project Area

Primary: Corpus / Provenance.

Supporting: Quality / Governance, Parser, and Generated / Local Artifacts
boundaries.

## Truth Owner

Parser truth remains owned by existing parser, router, event, state, model,
extractor, match/game identity, deduplication, and final reconciliation
layers.

This implementation owns only in-memory recovery candidate packet review
metadata and validation. It does not own parser facts, private evidence,
fixture expected output, corpus status, readiness, analytics truth, AI truth,
coaching truth, or tracker completion.

## Bridge-Code Status

`shared_support`

The new helper is shared support from Corpus / Provenance to Quality /
Governance review workflows. It composes existing #451 Field Recovery Matrix,
#452 symbolic offset-window metadata, and #453 field-evidence comparison
reports. It does not create a reverse-flow into parser behavior, corpus
status, fixture promotion, private harvest, diagnostics, drift, workbook,
analytics, AI, coaching, or #388/#381 activation.

## Role Performed

Codex C: Module Implementer.

Codex D: Module Fixer for RCAND-E-001 direct packet forbidden-key validation
gap.

Codex D: Module Fixer for RCAND-E-002 context identity value echo blocker.

## What Changed

Implemented the #454 recovery candidate packet generator as a deterministic,
public-safe, in-memory helper.

Added:

- report and packet schema constants;
- candidate status, candidate category, reviewer decision, privacy status,
  false-readiness, protected-surface, and non-claim vocabularies;
- `build_recovery_candidate_packet_report(...)`;
- `build_recovery_candidate_packet(...)`;
- validators for reports, packets, and reviewer decision scaffolds;
- fail-closed scanning for private markers, forbidden keys, readiness claims,
  authorization claims, protected-surface assertions, local path markers, raw
  payload markers, exact offset/size/timestamp markers, raw hashes, and secret
  markers;
- deterministic packet IDs from public-safe symbolic fields only;
- focused tests for contracted statuses, non-claims, privacy failures,
  false-flag enforcement, copy safety, and no runtime/file-writer imports.

Codex D fixer update:

- direct report, packet, and reviewer-decision validators now apply the same
  forbidden-key scanner used by raw input validation;
- generated report and packet self-checks include forbidden-key scans before
  returning public in-memory mappings;
- focused regression coverage proves direct packet/report validation rejects
  representative forbidden keys without echoing caller-supplied values.
- second Codex D pass fixed the remaining builder-path bypass where a
  caller-supplied comparison row could contain forbidden keys that were dropped
  from the sanitized packet output before validation.
- third Codex D pass fixed the context identity echo path so caller-supplied
  `source_issue`, `pipeline_tracker`, and `parent_private_evidence_issue`
  values can trigger fail-closed handling without being copied into the
  returned report.

Not implemented:

- no parser behavior changes;
- no parser runtime imports;
- no CLI;
- no packet file writer;
- no diagnostics, drift, runtime status, golden replay, feature-equity,
  evidence-ledger, workbook, webhook, Apps Script, local app, analytics, AI, or
  coaching integration;
- no private harvest, source discovery, watcher startup, tailer startup, or
  source content reads;
- no fixture promotion, corpus status changes, #388 activation, or #381
  activation.

## Files Changed

- `docs/contracts/parser_recovery_candidate_packet_generator.md`
  - Codex B contract source artifact, retained as part of this implementation
    package.
- `src/mythic_edge_parser/app/recovery_candidate_packet_generator.py`
  - New in-memory packet helper and validators.
- `tests/test_recovery_candidate_packet_generator.py`
  - New focused tests for the helper.
- `docs/implementation_handoffs/parser_recovery_candidate_packet_generator_comparison.md`
  - This implementation handoff.

## Code Changed

Runtime code file added:

- `src/mythic_edge_parser/app/recovery_candidate_packet_generator.py`

Behavior surface:

- Static, side-effect-free packet construction and validation only.
- New public helpers:
  - `build_recovery_candidate_packet_report(...)`
  - `build_recovery_candidate_packet(...)`
  - `validate_recovery_candidate_packet_report(...)`
  - `validate_recovery_candidate_packet(...)`
  - `validate_recovery_candidate_review_decision(...)`

No parser runtime path imports or calls this module.

## Tests Added Or Updated

- `tests/test_recovery_candidate_packet_generator.py`

The test suite covers:

- report object shape and false readiness/authorization flags;
- deterministic JSON serialization;
- direct packet review-only behavior;
- equivalent, derived-bounded, and approximate analytics-only review metadata;
- unavailable, blocked-private, and blocked-external non-authorization;
- stale, degraded, and conflict routing;
- fail-closed privacy handling without value echo;
- direct packet/report forbidden-key rejection without value echo;
- direct packet builder fail-closed handling for forbidden keys in
  caller-supplied comparison rows;
- context-supplied readiness/protected-surface claims failing closed;
- context-supplied identity values failing closed without value echo;
- reviewer decision drift rejection;
- summary counts not becoming readiness metrics;
- copy safety;
- no parser runtime or file-writer imports.

## Interface Changes

Added a report-only Python helper interface:

```python
RECOVERY_CANDIDATE_PACKET_REPORT_OBJECT
RECOVERY_CANDIDATE_PACKET_SCHEMA_VERSION
RECOVERY_CANDIDATE_PACKET_OBJECT
RECOVERY_CANDIDATE_REVIEW_DECISION_OBJECT
build_recovery_candidate_packet_report(...)
build_recovery_candidate_packet(...)
validate_recovery_candidate_packet_report(...)
validate_recovery_candidate_packet(...)
validate_recovery_candidate_review_decision(...)
```

No CLI, environment variable, workbook column, webhook payload, Apps Script,
runtime status, analytics schema, corpus metadata, fixture, golden replay
manifest, or parser event interface changed.

## Contracted Area Status

Implementation stayed within Corpus / Provenance shared support and Quality /
Governance validation boundaries.

Parser, workbook, webhook, Apps Script, Google Sheets sync, runtime status,
diagnostics, drift, golden replay, feature-equity, evidence-ledger behavior,
analytics, AI, coaching, corpus metadata, fixture-promotion, CI, merge, deploy,
release, and production boundaries were not touched.

False flags remain false:

```yaml
parser_behavior_ready: false
pipeline_activation_ready_for_issue_388: false
file_writing_authorized: false
private_harvest_authorized: false
fixture_promotion_authorized: false
corpus_status_change_authorized: false
field_recovery_ready: false
```

## Validation Run

Passed:

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_recovery_candidate_packet_generator.py
# 10 passed in 0.66s

PYTHONPATH=src python3 -m pytest -q tests/test_field_evidence_comparison_report.py tests/test_field_recovery_matrix.py tests/test_local_watcher_offset_window_monitor.py
# 37 passed in 1.05s

python3 -m ruff check src/mythic_edge_parser/app/recovery_candidate_packet_generator.py tests/test_recovery_candidate_packet_generator.py
# All checks passed!

git diff --check
# passed with no output

python3 tools/check_agent_docs.py
# passed: errors 0, warnings 0

printf '%s\n' \
  docs/contracts/parser_recovery_candidate_packet_generator.md \
  src/mythic_edge_parser/app/recovery_candidate_packet_generator.py \
  tests/test_recovery_candidate_packet_generator.py \
  | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
# passed: forbidden 0, warnings 0

printf '%s\n' \
  docs/contracts/parser_recovery_candidate_packet_generator.md \
  src/mythic_edge_parser/app/recovery_candidate_packet_generator.py \
  tests/test_recovery_candidate_packet_generator.py \
  | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
# passed: forbidden 0, warnings 0

printf '%s\n' \
  docs/contracts/parser_recovery_candidate_packet_generator.md \
  src/mythic_edge_parser/app/recovery_candidate_packet_generator.py \
  tests/test_recovery_candidate_packet_generator.py \
  | python3 tools/select_validation.py --base origin/main --paths-from-stdin --format text
# selection_status: ok

python3 -m ruff check src tests tools
# All checks passed!

PYTHONPATH=src python3 -m pytest -q tests
# 1911 passed in 22.96s
```

Advisory:

```bash
python3 tools/run_pyright_advisory_report.py
# status: advisory_findings
# exit_code: 1
# errors: 396
# gate_behavior: advisory_non_blocking
```

Codex D fixer validation through RCAND-E-002:

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_recovery_candidate_packet_generator.py
# 13 passed in 1.04s

PYTHONPATH=src python3 -m pytest -q tests/test_field_evidence_comparison_report.py tests/test_field_recovery_matrix.py tests/test_local_watcher_offset_window_monitor.py tests/test_recovery_candidate_packet_generator.py
# 50 passed in 2.14s

python3 -m ruff check src/mythic_edge_parser/app/recovery_candidate_packet_generator.py tests/test_recovery_candidate_packet_generator.py
# All checks passed!

python3 -m ruff check src tests tools
# All checks passed!

git diff --check
# passed with no output

python3 tools/check_agent_docs.py
# result: passed; errors 0; warnings 0

printf '%s\n' \
  docs/contracts/parser_recovery_candidate_packet_generator.md \
  src/mythic_edge_parser/app/recovery_candidate_packet_generator.py \
  tests/test_recovery_candidate_packet_generator.py \
  docs/implementation_handoffs/parser_recovery_candidate_packet_generator_comparison.md \
  | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
# passed: forbidden 0, warnings 0

printf '%s\n' \
  docs/contracts/parser_recovery_candidate_packet_generator.md \
  src/mythic_edge_parser/app/recovery_candidate_packet_generator.py \
  tests/test_recovery_candidate_packet_generator.py \
  docs/implementation_handoffs/parser_recovery_candidate_packet_generator_comparison.md \
  | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
# passed: forbidden 0, warnings 0

if rg -n "[[:blank:]]$" docs/contracts/parser_recovery_candidate_packet_generator.md src/mythic_edge_parser/app/recovery_candidate_packet_generator.py tests/test_recovery_candidate_packet_generator.py docs/implementation_handoffs/parser_recovery_candidate_packet_generator_comparison.md; then exit 1; else echo "no trailing whitespace"; fi
# no trailing whitespace

printf '%s\n' \
  docs/contracts/parser_recovery_candidate_packet_generator.md \
  src/mythic_edge_parser/app/recovery_candidate_packet_generator.py \
  tests/test_recovery_candidate_packet_generator.py \
  docs/implementation_handoffs/parser_recovery_candidate_packet_generator_comparison.md \
  | python3 tools/select_validation.py --base origin/main --paths-from-stdin --format text
# selection_status: ok

PYTHONPATH=src python3 -m pytest -q tests
# 1914 passed in 23.99s

python3 tools/run_pyright_advisory_report.py
# status: advisory_findings; errors: 396; gate_behavior: advisory_non_blocking
```

Pyright remains advisory. The Codex C report produced type findings but no
tooling configuration blockers.

## Still Unverified

- No GitHub Actions/CI run has been observed for this local implementation.
- No post-fix Codex E adversarial review has occurred yet.
- No PR has been opened.
- No private/live evidence was run or read.
- No packet persistence path exists or was tested, by contract.
- Pyright advisory still reports existing repo type findings.

## Reviewer Focus

Codex E should verify:

- the new helper is deterministic, in-memory, and side-effect-free;
- it does not import parser runtime paths, `FileTailer`, local app, workbook,
  analytics, AI, or model-provider code;
- it does not write files or expose a CLI;
- packet IDs and summaries never include raw private values;
- forbidden keys, private markers, local paths, exact offsets/sizes/timestamps,
  raw hashes, raw payload markers, true readiness flags, authorization flags,
  and protected-surface claims fail closed without value echo;
- approximate, blocked, unavailable, degraded, stale, conflict, and
  review-required signals cannot become parser truth;
- reviewer decision scaffolds do not create issues, PRs, branches, fixtures,
  corpus status changes, private harvest authorization, or #388/#381
  activation.

## Next Workflow Action

Next role:

Codex E: Module Reviewer / Contract Tester.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / Contract Tester for the Codex D fixer pass
on issue #454.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/454

Pipeline tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/388

Parent private-evidence issue:
https://github.com/Tahjali11/Mythic-Edge/issues/434

Contract:
docs/contracts/parser_recovery_candidate_packet_generator.md

Implementation handoff:
docs/implementation_handoffs/parser_recovery_candidate_packet_generator_comparison.md

Review the implementation against the contract and issue. Focus on fail-closed
privacy behavior, false readiness flags, no parser/runtime imports, no file
writing, no private evidence reads, no fixture/corpus promotion, and no
#388/#381 activation. Specifically re-test RCAND-E-001: direct packet/report
validation must reject forbidden keys without echoing values.

Do not implement fixes unless explicitly asked. Lead with findings ordered by
severity, or state clearly if there are no blocking findings.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/454"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  parent_private_evidence_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/453"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/540"
  previous_merge_commit: "507952919718b729556bdd3a544ff14ce48f08a0"
  completed_thread: "D"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_recovery_candidate_packet_generator.md"
  target_artifact: "src/mythic_edge_parser/app/recovery_candidate_packet_generator.py; tests/test_recovery_candidate_packet_generator.py; docs/implementation_handoffs/parser_recovery_candidate_packet_generator_comparison.md"
  finding_id: "RCAND-E-002"
  finding_lifecycle: "blocker_fixed"
  verdict: "context_identity_value_echo_blocker_fixed_ready_for_module_review"
  risk_tier: "High"
  base_branch: "main"
  target_branch: "main"
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  file_writing_authorized: false
  private_harvest_authorized: false
  fixture_promotion_authorized: false
  corpus_status_change_authorized: false
  validation:
    - "PYTHONPATH=src python3 -m pytest -q tests/test_recovery_candidate_packet_generator.py -> 13 passed"
    - "PYTHONPATH=src python3 -m pytest -q tests/test_field_evidence_comparison_report.py tests/test_field_recovery_matrix.py tests/test_local_watcher_offset_window_monitor.py tests/test_recovery_candidate_packet_generator.py -> 49 passed"
    - "python3 -m ruff check src/mythic_edge_parser/app/recovery_candidate_packet_generator.py tests/test_recovery_candidate_packet_generator.py -> All checks passed!"
    - "python3 -m ruff check src tests tools -> All checks passed!"
    - "git diff --check -> passed with no output"
    - "python3 tools/check_agent_docs.py -> passed: errors 0, warnings 0"
    - "path-scoped secret/private-marker scan over #454 files -> forbidden 0, warnings 0"
    - "path-scoped protected-surface scan over #454 files -> forbidden 0, warnings 0"
    - "direct trailing-whitespace scan over #454 files -> no trailing whitespace"
    - "path-scoped validation selector over #454 files -> selection_status: ok"
    - "PYTHONPATH=src python3 -m pytest -q tests -> sandbox run hit localhost bind PermissionError; rerun outside sandbox passed with 1913 passed"
    - "python3 tools/run_pyright_advisory_report.py -> advisory_findings: 396 type findings; gate_behavior: advisory_non_blocking"
  stop_conditions:
    - "Do not close #388, #454, or #434."
    - "Do not activate #388 or #381."
    - "Do not run or read private Player.log, UTC_Log, app-data, live MTGA, network, firewall/drop, packet, OS/router, diagnostics, drift, watcher, tailer, or private smoke checks."
    - "Do not create recovery packet files, fixture-promotion files, proof files, metadata diff files, issue drafts, PR-assist artifacts, local artifacts, fixtures, manifests, corpus metadata edits, runtime artifacts, or workbook exports."
    - "Do not promote blocked, report-only, private-evidence, external-boundary, approximate, fallback, watcher, offset-window, degraded, stale, unavailable, or review-required signals to parser truth."
    - "Do not change parser behavior, parser event classes, parser state final reconciliation, router semantics, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets sync, output transport, diagnostics, drift, golden replay, feature-equity, evidence-ledger behavior, analytics behavior, AI/model-provider behavior, coaching behavior, CI gates, merge readiness, deploy readiness, release readiness, production behavior, or final integration policy."
    - "Do not claim parser_behavior_ready, pipeline activation readiness, file-writing authorization, fixture-promotion readiness, field recovery readiness, private smoke success, watcher correctness, release readiness, production readiness, analytics truth, AI truth, coaching truth, or full parser regression parity."
```
