# Implementation Handoff: Parser Recovery Issue And Fixture Draft Generator

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/455

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/388

Parent private-evidence issue:
https://github.com/Tahjali11/Mythic-Edge/issues/434

## Contract

`docs/contracts/parser_recovery_issue_fixture_draft_generator.md`

## Internal Project Area

Primary: Quality / Governance.

Supporting: Corpus / Provenance and Generated / Local Artifacts boundaries.

## Truth Owner

Parser truth remains owned by existing parser, router, event, state, model,
extractor, match/game identity, deduplication, and final reconciliation
layers.

This implementation owns only in-memory issue/fixture draft review metadata
and validation. It does not own parser facts, private evidence, fixture
expected output, corpus status, readiness, analytics truth, AI truth, coaching
truth, issue lifecycle, PR lifecycle, or tracker completion.

## Bridge-Code Status

`shared_support`

The new helper is shared support from Corpus / Provenance recovery packets to
Quality / Governance review workflows. It composes #454 recovery candidate
packet objects into review-only issue draft, fixture summary, manifest summary,
and checklist objects. It does not create reverse-flow into parser behavior,
fixture promotion, corpus status, private harvest, diagnostics, drift,
workbook, analytics, AI, coaching, GitHub issue/PR lifecycle, or #388/#381
activation.

## Role Performed

Codex C: Module Implementer.

Codex D: Module Fixer for RIFDRAFT-E-001 and RIFDRAFT-E-002.

Codex D: Rebound Module Fixer for remaining RIFDRAFT-E-001/RIFDRAFT-E-002
value-echo gaps.

Codex D: Module Fixer for RIFDRAFT-E-003 and RIFDRAFT-E-004 remaining
contract mismatches.

## What Changed

Implemented the #455 recovery issue and fixture draft generator as a
deterministic, public-safe, in-memory helper.

Added:

- report, draft group, issue draft, fixture summary, manifest summary, and
  checklist schema constants;
- status, draft type, fixture evidence class, next-role, non-claim, false
  readiness, false authorization, and protected-surface vocabularies;
- `build_recovery_issue_fixture_draft_report(...)`;
- `build_recovery_issue_fixture_draft_group(...)`;
- `build_recovery_issue_draft(...)`;
- `build_recovery_fixture_draft_summary(...)`;
- `build_recovery_manifest_draft_summary(...)`;
- `build_recovery_draft_review_checklist(...)`;
- validators for reports and nested draft objects;
- fail-closed scanning for private markers, local paths, raw payload keys,
  exact offsets/sizes/timestamps/hashes, secret markers, true readiness or
  authorization claims, protected-surface assertions, and GitHub closing
  keywords;
- `Refs`-only issue lifecycle wording;
- deterministic draft IDs from public-safe symbolic fields only;
- focused tests for contracted statuses, non-claims, lifecycle wording,
  blocked-private/external preservation, privacy failures, false-flag
  enforcement, copy safety, and no runtime/file-writer/GitHub imports.

Not implemented:

- no parser behavior changes;
- no parser runtime imports;
- no CLI;
- no issue draft file writer;
- no fixture file writer;
- no golden replay manifest writer;
- no corpus metadata writer;
- no GitHub issue/PR/comment/label/status-check integration;
- no diagnostics, drift, runtime status, golden replay, feature-equity,
  evidence-ledger, workbook, webhook, Apps Script, local app, analytics, AI, or
  coaching integration;
- no private harvest, source discovery, watcher startup, tailer startup, or
  source content reads;
- no fixture promotion, corpus status changes, #388 activation, or #381
  activation.

Codex D fixer update:

- Fixed RIFDRAFT-E-001 by treating direct lifecycle action keys such as
  `closes`, `fixes`, `resolves`, `closed_by`, and `done_by` as forbidden
  keys, including camelCase or punctuation-normalized variants.
- Fixed RIFDRAFT-E-002 by treating direct protected-surface flags such as
  `parser_behavior_changed` and `parserBehaviorChanged` as false-only
  protected-surface claims, not only when nested under
  `protected_surface_assertions`.
- Added focused regression coverage proving both bypasses fail closed without
  echoing caller-provided issue references.

Codex D rebound fixer update:

- Sanitized caller-controlled symbolic text before it can appear in direct
  draft group IDs, issue draft titles, source packet refs, stop reasons,
  fixture summaries, manifest summaries, review checklist IDs, or minimal
  window summaries.
- Removed caller-provided unknown scalar values and duplicate IDs from
  validation error strings.
- Added focused regression coverage for unsafe packet-report status, direct
  draft-group builder inputs, and validator unknown-value errors.

Codex D RIFDRAFT-E-003/RIFDRAFT-E-004 fixer update:

- Extended privacy and lifecycle scanning to caller-controlled mapping keys,
  not only string values.
- Redacted unsafe mapping keys from validation error paths.
- Replaced unknown false-flag map key echo with symbolic `unknown_key`
  validation errors.
- Added focused regression coverage for unsafe `context` keys and nested
  false-flag map keys.

Codex D remaining RIFDRAFT-E-003/RIFDRAFT-E-004 fixer update:

- Fixed the remaining exact private metadata value gap by treating
  caller-supplied exact offset, file-size, timestamp, hash, filesystem ID,
  inode, archive-name, and source-generation ID strings as fail-closed
  privacy violations, not symbolic evidence labels.
- Added direct forbidden-key coverage for source-generation, filesystem ID,
  inode, archive-name, and file-size key variants, including camelCase forms.
- Added focused regression coverage proving those values and keys fail closed
  without echoing caller-supplied values into draft output.

Codex D second remaining RIFDRAFT-E-003/RIFDRAFT-E-004 fixer update:

- Fixed the remaining source-action instruction gap by treating
  caller-supplied PR-opening, branch, commit, staging, tracker, merge, deploy,
  release, and production action keys as fail-closed claims unless explicitly
  false.
- Added action-instruction value scanning for caller-supplied phrases such as
  PR opening, branch creation, merge, deploy, and release instructions.
- Added focused regression coverage proving those keys and instruction values
  fail closed without echoing caller-supplied branch, commit, tracker, or
  action text.

Codex D latest RIFDRAFT-E-003/RIFDRAFT-E-004 fixer update:

- Added source packet `confidence`, `finality`, `degradation_flags`, and
  `candidate_status` to fixture draft summaries and manifest draft summaries,
  preserving the recovery candidate packet values without raising draft,
  fixture, manifest, corpus, parser, or readiness authority.
- Added a recovery-matrix field-id guard so direct group builds with malformed
  field IDs or syntactically valid but unknown field IDs route to
  `review_required` instead of `draft_ready_for_review`.
- Added exact regression coverage for source-packet review metadata
  preservation and invalid/unknown field-id review routing.

## Files Changed

- `docs/contracts/parser_recovery_issue_fixture_draft_generator.md`
  - Codex B contract source artifact, retained as part of this implementation
    package.
- `src/mythic_edge_parser/app/recovery_issue_fixture_draft_generator.py`
  - New in-memory issue/fixture draft helper and validators.
- `tests/test_recovery_issue_fixture_draft_generator.py`
  - New focused tests for the helper.
- `docs/implementation_handoffs/parser_recovery_issue_fixture_draft_generator_comparison.md`
  - This implementation handoff.

## Code Changed

Runtime code file added:

- `src/mythic_edge_parser/app/recovery_issue_fixture_draft_generator.py`

Behavior surface:

- Static, side-effect-free draft construction and validation only.
- New public helpers:
  - `build_recovery_issue_fixture_draft_report(...)`
  - `build_recovery_issue_fixture_draft_group(...)`
  - `build_recovery_issue_draft(...)`
  - `build_recovery_fixture_draft_summary(...)`
  - `build_recovery_manifest_draft_summary(...)`
  - `build_recovery_draft_review_checklist(...)`
  - `validate_recovery_issue_fixture_draft_report(...)`
  - `validate_recovery_issue_fixture_draft_group(...)`
  - `validate_recovery_issue_draft(...)`
  - `validate_recovery_fixture_draft_summary(...)`
  - `validate_recovery_manifest_draft_summary(...)`
  - `validate_recovery_draft_review_checklist(...)`

No parser runtime path imports or calls this module.

## Tests Added Or Updated

- `tests/test_recovery_issue_fixture_draft_generator.py`

The test suite covers:

- report object shape and false readiness/authorization flags;
- deterministic JSON serialization;
- `Refs`-only issue draft lifecycle wording;
- fixture and manifest summaries remaining review-only;
- review-required packets staying review-required;
- blocked-private and blocked-external packets staying blocked;
- true readiness, issue creation, PR creation, file-writing, and
  protected-surface claims failing closed;
- lifecycle action keys such as `closes`, `fixes`, and `closedBy` failing
  closed without value echo;
- direct protected-surface claim keys such as `parser_behavior_changed` and
  `parserBehaviorChanged` failing closed;
- unsafe packet-report status values being sanitized without value echo;
- direct draft-group builder inputs being sanitized before output construction;
- unsafe context keys failing closed without key echo;
- private marker handling without value echo;
- closing keyword rejection;
- direct forbidden-key validation without value echo;
- unknown validation values not echoing forbidden values;
- unknown false-flag map keys not echoing forbidden key names;
- exact private metadata values such as offsets, file sizes, timestamps,
  hashes, filesystem IDs, inodes, archive names, and source-generation IDs
  failing closed without value echo;
- direct private metadata keys failing closed;
- direct source-action instruction keys and values failing closed without
  value echo;
- source packet `confidence`, `finality`, `degradation_flags`, and
  `candidate_status` preservation in fixture and manifest summaries;
- malformed and recovery-matrix-unknown field IDs routing to
  `review_required`;
- copy safety;
- no parser runtime, file-writer, subprocess, or GitHub client imports.

## Interface Changes

Added a report-only Python helper interface:

```python
RECOVERY_ISSUE_FIXTURE_DRAFT_REPORT_OBJECT
RECOVERY_ISSUE_FIXTURE_DRAFT_SCHEMA_VERSION
RECOVERY_ISSUE_DRAFT_OBJECT
RECOVERY_FIXTURE_DRAFT_SUMMARY_OBJECT
RECOVERY_MANIFEST_DRAFT_SUMMARY_OBJECT
RECOVERY_DRAFT_REVIEW_CHECKLIST_OBJECT
build_recovery_issue_fixture_draft_report(...)
build_recovery_issue_fixture_draft_group(...)
build_recovery_issue_draft(...)
build_recovery_fixture_draft_summary(...)
build_recovery_manifest_draft_summary(...)
build_recovery_draft_review_checklist(...)
validate_recovery_issue_fixture_draft_report(...)
validate_recovery_issue_fixture_draft_group(...)
validate_recovery_issue_draft(...)
validate_recovery_fixture_draft_summary(...)
validate_recovery_manifest_draft_summary(...)
validate_recovery_draft_review_checklist(...)
```

No CLI, environment variable, workbook column, webhook payload, Apps Script,
runtime status, analytics schema, corpus metadata, fixture, golden replay
manifest, GitHub issue/PR, or parser event interface changed.

## Contracted Area Status

Implementation stayed within Quality / Governance and Corpus / Provenance
shared-support boundaries.

Parser, workbook, webhook, Apps Script, Google Sheets sync, runtime status,
diagnostics, drift, golden replay, feature-equity, evidence-ledger behavior,
analytics, AI, coaching, corpus metadata, fixture-promotion, CI, merge, deploy,
release, production, GitHub issue lifecycle, and GitHub PR lifecycle boundaries
were not touched.

False flags remain false:

```yaml
parser_behavior_ready: false
pipeline_activation_ready_for_issue_388: false
file_writing_authorized: false
private_harvest_authorized: false
fixture_promotion_authorized: false
corpus_status_change_authorized: false
issue_creation_authorized: false
pr_creation_authorized: false
field_recovery_ready: false
```

## Validation Run

Passed:

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_recovery_issue_fixture_draft_generator.py
# 23 passed in 5.63s

python3 -m pytest -q tests/test_recovery_candidate_packet_generator.py tests/test_field_recovery_matrix.py tests/test_field_evidence_comparison_report.py tests/test_recovery_issue_fixture_draft_generator.py
# 63 passed in 7.43s

python3 -m ruff check src/mythic_edge_parser/app/recovery_issue_fixture_draft_generator.py tests/test_recovery_issue_fixture_draft_generator.py
# All checks passed!

python3 -m ruff check src tests tools
# All checks passed!

python3 -m py_compile src/mythic_edge_parser/app/recovery_issue_fixture_draft_generator.py
# passed with no output

git diff --check
# passed with no output

python3 tools/check_agent_docs.py
# errors: 0, warnings: 0

printf '%s\n' docs/contracts/parser_recovery_issue_fixture_draft_generator.md src/mythic_edge_parser/app/recovery_issue_fixture_draft_generator.py tests/test_recovery_issue_fixture_draft_generator.py docs/implementation_handoffs/parser_recovery_issue_fixture_draft_generator_comparison.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
# scanned_paths: 4, forbidden: 0, warnings: 0, result: passed

printf '%s\n' docs/contracts/parser_recovery_issue_fixture_draft_generator.md src/mythic_edge_parser/app/recovery_issue_fixture_draft_generator.py tests/test_recovery_issue_fixture_draft_generator.py docs/implementation_handoffs/parser_recovery_issue_fixture_draft_generator_comparison.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
# changed_paths: 4, forbidden: 0, warnings: 0, result: passed

printf '%s\n' docs/contracts/parser_recovery_issue_fixture_draft_generator.md src/mythic_edge_parser/app/recovery_issue_fixture_draft_generator.py tests/test_recovery_issue_fixture_draft_generator.py docs/implementation_handoffs/parser_recovery_issue_fixture_draft_generator_comparison.md | python3 tools/select_validation.py --base origin/main --paths-from-stdin
# selection_status: ok; required 5, recommended 2, advisory 1

direct trailing whitespace scan over the four #455 package files
# no trailing whitespace

Codex D remaining RIFDRAFT-E-003/RIFDRAFT-E-004 repro check
# exact offset, file-size, timestamp, hash, source-generation ID, and inode
# values now return fail_closed with zero drafts and no value echo
# PR-opening, branch, commit, staging, tracker, merge, deploy, release, and
# production action keys/values now return fail_closed with zero drafts and no
# value echo
# fixture and manifest draft summaries preserve source packet confidence,
# finality, degradation_flags, and candidate_status
# direct group builds with malformed or unknown field IDs route to
# review_required instead of draft_ready_for_review

python3 -m pytest -q tests
# 1937 passed in 31.87s

python3 tools/run_pyright_advisory_report.py
# status: advisory_findings; errors: 396; tooling_config_blockers: 0; gate_behavior: advisory_non_blocking
```

The path-scoped secret/private-marker scan above passed for the four #455
package files and is the scoped validation evidence for this implementation.

## Acceptance Criteria

- Contract artifact exists and remains part of the package.
- Helper builds in-memory issue/fixture draft reports from #454 candidate
  packets.
- Helper emits no files and performs no GitHub actions.
- Helper preserves all false readiness and authorization flags.
- Helper enforces `Refs`-only lifecycle wording.
- Helper rejects direct lifecycle action keys such as `closes`, `fixes`, and
  `closedBy`.
- Helper rejects direct protected-surface claim keys unless they remain false.
- Helper sanitizes unsafe direct builder inputs before constructing public
  draft metadata.
- Helper validation errors do not echo caller-provided unknown scalar values.
- Helper fail-closes unsafe caller-provided mapping keys and redacts unsafe key
  names from validation errors.
- Helper fail-closes exact private metadata values that otherwise look like
  symbolic IDs.
- Helper fail-closes caller-supplied source-action instructions that otherwise
  looked like optional context labels.
- Helper preserves source packet `confidence`, `finality`,
  `degradation_flags`, and `candidate_status` in fixture and manifest draft
  summaries without using them as readiness authority.
- Helper routes malformed or recovery-matrix-unknown field IDs to
  `review_required`, not `draft_ready_for_review`.
- Helper fails closed on forbidden private/raw markers, local paths, exact
  offsets/sizes/timestamps/hashes, secrets, true readiness flags,
  protected-surface assertions, issue/PR creation claims, file-writing claims,
  fixture-promotion claims, corpus-status claims, and GitHub closing keywords.
- Focused tests and adjacent recovery tests pass.

## Remaining Risks

- The helper creates review-friendly text, which can be overread by a human as
  action authority if copied without review. The output preserves non-claims
  and false flags, but Codex E should scrutinize lifecycle wording.
- The helper supports only in-memory objects. Any persisted draft artifact,
  GitHub issue creation, fixture file, manifest file, metadata edit, PR assist
  action, or #456 parser/corpus update workflow still requires a separate
  contract.
- #388 and #381 remain inactive.

## Recommended Next Role

Codex E: Module Reviewer / Contract Tester.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / Contract Tester for issue #455.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/455

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/388

Parent private-evidence issue:
https://github.com/Tahjali11/Mythic-Edge/issues/434

Contract:
docs/contracts/parser_recovery_issue_fixture_draft_generator.md

Implementation handoff:
docs/implementation_handoffs/parser_recovery_issue_fixture_draft_generator_comparison.md

Scope:
Review the #455 implementation against the contract and handoff. Focus on
public-safe in-memory draft generation, Refs-only lifecycle wording, false
readiness/authorization flags, direct lifecycle-action key rejection, direct
protected-surface claim rejection, no private/raw value echo, blocked-private
and blocked-external preservation, unsafe direct-builder input sanitization,
unsafe context key fail-closed behavior, unknown validation key/value non-echo,
source packet review metadata preservation in fixture/manifest summaries,
invalid/unknown field-id review-required routing,
and no parser/runtime/GitHub/file-writing side effects.

Expected files:
- docs/contracts/parser_recovery_issue_fixture_draft_generator.md
- src/mythic_edge_parser/app/recovery_issue_fixture_draft_generator.py
- tests/test_recovery_issue_fixture_draft_generator.py
- docs/implementation_handoffs/parser_recovery_issue_fixture_draft_generator_comparison.md

Do not implement fixes unless explicitly asked. Do not activate #388 or #381.
Do not run or read private Player.log, UTC_Log, app-data, live MTGA,
diagnostics, drift, watcher, network, firewall/drop, packet, OS/router, or
private smoke checks. Do not create GitHub issues, PRs, branches, commits,
fixtures, manifests, expected-output files, corpus metadata edits, or
local/generated artifacts.

Recommended validation:
- PYTHONPATH=src python3 -m pytest -q tests/test_recovery_issue_fixture_draft_generator.py
- python3 -m pytest -q tests/test_recovery_candidate_packet_generator.py tests/test_field_recovery_matrix.py tests/test_field_evidence_comparison_report.py tests/test_recovery_issue_fixture_draft_generator.py
- python3 -m ruff check src/mythic_edge_parser/app/recovery_issue_fixture_draft_generator.py tests/test_recovery_issue_fixture_draft_generator.py
- git diff --check
- python3 tools/check_agent_docs.py
- python3 tools/check_secret_patterns.py --all
- python3 tools/check_protected_surfaces.py --base origin/main
- python3 tools/select_validation.py --base origin/main
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/455"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  parent_private_evidence_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/454"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/546"
  completed_thread: "D"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_recovery_issue_fixture_draft_generator.md"
  target_artifact: "docs/implementation_handoffs/parser_recovery_issue_fixture_draft_generator_comparison.md"
  finding_ids:
    - "RIFDRAFT-E-003"
    - "RIFDRAFT-E-004"
  verdict: "remaining_contract_mismatches_fixed_ready_for_review"
  risk_tier: "High"
  base_branch: "main"
  target_branch: "main"
  previous_merge_commit: "115e5950ce9006d97fe79af28378f16364644344"
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  private_harvest_authorized: false
  fixture_promotion_authorized: false
  corpus_status_change_authorized: false
  file_writing_authorized: false
  issue_creation_authorized: false
  pr_creation_authorized: false
```
