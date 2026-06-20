# Parser Evidence Corpus Metadata Diff Generator Implementation Handoff

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/386

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/388

Parent private-evidence issue:
https://github.com/Tahjali11/Mythic-Edge/issues/434

Previous issue:
https://github.com/Tahjali11/Mythic-Edge/issues/384

Previous PR:
https://github.com/Tahjali11/Mythic-Edge/pull/523

Previous merge commit:
`d31ebb8fa773edbd784a873c57b07f7bbbc97478`

## Contract

`docs/contracts/parser_evidence_corpus_metadata_diff_generator.md`

## Role Performed

Codex C: Module Implementer.

Codex D: Module Fixer follow-up for Codex E findings CMDIFF-E-001 and
CMDIFF-E-002.

## Comparison Summary

Before this implementation:

- #384 had a synthetic-only in-memory fixture promotion proof builder.
- #386 had a planning contract and a later Codex A lifecycle decision
  authorizing only synthetic/in-memory implementation.
- There was no corpus metadata diff builder, focused test file, or #386
  implementation handoff.

After this implementation:

- `build_corpus_metadata_diff(...)` builds deterministic
  `mythic_edge_corpus_metadata_diff` dictionaries from supplied in-memory
  #384 proof objects, current corpus manifest dictionaries, current session
  ledger dictionaries, optional public-safe proposed manifest/session entries,
  and optional public-safe diff context.
- Missing proof inputs return `insufficient_proof`.
- Malformed proof inputs return `needs_contract_update`.
- Non-ready proof inputs return `insufficient_proof`, `blocked_authorization`,
  `diff_rejected`, or `needs_contract_update` according to proof status.
- Public-safe proposed entries from a ready proof can return
  `diff_ready_for_review`.
- No proposed metadata movement returns `no_metadata_change`.
- Forbidden raw/private fields or local paths in proposed metadata or the
  promotion proof return `blocked_privacy` without echoing supplied values.
- Blocked private/external promotion attempts return `blocked_authorization`
  because they require separate authority.
- Premature `parser_behavior_verified`, unrelated family promotion, known-gap
  deletion, and truth/readiness claims are treated as overclaim blockers.
- Manifest/session schema validation, family scope, known-gap preservation,
  privacy-flag preservation, and input non-mutation are covered by tests.

## Files Changed

- `docs/contracts/parser_evidence_corpus_metadata_diff_generator.md`
- `src/mythic_edge_parser/app/corpus_metadata_diff_generator.py`
- `tests/test_corpus_metadata_diff_generator.py`
- `docs/implementation_handoffs/parser_evidence_corpus_metadata_diff_generator_comparison.md`

## Boundary Preservation

The implementation is pure and side-effect free. It does not write metadata
diff files, proof files, fixtures, fixture-promotion packets, golden replay
manifests, expected outputs, corpus manifest edits, or session ledger edits.

Every output preserves:

- `parser_behavior_ready=false`
- `pipeline_activation_ready_for_issue_388=false`
- `file_writing_authorized=false`
- `private_harvest_authorized=false`
- `fixture_promotion_authorized=false`
- `corpus_status_change_authorized=false`

No parser behavior, parser event classes, router semantics, parser state final
reconciliation, match/game identity, deduplication, diagnostics, drift, golden
replay behavior, feature-equity behavior, workbook schema, webhook payload
shape, Apps Script behavior, Google Sheets sync, output transport, analytics
behavior, AI/model-provider behavior, coaching behavior, CI gates, merge
readiness, deploy readiness, production behavior, or final integration policy
changed.

## Codex D Fixer Addendum

Codex E reported two blocking mismatches:

- CMDIFF-E-001: `promotion_proof` raw/private fields were not scanned and did
  not block as `blocked_privacy`.
- CMDIFF-E-002: blocked-private/external promotion attempts returned
  `blocked_overclaim` instead of `blocked_authorization`.

The fixer pass resolved both without adding file writes or changing corpus
metadata:

- `promotion_proof` is now scanned with the same privacy boundary as proposed
  metadata, so forbidden raw/private proof fields return `blocked_privacy`
  without echoing supplied values.
- Blocked-private and blocked-external status movement now records
  authorization reasons and returns `blocked_authorization`.
- Focused regression tests cover proof-level raw/private data and both
  blocked-private and blocked-external promotion attempts.

No `docs/contract_test_reports/parser_evidence_corpus_metadata_diff_generator.md`
file was present on this branch during the fixer pass; this handoff records the
Codex E finding resolution and validation evidence.

## Validation Run

```bash
python3 -m pytest -q tests/test_corpus_metadata_diff_generator.py
# Passed: 14 tests.

python3 -m pytest -q tests/test_fixture_promotion_proof.py tests/test_corpus_metadata_diff_generator.py
# Passed: 24 tests.

python3 -m pytest -q tests/test_local_harvest_candidate_reports.py tests/test_harvest_review_packets.py tests/test_fixture_promotion_proof.py tests/test_corpus_metadata_diff_generator.py
# Passed: 51 tests.

python3 -m json.tool tests/fixtures/parser_corpus/corpus_manifest.v1.json >/dev/null
# Passed.

python3 -m json.tool tests/fixtures/parser_corpus/session_ledger.v1.json >/dev/null
# Passed.

PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
# Passed observational validation:
# partial_coverage_map_ready (45 families; committed=6, synthetic=22,
# report_only=11, blocked=6 [private=2, external=4], missing=0,
# parser_behavior_ready=no).

python3 tools/check_agent_docs.py
# Passed: errors=0, warnings=0.

python3 -m pytest -q tests
# Passed: 1841 tests.

python3 -m ruff check src tests tools
# Passed.

git diff --check
# Passed.

for path in docs/contracts/parser_evidence_corpus_metadata_diff_generator.md src/mythic_edge_parser/app/corpus_metadata_diff_generator.py tests/test_corpus_metadata_diff_generator.py docs/implementation_handoffs/parser_evidence_corpus_metadata_diff_generator_comparison.md; do output="$(/usr/bin/git diff --no-index --check /dev/null "$path" 2>&1)"; code=$?; if [ "$code" -gt 1 ]; then printf '%s\n' "$output"; exit "$code"; fi; done
# Passed. Untracked-file whitespace check clean.

printf '%s\n' docs/contracts/parser_evidence_corpus_metadata_diff_generator.md src/mythic_edge_parser/app/corpus_metadata_diff_generator.py tests/test_corpus_metadata_diff_generator.py docs/implementation_handoffs/parser_evidence_corpus_metadata_diff_generator_comparison.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
# Passed. scanned_paths=4; forbidden=0; warnings=0.

printf '%s\n' docs/contracts/parser_evidence_corpus_metadata_diff_generator.md src/mythic_edge_parser/app/corpus_metadata_diff_generator.py tests/test_corpus_metadata_diff_generator.py docs/implementation_handoffs/parser_evidence_corpus_metadata_diff_generator_comparison.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
# Passed. changed_paths=4; forbidden=0; warnings=0.

printf '%s\n' docs/contracts/parser_evidence_corpus_metadata_diff_generator.md src/mythic_edge_parser/app/corpus_metadata_diff_generator.py tests/test_corpus_metadata_diff_generator.py docs/implementation_handoffs/parser_evidence_corpus_metadata_diff_generator_comparison.md | python3 tools/select_validation.py --base origin/main --paths-from-stdin
# Passed. selection_status=ok.

python3 tools/run_pyright_advisory_report.py
# Completed in advisory mode. status=advisory_findings; gate_behavior=advisory_non_blocking.
# Current advisory findings: 394 type findings.
```

## Remaining Risks And Non-Claims

- This is not corpus metadata mutation authority.
- This is not fixture-promotion authorization.
- This is not metadata diff file-writing authorization.
- This is not private harvest authorization.
- This is not parser behavior readiness.
- This is not #388 or #381 activation.
- This does not prove private smoke success, release readiness, production
  behavior, analytics truth, AI truth, coaching truth, or full parser
  regression parity.

## Recommended Next Role

Codex E: Module Reviewer.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer for issue #386.

Repository:
Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/386

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/388

Parent private-evidence issue:
https://github.com/Tahjali11/Mythic-Edge/issues/434

Source contract:
docs/contracts/parser_evidence_corpus_metadata_diff_generator.md

Implementation handoff:
docs/implementation_handoffs/parser_evidence_corpus_metadata_diff_generator_comparison.md

Goal:
Review the #386 synthetic-only in-memory corpus metadata diff object builder
against the contract and implementation handoff.

Review:
- src/mythic_edge_parser/app/corpus_metadata_diff_generator.py
- tests/test_corpus_metadata_diff_generator.py
- docs/contracts/parser_evidence_corpus_metadata_diff_generator.md
- docs/implementation_handoffs/parser_evidence_corpus_metadata_diff_generator_comparison.md

Focus:
- Contract compliance for proof consumption and diff-status mapping.
- No file writing, fixture writing, metadata mutation, or pipeline activation.
- Preservation of all false readiness and authorization flags.
- Privacy blocking without value echo.
- Authorization handling for blocked-private/external promotion attempts.
- Anti-overclaim handling for parser_behavior_verified, unrelated families,
  known-gap deletion, and readiness/truth claims.
- Compatibility with #384 fixture promotion proof outputs.
- Test coverage for missing/malformed/non-ready proof, ready proof with
  public-safe entries, no metadata movement, invalid manifest/session schema,
  input immutability, and non-claim preservation.

Do not:
- Target main directly.
- Close #386, #388, or #434.
- Edit corpus_manifest.v1.json or session_ledger.v1.json.
- Create metadata diff files, fixtures, fixture-promotion packets, proof
  files, golden replay manifests, or expected outputs.
- Run or read private Player.log, UTC_Log, app-data, live MTGA, network,
  firewall/drop, packet, OS/router, diagnostics, drift, or private smoke
  checks.
- Claim parser_behavior_ready, #388 activation readiness, fixture-promotion
  readiness, release readiness, production readiness, analytics truth, AI
  truth, coaching truth, or full parser regression parity.

Suggested validation:
- python3 -m pytest -q tests/test_fixture_promotion_proof.py tests/test_corpus_metadata_diff_generator.py
- python3 -m pytest -q tests/test_local_harvest_candidate_reports.py tests/test_harvest_review_packets.py tests/test_fixture_promotion_proof.py tests/test_corpus_metadata_diff_generator.py
- python3 -m json.tool tests/fixtures/parser_corpus/corpus_manifest.v1.json >/dev/null
- python3 -m json.tool tests/fixtures/parser_corpus/session_ledger.v1.json >/dev/null
- PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
- python3 tools/check_agent_docs.py
- python3 -m ruff check src tests tools
- git diff --check
- path-scoped secret/private-marker scan for changed files
- path-scoped protected-surface scan for changed files
- path-scoped validation selector for changed files

End with:
- findings first, ordered by severity
- validation run
- remaining risks/non-claims
- recommended next role
- workflow_handoff block
```

## workflow_handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/386"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/384"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/523"
  parent_private_evidence_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  completed_thread: "D"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_evidence_corpus_metadata_diff_generator.md"
  target_artifact: "docs/implementation_handoffs/parser_evidence_corpus_metadata_diff_generator_comparison.md"
  verdict: "synthetic_only_in_memory_corpus_metadata_diff_builder_ready_for_review_after_d_fixer"
  risk_tier: "High"
  base_branch: "main"
  implementation_branch: "codex/parser-evidence-corpus-metadata-diff-386"
  previous_merge_commit: "d31ebb8fa773edbd784a873c57b07f7bbbc97478"
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  file_writing_authorized: false
  private_harvest_authorized: false
  fixture_promotion_authorized: false
  corpus_status_change_authorized: false
```
