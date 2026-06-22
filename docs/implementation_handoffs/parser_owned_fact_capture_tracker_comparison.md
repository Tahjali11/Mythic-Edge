# Parser-Owned Fact Capture Tracker Implementation Handoff

## Role

Codex C: Module Implementer for issue #481.

## Source Artifact

- Contract: `docs/contracts/parser_owned_fact_capture_tracker.md`
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/481
- Pipeline tracker: https://github.com/Tahjali11/Mythic-Edge/issues/388
- Parent private-evidence issue: https://github.com/Tahjali11/Mythic-Edge/issues/434

## Comparison Summary

The contract requested a metadata-only parser-owned fact capture tracker with
three deterministic object surfaces:

- parser-owned fact target matrix;
- session capture ledger;
- coverage progress report.

The implementation adds those builders and validators in
`parser_owned_fact_tracker.py`. The module seeds target rows from the existing
field recovery matrix, preserves the required false readiness and
authorization flags, keeps blocked/private/external rows visible as blocked,
and keeps analytics/deck-state rows out of parser-truth promotion.

No parser behavior, router behavior, corpus metadata, fixture manifests,
runtime behavior, workbook/webhook/App Script behavior, analytics behavior,
AI/model-provider behavior, CI policy, merge policy, or production behavior
was changed.

## Files Changed

- `src/mythic_edge_parser/app/parser_owned_fact_tracker.py`
- `tests/test_parser_owned_fact_tracker.py`
- `docs/implementation_handoffs/parser_owned_fact_capture_tracker_comparison.md`

The existing contract file
`docs/contracts/parser_owned_fact_capture_tracker.md` remains untracked from
the prior contract-writer pass and was used as the implementation source.

## Implementation Details

Added module constants and validators for:

- `mythic_edge_parser_owned_fact_target_matrix`
- `parser_owned_fact_target_matrix.v1`
- `mythic_edge_parser_owned_fact_session_capture_ledger`
- `parser_owned_fact_session_capture_ledger.v1`
- `mythic_edge_parser_owned_fact_coverage_progress_report`
- `parser_owned_fact_coverage_progress_report.v1`

Added deterministic builders:

- `build_default_fact_target_matrix(...)`
- `build_empty_session_capture_ledger(...)`
- `record_capture_session(matrix, ledger, session_record)`
- `build_coverage_progress_report(matrix, ledger, *, previous_report=None)`

Added public-safe validators:

- `validate_fact_target_matrix(matrix)`
- `validate_fact_row(row)`
- `validate_session_capture_ledger(ledger)`
- `validate_session_entry(session, *, matrix=None, ledger=None)`
- `validate_coverage_progress_report(report)`

The validator layer fails closed for unsupported object/schema values,
readiness or authorization overclaims, forbidden lifecycle jumps, forbidden
private markers, raw/private key names, privacy findings, and cross-platform
confirmation without both Windows and macOS confirmation.

## Tests Added

`tests/test_parser_owned_fact_tracker.py` covers:

- target matrix shape, source refs, summary, false flags, and non-claims;
- representative scope boundaries for direct, analytics, deck-state,
  private-evidence, and external-boundary rows;
- sanitized privacy failure output without echoing a local path marker;
- private capture ledger append behavior;
- forbidden lifecycle skip rejection;
- private source kind requiring private or blocked deltas;
- progress report summaries for captures, candidates, deferred rows, and
  blocked rows;
- cross-platform confirmation guard;
- report-level readiness and parser-behavior overclaim rejection;
- copy-safe object construction.

## Codex D Fixer Update

Codex D addressed `POFACT-E-001`, the reference-gated lifecycle blocker.
Fact rows and session deltas now fail closed when a gated lifecycle status is
claimed without the corresponding public-safe symbolic reference:

- `candidate_generated` requires candidate refs;
- `review_packet_created` and `human_approved` require review or reviewer
  decision refs;
- `promotion_proof_ready` requires proof refs;
- `fixture_manifest_draft_ready` requires draft refs;
- `promoted_golden_fixture` and platform confirmation statuses require
  promoted fixture refs.

The fix is limited to metadata-only validator behavior and focused tests. It
does not read private logs, run private harvest, create fixtures, edit corpus
metadata, activate #388/#381, change parser behavior, or change any workbook,
webhook, App Script, analytics, AI, coaching, runtime, or production behavior.

## Validation Run

Passed:

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_parser_owned_fact_tracker.py
PYTHONPATH=src python3 -m pytest -q tests/test_parser_owned_fact_tracker.py tests/test_field_recovery_matrix.py tests/test_local_harvest_candidate_reports.py tests/test_harvest_review_packets.py
PYTHONPATH=src python3 -m pytest -q tests/test_fixture_promotion_proof.py tests/test_corpus_metadata_diff_generator.py tests/test_golden_replay_fixture_manifest_drafts.py
PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_golden_replay_harness.py
PYTHONPATH=src python3 -m pytest -q tests
python3 -m ruff check src tests tools
python3 tools/check_agent_docs.py
printf '%s\n' docs/contracts/parser_owned_fact_capture_tracker.md src/mythic_edge_parser/app/parser_owned_fact_tracker.py tests/test_parser_owned_fact_tracker.py docs/implementation_handoffs/parser_owned_fact_capture_tracker_comparison.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' docs/contracts/parser_owned_fact_capture_tracker.md src/mythic_edge_parser/app/parser_owned_fact_tracker.py tests/test_parser_owned_fact_tracker.py docs/implementation_handoffs/parser_owned_fact_capture_tracker_comparison.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
printf '%s\n' docs/contracts/parser_owned_fact_capture_tracker.md src/mythic_edge_parser/app/parser_owned_fact_tracker.py tests/test_parser_owned_fact_tracker.py docs/implementation_handoffs/parser_owned_fact_capture_tracker_comparison.md | python3 tools/select_validation.py --base origin/main --paths-from-stdin
git diff --check
focused whitespace check over the four changed/untracked files
focused public-artifact rg scan for local paths, readiness overclaims, webhook, token, secret, and API-key markers
```

Results:

- `tests/test_parser_owned_fact_tracker.py`: 12 passed.
- Field recovery / harvest / review packet group: 50 passed.
- Fixture proof / metadata diff / golden replay draft group: 36 passed.
- Corpus parity / golden replay harness group: 22 passed.
- Full test suite: 1949 passed.
- Ruff: passed.
- Agent docs: passed.
- Path-scoped secret/private marker scan over the four slice files: passed.
- Path-scoped protected-surface gate over the four slice files: passed.
- Path-scoped validation selector over the four slice files: passed.
- `git diff --check`: passed.
- Focused public-artifact overclaim/private marker scan: passed with only the
  expected scanner vocabulary match in the new validator.
- `python3 tools/run_pyright_advisory_report.py`: completed in advisory mode
  with existing non-blocking type findings.

`python3 tools/check_secret_patterns.py --all` was also run and failed on
pre-existing repository-wide findings outside this slice. The path-scoped scan
for the four new/changed artifacts passed with `forbidden: 0` and
`warnings: 0`.

Codex D `POFACT-E-001` validation:

```bash
PYTHONPATH=src python3 -m pytest -q tests/test_parser_owned_fact_tracker.py
PYTHONPATH=src python3 -m pytest -q tests/test_parser_owned_fact_tracker.py tests/test_field_recovery_matrix.py tests/test_local_harvest_candidate_reports.py tests/test_harvest_review_packets.py
PYTHONPATH=src python3 -m pytest -q tests/test_fixture_promotion_proof.py tests/test_corpus_metadata_diff_generator.py tests/test_golden_replay_fixture_manifest_drafts.py
PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_golden_replay_harness.py
PYTHONPATH=src python3 -m pytest -q tests
python3 -m ruff check src tests tools
python3 tools/check_agent_docs.py
printf '%s\n' docs/contracts/parser_owned_fact_capture_tracker.md src/mythic_edge_parser/app/parser_owned_fact_tracker.py tests/test_parser_owned_fact_tracker.py docs/implementation_handoffs/parser_owned_fact_capture_tracker_comparison.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' docs/contracts/parser_owned_fact_capture_tracker.md src/mythic_edge_parser/app/parser_owned_fact_tracker.py tests/test_parser_owned_fact_tracker.py docs/implementation_handoffs/parser_owned_fact_capture_tracker_comparison.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
printf '%s\n' docs/contracts/parser_owned_fact_capture_tracker.md src/mythic_edge_parser/app/parser_owned_fact_tracker.py tests/test_parser_owned_fact_tracker.py docs/implementation_handoffs/parser_owned_fact_capture_tracker_comparison.md | python3 tools/select_validation.py --base origin/main --paths-from-stdin
python3 tools/run_pyright_advisory_report.py
git diff --check
focused whitespace check over the four changed/untracked files
generated cache cleanup verification
```

Results: focused tracker tests 12 passed; adjacent field recovery / harvest /
review packet group 50 passed; fixture proof / metadata diff / golden replay
draft group 36 passed; corpus parity / golden replay harness group 22 passed;
full `tests` suite 1949 passed; Ruff, agent docs, path-scoped secret/private
marker scan, path-scoped protected-surface gate, path-scoped validation selector,
and `git diff --check` passed. Pyright advisory completed with existing
non-blocking type findings.

## Remaining Risks And Non-Claims

- The default target matrix intentionally seeds only the 8 reviewed
  field-recovery rows. It does not claim complete parser-owned fact coverage.
- The tracker is metadata-only. It does not read raw logs, inspect private
  artifacts, create harvest candidates, create review packets, prove fixture
  promotion, edit corpus metadata, or activate #388/#381.
- `parser_behavior_ready=false`,
  `pipeline_activation_ready_for_issue_388=false`,
  `private_harvest_authorized=false`,
  `fixture_promotion_authorized=false`, and
  `corpus_status_change_authorized=false` remain preserved in generated
  objects.
- The module does not implement a CLI. The contract listed CLI behavior as a
  potential future surface, not required for the first pure builder/validator
  implementation.

## Recommended Next Role

Codex E: Module Reviewer. Review the implementation against
`docs/contracts/parser_owned_fact_capture_tracker.md`, run the full requested
validation set, and route to Codex D only if concrete implementation findings
are present.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer for issue #481.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/481

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/388

Parent private-evidence issue:
https://github.com/Tahjali11/Mythic-Edge/issues/434

Contract:
docs/contracts/parser_owned_fact_capture_tracker.md

Implementation handoff:
docs/implementation_handoffs/parser_owned_fact_capture_tracker_comparison.md

Goal:
Review the metadata-only parser-owned fact capture tracker implementation
against the contract. Lead with findings ordered by severity. Confirm whether
the target matrix, session capture ledger, progress report builders, validators,
tests, false readiness flags, privacy boundaries, lifecycle transitions, and
non-claims satisfy the contract.

Review scope:
- src/mythic_edge_parser/app/parser_owned_fact_tracker.py
- tests/test_parser_owned_fact_tracker.py
- docs/implementation_handoffs/parser_owned_fact_capture_tracker_comparison.md
- docs/contracts/parser_owned_fact_capture_tracker.md

Protected boundaries:
- Do not read, tail, copy, hash, normalize, summarize, upload, or commit
  private Player.log or UTC_Log content.
- Do not run private harvest, live MTGA, diagnostics, drift, watcher, tailer,
  network, firewall/drop, packet, OS/router, or private smoke checks.
- Do not create fixtures, golden replay manifests, proof files, metadata diff
  files, review packets, recovery packet files, local/generated artifacts, or
  corpus metadata edits.
- Do not edit tests/fixtures/parser_corpus/corpus_manifest.v1.json or
  tests/fixtures/parser_corpus/session_ledger.v1.json.
- Do not change parser/runtime/workbook/webhook/App Script/analytics/AI/coaching
  behavior or production behavior.
- Preserve parser_behavior_ready=false,
  pipeline_activation_ready_for_issue_388=false,
  private_harvest_authorized=false, fixture_promotion_authorized=false, and
  corpus_status_change_authorized=false.

Validation:
- PYTHONPATH=src python3 -m pytest -q tests/test_parser_owned_fact_tracker.py
- PYTHONPATH=src python3 -m pytest -q tests/test_parser_owned_fact_tracker.py tests/test_field_recovery_matrix.py tests/test_local_harvest_candidate_reports.py tests/test_harvest_review_packets.py
- PYTHONPATH=src python3 -m pytest -q tests/test_fixture_promotion_proof.py tests/test_corpus_metadata_diff_generator.py tests/test_golden_replay_fixture_manifest_drafts.py
- PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_golden_replay_harness.py
- python3 tools/check_secret_patterns.py --all
- python3 tools/check_protected_surfaces.py --base origin/main
- python3 tools/select_validation.py --base origin/main
- git diff --check

End with:
- findings first
- validation run
- remaining risk
- recommended next role
- workflow_handoff block
```

## Workflow Handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/481"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  parent_private_evidence_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/465"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/549"
  previous_merge_commit: "ace067d3491565b2825a4c2c9fa1777a9c87ce30"
  completed_thread: "D"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_owned_fact_capture_tracker.md"
  target_artifact: "src/mythic_edge_parser/app/parser_owned_fact_tracker.py; tests/test_parser_owned_fact_tracker.py; docs/implementation_handoffs/parser_owned_fact_capture_tracker_comparison.md"
  finding_id: "POFACT-E-001"
  verdict: "reference_gated_lifecycle_blocker_fixed_ready_for_review"
  risk_tier: "High"
  base_branch: "main"
  target_branch: "main"
  branch: "codex/parser-owned-fact-capture-tracker-481"
  implementation_scope: "metadata_only_parser_owned_fact_target_matrix_session_ledger_progress_report"
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  private_harvest_authorized: false
  fixture_promotion_authorized: false
  corpus_status_change_authorized: false
  implementation_authorized: true
  file_writing_authorized: false
  issue_creation_authorized: false
  pr_creation_authorized: false
  ready_for_codex_f: false
```
