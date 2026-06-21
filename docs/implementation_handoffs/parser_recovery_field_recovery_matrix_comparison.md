# Implementation Handoff: Parser Recovery Field Recovery Matrix

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/451

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/388

Parent private-evidence gate:
https://github.com/Tahjali11/Mythic-Edge/issues/434

## Contract

`docs/contracts/parser_recovery_field_recovery_matrix.md`

## Internal Project Area

Primary: Corpus / Provenance.

Supporting: Parser and Quality / Governance.

## Truth Owner

Parser truth remains owned by existing parser, router, event, state, model,
extractor, match/game identity, deduplication, and final reconciliation
layers. The new matrix owns only report-only recovery metadata and validation.

## Bridge-Code Status

`shared_support`

The module is shared support for future recovery review workflows. It does not
bridge parser output into workbook, webhook, Apps Script, analytics, AI,
coaching, runtime, corpus metadata, or fixture-promotion behavior.

## Role Performed

Codex C: Module Implementer.

## Comparison Summary

Confirmed before editing:

- Issue #451 is open and scoped to Field Recovery Matrix metadata.
- Pipeline tracker #388 remains open/inactive.
- Parent private-evidence issue #434 remains open.
- Previous PR #537 is merged with merge commit
  `a020311871738d4ea04d9244ac1635ef3936975c`.
- `origin/main` is at `a020311871738d4ea04d9244ac1635ef3936975c`.
- The contract was present as an untracked Codex B artifact and was copied into
  a clean issue worktree before implementation.
- No existing `field_recovery_matrix.py` or focused matrix tests existed.

Implemented:

- Added a pure static Field Recovery Matrix helper module.
- Added contracted object/schema constants.
- Added recovery category, parser-output policy, analytics-output policy,
  stale-source behavior, field-family, false-readiness, and non-claim
  vocabularies.
- Added representative seed rows covering all contracted recovery categories:
  direct, equivalent, derived_bounded, approximate_analytics_only,
  unavailable, blocked_private_evidence, blocked_external_boundary, and
  review_required.
- Reused evidence-ledger confidence, finality, drift flag, and ledger-entry
  vocabularies.
- Added validators for matrix shape, row shape, unknown vocabularies, duplicate
  field IDs, unknown ledger references, privacy markers, false readiness flags,
  summary consistency, and anti-promotion rules.
- Added focused tests for shape, vocabulary reuse, deterministic serialization,
  copy safety, anti-promotion behavior, blocked/private behavior, unknown
  ledger reference handling, readiness flag enforcement, privacy blocking, and
  duplicate IDs.

Not implemented:

- No parser behavior changes.
- No watcher, diagnostics, drift, runtime status, golden replay, corpus
  metadata, fixture, manifest, recovery packet, issue/fixture draft, workbook,
  webhook, Apps Script, analytics, AI, coaching, CI, merge, deploy, or
  production behavior changes.
- No private Player.log, UTC_Log, app-data, live MTGA, network, firewall,
  packet, OS/router, diagnostics, drift, or private smoke evidence was read or
  generated.
- No #388 or #381 activation.
- No readiness flags were changed to true.

## Files Changed

- `docs/contracts/parser_recovery_field_recovery_matrix.md`
  - Codex B contract source artifact retained in the clean worktree.
- `src/mythic_edge_parser/app/field_recovery_matrix.py`
  - New static metadata helper and validators.
- `tests/test_field_recovery_matrix.py`
  - New focused tests for the metadata helper.
- `docs/implementation_handoffs/parser_recovery_field_recovery_matrix_comparison.md`
  - This implementation handoff.

## Code Changed

Runtime code file added:

- `src/mythic_edge_parser/app/field_recovery_matrix.py`

Behavior surface:

- Static, side-effect-free metadata construction and validation only.
- New public helpers:
  - `build_field_recovery_matrix()`
  - `iter_field_recovery_rows()`
  - `validate_field_recovery_matrix(...)`
  - `validate_field_recovery_row(...)`

No parser runtime path imports or calls this module.

## Tests Added Or Updated

- `tests/test_field_recovery_matrix.py`

The test suite covers:

- matrix object shape and false readiness flags;
- representative recovery category coverage;
- evidence-ledger vocabulary reuse;
- deterministic JSON serialization;
- copy-safe row iteration;
- approximate/blocked/non-direct anti-promotion rules;
- unknown ledger entry review behavior;
- privacy and local-artifact marker rejection;
- duplicate field ID detection.

## Interface Changes

Added a report-only Python helper interface:

```python
FIELD_RECOVERY_MATRIX_OBJECT
FIELD_RECOVERY_MATRIX_SCHEMA_VERSION
FIELD_RECOVERY_MATRIX_ROW_OBJECT
build_field_recovery_matrix()
iter_field_recovery_rows()
validate_field_recovery_matrix(...)
validate_field_recovery_row(...)
```

No CLI, environment variable, workbook column, webhook payload, Apps Script,
runtime status, analytics schema, corpus metadata, fixture, golden replay
manifest, or parser event interface changed.

## Contracted Area Status

Implementation stayed within Corpus / Provenance shared support. Parser,
workbook, webhook, Apps Script, Google Sheets sync, runtime status, analytics,
AI, coaching, corpus metadata, fixture-promotion, CI, merge, deploy, release,
and production boundaries were not touched.

## Validation Run

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_field_recovery_matrix.py
# 10 passed

PYTHONPATH=src python3 -m pytest -q tests/test_evidence_ledger.py
# 101 passed

python3 -m ruff check src/mythic_edge_parser/app/field_recovery_matrix.py tests/test_field_recovery_matrix.py
# passed

git diff --check
# passed

python3 tools/check_agent_docs.py
# passed

printf '%s\n' docs/contracts/parser_recovery_field_recovery_matrix.md src/mythic_edge_parser/app/field_recovery_matrix.py tests/test_field_recovery_matrix.py | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
# passed

printf '%s\n' docs/contracts/parser_recovery_field_recovery_matrix.md src/mythic_edge_parser/app/field_recovery_matrix.py tests/test_field_recovery_matrix.py | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
# passed

printf '%s\n' docs/contracts/parser_recovery_field_recovery_matrix.md src/mythic_edge_parser/app/field_recovery_matrix.py tests/test_field_recovery_matrix.py | python3 tools/select_validation.py --base origin/main --paths-from-stdin --format text
# selection_status: ok

python3 -m ruff check src tests tools
# passed

PYTHONPATH=src python3 -m pytest -q tests
# 1863 passed
```

## Codex D Fixer Update

Finding fixed: `FRM-E-001`
(`embedded_local_path_privacy_gap_needs_codex_d_fixer`).

Fault category: implementation validation gap.

The original privacy scanner rejected strings that began with a local absolute
path, but missed embedded local paths inside otherwise public-safe text. The
fix changes the field-recovery privacy validator to search for embedded Unix,
colon-delimited Unix, `file:` URI, Windows-drive, and UNC-style local absolute
path shapes without echoing the matched value in returned errors.

Focused regression coverage was added for local paths embedded in
`restoration_requirements` and `forbidden_fallback_evidence`.

Codex D validation:

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_field_recovery_matrix.py
# 11 passed
```

No private/live evidence was read. No parser behavior, workbook/webhook/App
Script behavior, fixture promotion, corpus status, #388 activation, or
pipeline readiness behavior changed.

Not run:

- `python3 tools/run_pyright_advisory_report.py`
  - Selector reported this as advisory. Full pytest and Ruff passed; no typing
    gate was required by the contract.

## Still Unverified

- No private or live log evidence was checked by design.
- No actual field recovery, drift comparison, watcher, recovery packet,
  fixture promotion, or #388 activation was attempted.
- No downstream workbook, webhook, Apps Script, Google Sheets sync, analytics,
  AI, coaching, runtime status, merge, deploy, release, or production behavior
  was exercised or changed.

## Reviewer Focus

Codex E should verify:

- `field_recovery_matrix.py` is pure metadata and side-effect free.
- All readiness and authorization flags remain false.
- The representative seed rows reuse evidence-ledger vocabulary and real
  ledger entry IDs.
- Approximate, unavailable, blocked, equivalent, derived, and review-required
  rows cannot restore parser output by matrix policy.
- Privacy/local-artifact marker checks are conservative and do not echo private
  values.
- The module does not write files, read private data, mutate corpus metadata,
  activate #388/#381, or touch protected runtime/workbook/webhook/App Script
  surfaces.

## Next Workflow Action

Next role: Codex E: Module Reviewer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer for issue #451.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/451

Pipeline tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/388

Parent private-evidence issue:
https://github.com/Tahjali11/Mythic-Edge/issues/434

Previous issue:
https://github.com/Tahjali11/Mythic-Edge/issues/387

Previous PR:
https://github.com/Tahjali11/Mythic-Edge/pull/537

Contract:
docs/contracts/parser_recovery_field_recovery_matrix.md

Implementation handoff:
docs/implementation_handoffs/parser_recovery_field_recovery_matrix_comparison.md

Review scope:
- docs/contracts/parser_recovery_field_recovery_matrix.md
- src/mythic_edge_parser/app/field_recovery_matrix.py
- tests/test_field_recovery_matrix.py
- docs/implementation_handoffs/parser_recovery_field_recovery_matrix_comparison.md

Review focus:
- Confirm the module is pure metadata and side-effect free.
- Confirm readiness and authorization flags remain false.
- Confirm evidence-ledger confidence/finality/drift vocabulary is reused.
- Confirm approximate, unavailable, blocked, equivalent, derived, and
  review-required rows cannot restore parser output by matrix policy.
- Confirm privacy/local-artifact marker validation is conservative.
- Confirm no parser behavior, runtime status, workbook, webhook, Apps Script,
  Google Sheets sync, analytics, AI, coaching, corpus metadata, fixture,
  manifest, recovery packet, #388 activation, #381 activation, merge, deploy,
  release, or production behavior changed.

Validation:
- PYTHONPATH=src python3 -m pytest -q tests/test_field_recovery_matrix.py
- PYTHONPATH=src python3 -m pytest -q tests/test_evidence_ledger.py
- python3 -m ruff check src/mythic_edge_parser/app/field_recovery_matrix.py tests/test_field_recovery_matrix.py
- git diff --check
- python3 tools/check_agent_docs.py
- path-scoped secret/private marker scan
- path-scoped protected-surface check

Do not:
- Change parser behavior.
- Read or run private/live evidence.
- Create fixtures, manifests, expected outputs, recovery packets, corpus
  metadata, issue/fixture drafts, or local/generated artifacts.
- Activate #388 or #381.
- Claim parser_behavior_ready, pipeline activation readiness, fixture-promotion
  readiness, field recovery readiness, private smoke success, release
  readiness, production readiness, analytics truth, AI truth, coaching truth,
  or full parser regression parity.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/451"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  parent_private_evidence_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/387"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/537"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_recovery_field_recovery_matrix.md"
  target_artifact: "docs/implementation_handoffs/parser_recovery_field_recovery_matrix_comparison.md"
  verdict: "field_recovery_matrix_metadata_ready_for_review"
  risk_tier: "High"
  base_branch: "main"
  target_branch: "main"
  branch: "codex/parser-recovery-field-recovery-matrix-451"
  previous_merge_commit: "a020311871738d4ea04d9244ac1635ef3936975c"
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  evidence_pipeline_planning_ready_for_issue_388: false
  file_writing_authorized: false
  private_harvest_authorized: false
  fixture_promotion_authorized: false
  corpus_status_change_authorized: false
  validation:
    - "PYTHONPATH=src python3 -m pytest -q tests/test_field_recovery_matrix.py"
    - "PYTHONPATH=src python3 -m pytest -q tests/test_evidence_ledger.py"
    - "python3 -m ruff check src/mythic_edge_parser/app/field_recovery_matrix.py tests/test_field_recovery_matrix.py"
    - "git diff --check"
    - "python3 tools/check_agent_docs.py"
    - "path-scoped secret/private marker scan passed"
    - "path-scoped protected-surface check passed"
    - "path-scoped validation selector passed"
    - "python3 -m ruff check src tests tools"
    - "PYTHONPATH=src python3 -m pytest -q tests"
  stop_conditions:
    - "Do not activate #388 or #381."
    - "Do not read or run private/live evidence."
    - "Do not change parser behavior or protected runtime/workbook/webhook/App Script surfaces."
    - "Do not promote blocked, approximate, fallback, or review-required evidence to parser truth."
    - "Do not claim parser behavior readiness, pipeline activation readiness, fixture-promotion readiness, release readiness, production readiness, analytics truth, AI truth, coaching truth, or full parser regression parity."
```
