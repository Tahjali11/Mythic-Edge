# Parser Evidence Golden Replay Fixture Manifest Drafts Implementation Handoff

## Context

- Repository: `Tahjali11/Mythic-Edge`
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/385
- Pipeline tracker: https://github.com/Tahjali11/Mythic-Edge/issues/388
- Parent private-evidence issue: https://github.com/Tahjali11/Mythic-Edge/issues/434
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/386
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/530
- Previous merge commit: `b11351e99b025486be442c0c49a67b13288ac3d9`
- Source contract: `docs/contracts/parser_evidence_golden_replay_fixture_manifest_drafts.md`
- Risk tier: High

The contract artifact still records its original Codex B planning-only posture.
This implementation relied on the later issue #385 lifecycle handoff that
explicitly authorized a synthetic-only, in-memory Codex C builder while keeping
file writing, private harvest, fixture promotion, corpus status changes, and
pipeline activation unauthorized.

## Comparison Summary

Confirmed matches before editing:

- Local `main` and `origin/main` were at
  `b11351e99b025486be442c0c49a67b13288ac3d9`.
- The repository remote matched `https://github.com/Tahjali11/Mythic-Edge.git`.
- Issue #386 was complete through PR #530.
- Issue #385 authorized only synthetic/in-memory draft construction.
- Existing #383, #384, and #386 builders already provided in-memory review
  packet, proof, and metadata-diff objects.
- No existing #385 draft builder module or focused tests existed.

Contract mismatches fixed:

- Added a deterministic packet builder for golden replay fixture and manifest
  draft objects.
- Added draft object identities, schema versions, status vocabulary handling,
  provenance links, false readiness flags, false authorization flags, review
  gates, privacy summary, minimization summary, expected-section boundaries,
  and explicit non-claims.
- Added fail-closed behavior for missing upstream review/proof/diff/preview
  inputs, malformed corpus/session schema, blocked source classes, forbidden
  private values, overclaims, oversized windows, ambiguous windows, and
  multi-family windows.
- Codex D follow-up for `GRDRAFT-E-001` tightened proposed draft path and parser
  expected-preview reference handling so repo-relative private/generated/runtime
  artifact references return `blocked_privacy` instead of being accepted into a
  draft packet.
- Second Codex D follow-up for `GRDRAFT-E-001` fixed the remaining semantic
  privacy gap: account IDs, display names, opponent identifiers, machine names,
  local user names, source paths, deck names/IDs, decklists, and private session
  timestamp fields now fail closed as `blocked_privacy` when populated.
- Third Codex D follow-up for `GRDRAFT-E-001` fixed the strategy-note variant:
  generic strategy notes, sideboarding notes, and card-choice fields now fail
  closed as `blocked_privacy` when populated.
- Fourth Codex D follow-up for `GRDRAFT-E-001` fixed the remaining generic-note
  privacy variant: generic `note`, `notes`, and `comment` fields carrying
  private-note, strategy-note, sideboarding-note, or sideboard-plan language now
  fail closed as `blocked_privacy`, while public review-only notes remain
  allowed.
- Fifth Codex D follow-up for `GRDRAFT-E-001` fixed the card-choice-note variant:
  generic note/comment fields carrying `card choice note` or `card choices note`
  language now fail closed as `blocked_privacy`, without treating public
  non-claim prose that merely says card choices are not included as private.
- Sixth Codex D follow-up for `GRDRAFT-E-001` fixed the card-choice colon
  variant: generic note/comment fields carrying `card choice:`, `card choices:`,
  or `card-choice:` label-style language now fail closed as `blocked_privacy`,
  while public non-claim prose that only says card choices are excluded remains
  accepted.
- Added focused tests proving public-safe ready output, deterministic behavior,
  input immutability, privacy blocking without value echo, authorization
  blocking, overclaim blocking, parser-preview boundaries, and fixture-window
  refusal statuses, including forbidden reference-path and semantic private-field
  blocking.

Still intentionally open:

- The builder does not write fixture files, manifest files, expected-output
  files, proof files, metadata diff files, fixture-promotion packets, local
  artifacts, corpus manifest entries, or session ledger entries.
- The builder does not run golden replay, corpus parity, diagnostics, drift,
  private evidence, live MTGA, network, firewall, or private smoke checks.
- The builder does not authorize parser behavior readiness, #388 activation,
  #381 activation, fixture promotion, corpus status movement, release
  readiness, production behavior, analytics truth, AI truth, or coaching truth.

## Files Changed

- `docs/contracts/parser_evidence_golden_replay_fixture_manifest_drafts.md`
  - Present from the Codex B contract pass and retained as the source artifact.
- `src/mythic_edge_parser/app/golden_replay_fixture_manifest_drafts.py`
  - New synthetic-only in-memory draft packet builder.
- `tests/test_golden_replay_fixture_manifest_drafts.py`
  - New focused tests for the #385 builder.
- `docs/implementation_handoffs/parser_evidence_golden_replay_fixture_manifest_drafts_comparison.md`
  - This implementation handoff.

## Validation Run

- `PYTHONPATH=src python3 -m pytest -q tests/test_golden_replay_fixture_manifest_drafts.py`
  - Passed: 12 tests.
- `PYTHONPATH=src python3 -m pytest -q tests/test_fixture_promotion_proof.py tests/test_corpus_metadata_diff_generator.py tests/test_golden_replay_fixture_manifest_drafts.py`
  - Passed: 36 tests.
- `python3 -m json.tool tests/fixtures/parser_corpus/corpus_manifest.v1.json >/dev/null`
  - Passed.
- `python3 -m json.tool tests/fixtures/parser_corpus/session_ledger.v1.json >/dev/null`
  - Passed.
- `PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json`
  - Passed with `partial_coverage_map_ready`.
- `python3 tools/check_agent_docs.py`
  - Passed.
- `python3 -m ruff check src tests tools`
  - Passed.
- `git diff --check`
  - Passed.
- Direct trailing-whitespace scan against the changed path set.
  - Passed.
- Path-scoped secret/private-marker scan for the changed path set.
  - Passed.
- Path-scoped protected-surface gate for the changed path set.
  - Passed.
- Path-scoped validation selector for the changed path set.
  - Passed with required focused checks satisfied.
- `python3 -m pytest -q tests`
  - Passed: 1853 tests.
- `python3 tools/run_pyright_advisory_report.py`
  - Ran in advisory mode. Reported existing type findings with
    `gate_behavior: advisory_non_blocking`.

## Remaining Risks And Non-Claims

- This implementation depends on synthetic in-memory objects supplied by prior
  pipeline steps; it does not prove a real fixture can or should be committed.
- The draft packet is review material only. It is not parser truth, golden
  replay pass evidence, fixture-promotion authority, metadata mutation
  authority, private-evidence approval, or a readiness gate.
- Existing parser behavior, golden replay behavior, corpus metadata, and
  protected runtime/workbook/webhook/App Script/analytics/AI/coaching surfaces
  were not changed.
- The contract text includes older planning-only language, so Codex E should
  verify the later issue #385 lifecycle handoff remains the accepted authority
  for this Codex C implementation.

## Recommended Next Role

Codex E: Module Reviewer. Review the synthetic-only builder and tests for
contract alignment, privacy/non-claim boundaries, fail-closed statuses,
determinism, absence of side effects, and protected-surface containment.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer for issue #385.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/385

Pipeline tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/388

Parent private-evidence issue:
https://github.com/Tahjali11/Mythic-Edge/issues/434

Previous issue:
https://github.com/Tahjali11/Mythic-Edge/issues/386

Previous PR:
https://github.com/Tahjali11/Mythic-Edge/pull/530

Previous merge commit:
b11351e99b025486be442c0c49a67b13288ac3d9

Source contract:
docs/contracts/parser_evidence_golden_replay_fixture_manifest_drafts.md

Implementation handoff:
docs/implementation_handoffs/parser_evidence_golden_replay_fixture_manifest_drafts_comparison.md

Review scope:
- src/mythic_edge_parser/app/golden_replay_fixture_manifest_drafts.py
- tests/test_golden_replay_fixture_manifest_drafts.py
- docs/contracts/parser_evidence_golden_replay_fixture_manifest_drafts.md
- docs/implementation_handoffs/parser_evidence_golden_replay_fixture_manifest_drafts_comparison.md

Goal:
Review the synthetic-only, in-memory golden replay fixture/manifest draft packet
builder for contract alignment and boundary safety. Confirm it remains a
review-only object builder and does not become fixture writing, manifest
writing, expected-output truth, fixture-promotion authority, corpus metadata
mutation, private-evidence approval, parser behavior readiness, #388/#381
activation, release readiness, analytics truth, AI truth, or coaching truth.

Review focus:
- Codex D fixed `GRDRAFT-E-001`: proposed draft paths and parser expected-preview
  source references that point at private/generated/runtime artifacts now fail
  closed as `blocked_privacy` without echoing the value.
- Codex D also fixed the remaining semantic privacy reproduction: populated
  account/display/opponent/machine/local-user/source/deck/private-session fields
  now fail closed as `blocked_privacy` without echoing the value.
- Codex D also fixed the later strategy-note reproduction: populated
  strategy-note, sideboarding-note, and card-choice fields now fail closed as
  `blocked_privacy` without echoing the value.
- Codex D also fixed the later generic-note reproduction: generic note/comment
  fields containing private-note, strategy-note, sideboarding-note, or
  sideboard-plan language now fail closed as `blocked_privacy` without echoing
  the value, while public review-only notes remain accepted.
- Codex D also fixed the later card-choice-note reproduction: generic
  note/comment fields containing `card choice note` or `card choices note`
  language now fail closed as `blocked_privacy`, while public non-claim prose
  about card choices remaining excluded stays accepted.
- Codex D also fixed the later card-choice colon reproduction: generic
  note/comment fields containing `card choice:`, `card choices:`, or
  `card-choice:` label-style language now fail closed as `blocked_privacy`,
  while public non-claim prose about card choices remaining excluded stays
  accepted.
- The later issue #385 lifecycle handoff authorized Codex C implementation
  even though the original Codex B contract text says implementation was not
  authorized.
- Output shape uses the contracted packet, fixture draft, and manifest draft
  object/schema identities.
- All readiness and authorization flags remain false.
- Missing or malformed upstream review/proof/diff/preview inputs fail closed.
- Private/raw/local/secrets values are blocked without echoing values.
- Blocked private/external source classes return blocked authorization.
- Overclaim attempts return blocked overclaim.
- Expected manifest draft sections are limited to parser-owned golden replay
  sections.
- Fixture-window minimization and refusal statuses are deterministic.
- The builder is side-effect free and does not mutate inputs.
- Existing parser, golden replay, corpus metadata, runtime, workbook, webhook,
  Apps Script, analytics, AI, and coaching behavior are unchanged.

Validation:
- PYTHONPATH=src python3 -m pytest -q tests/test_golden_replay_fixture_manifest_drafts.py
- PYTHONPATH=src python3 -m pytest -q tests/test_fixture_promotion_proof.py tests/test_corpus_metadata_diff_generator.py tests/test_golden_replay_fixture_manifest_drafts.py
- python3 -m json.tool tests/fixtures/parser_corpus/corpus_manifest.v1.json >/dev/null
- python3 -m json.tool tests/fixtures/parser_corpus/session_ledger.v1.json >/dev/null
- PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
- python3 tools/check_agent_docs.py
- python3 -m ruff check src tests tools
- git diff --check
- path-scoped secret/private-marker scan for changed files
- path-scoped protected-surface gate for changed files
- path-scoped validation selector for changed files
- python3 -m pytest -q tests
- python3 tools/run_pyright_advisory_report.py

Do not:
- Close issue #385, #388, #381, or #434.
- Stage, commit, push, or open a PR unless explicitly asked.
- Run private/live Player.log, UTC_Log, app-data, live MTGA, network,
  firewall, packet, OS/router, diagnostics, drift, or private smoke checks.
- Write fixture files, manifest files, expected-output files, proof files,
  metadata diff files, fixture-promotion packets, local artifacts, corpus
  manifest entries, or session ledger entries.
- Claim parser behavior readiness, pipeline activation readiness, release
  readiness, production behavior, analytics truth, AI truth, coaching truth,
  or full parser regression parity.
```

## Workflow Handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/385"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/386"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/530"
  parent_private_evidence_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  completed_thread: "D"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_evidence_golden_replay_fixture_manifest_drafts.md"
  target_artifact: "src/mythic_edge_parser/app/golden_replay_fixture_manifest_drafts.py; tests/test_golden_replay_fixture_manifest_drafts.py; docs/implementation_handoffs/parser_evidence_golden_replay_fixture_manifest_drafts_comparison.md"
  finding_id: "GRDRAFT-E-001"
  verdict: "golden_replay_fixture_manifest_draft_card_choice_colon_privacy_fix_ready_for_review"
  risk_tier: "High"
  base_branch: "main"
  target_branch: "main"
  previous_merge_commit: "b11351e99b025486be442c0c49a67b13288ac3d9"
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  implementation_authorized: true
  implementation_scope: "synthetic_only_in_memory_golden_replay_fixture_manifest_draft_builder"
  file_writing_authorized: false
  private_harvest_authorized: false
  fixture_promotion_authorized: false
  corpus_status_change_authorized: false
```
