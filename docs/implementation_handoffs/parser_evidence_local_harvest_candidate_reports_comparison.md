# Parser Evidence Local Harvest Candidate Reports Implementation Handoff

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/382

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/388

## Contract

`docs/contracts/parser_evidence_local_harvest_candidate_reports.md`

## Internal Project Area

Parser evidence pipeline / Corpus and Provenance.

## Truth Owner

Parser-owned truth remains with the existing parser, router, state, match/game
identity, and final reconciliation layers. The new report builder is an
advisory evidence-discovery helper only.

## Bridge-Code Status

`shared_support`

The implementation produces a local planning/report shape from supplied
synthetic in-memory inputs. It does not attach evidence to runtime, workbook,
webhook, Apps Script, analytics, AI, diagnostics, golden replay, corpus
metadata, or fixture-promotion surfaces.

## Role Performed

Codex C: Module Implementer.

## Comparison Summary

The Codex B contract was planning-only, but the latest issue comment and user
prompt explicitly activated a synthetic-only, in-memory Codex C implementation.
This implementation preserves the contract's blocked private-harvest,
fixture-promotion, and pipeline-activation boundaries.

Confirmed matches:

- Builds `mythic_edge_harvest_candidate_summary` reports with schema version
  `parser_evidence_harvest_candidate_summary.v1`.
- Requires caller-supplied synthetic/in-memory inputs.
- Supports synthetic Player.log-style summary inputs.
- Supports synthetic UTC_Log-derived metadata via the #381
  `utc_log_source_adapter.v1` normalization result.
- Preserves `parser_behavior_verified=false`,
  `corpus_status_change_authorized=false`,
  `fixture_promotion_authorized=false`,
  `private_harvest_authorized=false`, and
  `pipeline_activation_ready_for_issue_388=false`.
- Blocks private source classes with `authorization_status=missing_required`.
- Rejects forbidden raw/private summary fields without echoing the supplied
  value.
- Emits reduced parser fact preview metadata only: counts, event kind names,
  status labels, and non-claims.

Still deferred:

- File discovery, default local paths, tailing, private Player.log or UTC_Log
  reads, private pointer creation, local artifact writes, fixture creation,
  fixture promotion, corpus status changes, and #388 activation.

## Files Changed

- `src/mythic_edge_parser/app/local_harvest_candidate_reports.py`
- `tests/test_local_harvest_candidate_reports.py`
- `docs/implementation_handoffs/parser_evidence_local_harvest_candidate_reports_comparison.md`

Source artifact present but not modified by this Codex C pass:

- `docs/contracts/parser_evidence_local_harvest_candidate_reports.md`

## Code Changed

Added `src/mythic_edge_parser/app/local_harvest_candidate_reports.py`.

New public helpers:

- `parser_evidence_from_utc_log_normalization(...)`
- `build_harvest_candidate_report(...)`

Behavior surface:

- Pure deterministic report construction from supplied mappings and #381
  normalization metadata.
- No filesystem reads.
- No filesystem writes.
- No parser behavior changes.
- No corpus metadata changes.
- No runtime, workbook, webhook, Apps Script, analytics, AI, or coaching
  changes.

## Tests Added Or Updated

- Added `tests/test_local_harvest_candidate_reports.py`.

Focused coverage includes:

- deterministic synthetic Player.log-style summary reports;
- synthetic UTC_Log normalization metadata consumption;
- warning/degradation handling;
- private source class blocking;
- forbidden raw summary field rejection without value echo;
- source-label path rejection without path leakage;
- missing parser evidence staying insufficient and non-promotional.

## Interface Changes

New local Python module interface only. No CLI, environment variable,
configuration, runtime status field, corpus metadata field, workbook column,
webhook payload field, Apps Script surface, or public runtime endpoint was
added.

## Contracted Area Status

Stayed inside the activated synthetic-only in-memory report-builder scope. The
implementation did not create local harvest artifacts, parser fixtures,
fixture-promotion packets, or corpus manifest/session-ledger changes.

## Validation Run

```bash
python3 -m pytest -q tests/test_utc_log_source_adapter.py tests/test_local_harvest_candidate_reports.py
# 15 passed

python3 -m pytest -q tests
# 1797 passed

python3 tools/check_agent_docs.py
# passed

python3 -m ruff check src tests tools
# passed

git diff --check
# passed

python3 tools/run_pyright_advisory_report.py
# advisory_findings, non-blocking: 390 existing type findings

printf '%s\n' docs/contracts/parser_evidence_local_harvest_candidate_reports.md src/mythic_edge_parser/app/local_harvest_candidate_reports.py tests/test_local_harvest_candidate_reports.py docs/implementation_handoffs/parser_evidence_local_harvest_candidate_reports_comparison.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
# passed: forbidden 0, warnings 0

printf '%s\n' docs/contracts/parser_evidence_local_harvest_candidate_reports.md src/mythic_edge_parser/app/local_harvest_candidate_reports.py tests/test_local_harvest_candidate_reports.py docs/implementation_handoffs/parser_evidence_local_harvest_candidate_reports_comparison.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
# passed: forbidden 0, warnings 0

printf '%s\n' docs/contracts/parser_evidence_local_harvest_candidate_reports.md src/mythic_edge_parser/app/local_harvest_candidate_reports.py tests/test_local_harvest_candidate_reports.py docs/implementation_handoffs/parser_evidence_local_harvest_candidate_reports_comparison.md | python3 tools/select_validation.py --base origin/main --paths-from-stdin
# selection_status: ok
```

Supplemental check:

```bash
python3 - <<'PY'
from pathlib import Path
paths = [
    Path('docs/contracts/parser_evidence_local_harvest_candidate_reports.md'),
    Path('src/mythic_edge_parser/app/local_harvest_candidate_reports.py'),
    Path('tests/test_local_harvest_candidate_reports.py'),
    Path('docs/implementation_handoffs/parser_evidence_local_harvest_candidate_reports_comparison.md'),
]
errors = []
for path in paths:
    text = path.read_text(encoding='utf-8')
    for lineno, line in enumerate(text.splitlines(), start=1):
        if line.rstrip(' \t') != line:
            errors.append(f'{path}:{lineno}: trailing whitespace')
    if text and not text.endswith('\n'):
        errors.append(f'{path}: missing final newline')
if errors:
    print('\n'.join(errors))
    raise SystemExit(1)
print('new-file whitespace check passed')
PY
# passed
```

## Still Unverified

- Private/local harvest execution.
- Private Player.log and UTC_Log evidence windows.
- Any future `candidate_summary.json`, `candidate_summary.md`,
  `parser_fact_preview.json`, or `private_pointer.json` file-writing behavior.
- Fixture promotion readiness.
- Parser behavior readiness.
- #388 pipeline activation readiness.
- Release, deploy, production, analytics, AI, or coaching readiness.

## Reviewer Focus

Codex E should verify:

- no source file discovery, log tailing, default Player.log path use, or output
  artifact write behavior exists;
- report output cannot include raw log lines, raw payloads, private paths, raw
  hashes, exact offsets, generated artifacts, or private content;
- private source classes remain blocked without separate authorization;
- `parser_behavior_verified`, fixture-promotion, private-harvest, and #388
  activation flags remain false;
- UTC_Log support is metadata-only and depends on the #381 adapter boundary
  rather than reimplementing normalization;
- tests cover the contracted safety boundaries.

## Next Workflow Action

Next role: Codex E: Module Reviewer / Contract Tester.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / Contract Tester for issue #382.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/382

Pipeline tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/388

Previous issue:
https://github.com/Tahjali11/Mythic-Edge/issues/381

Previous PR:
https://github.com/Tahjali11/Mythic-Edge/pull/520

Parent private-evidence issue:
https://github.com/Tahjali11/Mythic-Edge/issues/434

Contract:
docs/contracts/parser_evidence_local_harvest_candidate_reports.md

Implementation handoff:
docs/implementation_handoffs/parser_evidence_local_harvest_candidate_reports_comparison.md

Review scope:
- src/mythic_edge_parser/app/local_harvest_candidate_reports.py
- tests/test_local_harvest_candidate_reports.py
- docs/implementation_handoffs/parser_evidence_local_harvest_candidate_reports_comparison.md
- docs/contracts/parser_evidence_local_harvest_candidate_reports.md

Goal:
Review the #382 synthetic-only in-memory local harvest candidate report builder
against the contract, issue comments, implementation handoff, and diff. Verify
that it does not read private sources, discover files, write harvest artifacts,
create fixtures, promote corpus rows, change parser behavior, or claim
pipeline/readiness truth.

Suggested validation:
- python3 -m pytest -q tests/test_utc_log_source_adapter.py tests/test_local_harvest_candidate_reports.py
- python3 tools/check_agent_docs.py
- git diff --check
- path-scoped secret/private marker scan for changed files
- path-scoped protected-surface gate for changed files
- path-scoped validation selector for changed files

Do not:
- Implement fixes unless explicitly rerouted as Codex D.
- Read or run private Player.log, UTC_Log, app-data, live MTGA, network,
  firewall/drop, packet, OS/router, diagnostics, drift, or private smoke checks.
- Discover files, tail logs, use default local Player.log paths, or write local
  harvest artifacts.
- Create fixtures or fixture-promotion packets.
- Promote blocked, report-only, private-evidence, or external-boundary rows.
- Change parser behavior, parser event classes, parser state final
  reconciliation, router semantics, match/game identity, deduplication, golden
  replay behavior, workbook schema, webhook payload shape, Apps Script behavior,
  Google Sheets sync, output transport, CI gates, merge readiness, deploy
  readiness, production behavior, analytics behavior, AI/model-provider
  behavior, coaching behavior, or final integration policy.
- Claim parser_behavior_ready, pipeline activation readiness,
  fixture-promotion readiness, release readiness, production readiness,
  analytics truth, AI truth, coaching truth, or full parser regression parity.

Expected output:
- findings first, ordered by severity;
- validation run;
- residual risks;
- next recommended role;
- workflow_handoff block.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/382"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/381"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/520"
  parent_private_evidence_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_evidence_local_harvest_candidate_reports.md"
  target_artifact: "docs/implementation_handoffs/parser_evidence_local_harvest_candidate_reports_comparison.md"
  verdict: "synthetic_only_report_builder_ready_for_review"
  risk_tier: "High"
  base_branch: "main"
  target_branch: "main"
  branch: "main"
  previous_merge_commit: "34631ed7f67702aa6d96791d74506a72b1bba24f"
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  private_harvest_authorized: false
  fixture_promotion_authorized: false
  validation:
    - "python3 -m pytest -q tests/test_utc_log_source_adapter.py tests/test_local_harvest_candidate_reports.py"
    - "python3 -m pytest -q tests"
    - "python3 tools/check_agent_docs.py"
    - "python3 -m ruff check src tests tools"
    - "git diff --check"
    - "python3 tools/run_pyright_advisory_report.py (advisory_findings, non-blocking)"
    - "path-scoped secret/private marker scan passed"
    - "path-scoped protected-surface gate passed"
    - "path-scoped validation selector passed"
  stop_conditions:
    - "Do not run or read private Player.log, UTC_Log, app-data, live MTGA, network, firewall/drop, packet, OS/router, diagnostics, drift, or private smoke checks."
    - "Do not discover files, tail logs, use default local Player.log paths, or write local harvest artifacts."
    - "Do not create fixtures or fixture-promotion packets."
    - "Do not promote blocked, report-only, private-evidence, or external-boundary rows."
    - "Do not claim parser_behavior_ready, pipeline activation readiness, fixture-promotion readiness, release readiness, production readiness, analytics truth, AI truth, coaching truth, or full parser regression parity."
```
