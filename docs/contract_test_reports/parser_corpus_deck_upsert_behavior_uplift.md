# Parser Corpus Deck Upsert Behavior Uplift Contract-Test Report

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/490

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/158

Related pipeline tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/388

Parent private-evidence gate:
https://github.com/Tahjali11/Mythic-Edge/issues/434

## Contract

`docs/contracts/parser_corpus_deck_upsert_behavior_uplift.md`

## Implementation Under Test

Branch: `codex/parser-corpus-deck-upsert-behavior-uplift-490`

Base branch: `main`

Changed artifact under review:

- `docs/contracts/parser_corpus_deck_upsert_behavior_uplift.md`

Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/488

Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/489

Previous merge commit: `73f615d59211397f8a783b3971e43b2060b6ccfa`

Prior boundary issue: https://github.com/Tahjali11/Mythic-Edge/issues/396

## Report Lifecycle

`report_lifecycle`: `final_approval`

## Contract Summary

The #490 contract decides whether `deck_api.deck_upsert` can move from
`covered_report_only` toward parser-behavior readiness. The selected path is to
preserve `covered_report_only` because current evidence is adjacent-only:
EventSetDeck, SubmitDeckResp, submitted-deck card-content provenance, StartHook,
deck-summary, deck-state, inventory, and collection evidence do not prove a
dedicated deck-upsert API parser.

## Internal Project Area Reviewed

Corpus / Provenance.

The contract preserves parser-owned truth boundaries and does not move truth to
corpus metadata, workbook formulas, dashboards, Apps Script, webhook transport,
analytics, AI, coaching, readiness, deploy, or production surfaces.

## Bridge-Code Status Reviewed

`ambiguous_pending_follow_up`

The contract explicitly routes future implementation back to Codex A/B unless a
later issue authorizes dedicated deck-upsert evidence or taxonomy reframing.

## Findings

No blocking findings.

No non-blocking contract mismatches were found.

## Checks Run

```bash
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report \
  tests/fixtures/parser_corpus/corpus_manifest.v1.json \
  --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json \
  --out /tmp/mythic_edge_issue_490_corpus_report.json
```

```bash
PYTHONPATH=src python3 -m pytest -q \
  tests/test_corpus_parity_report.py \
  tests/test_client_actions_parser.py \
  tests/test_parsers.py
```

```bash
python3 tools/check_agent_docs.py
python3 -m ruff check src tests tools
git diff --check
```

```bash
printf '%s\n' docs/contracts/parser_corpus_deck_upsert_behavior_uplift.md \
  | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
```

```bash
printf '%s\n' docs/contracts/parser_corpus_deck_upsert_behavior_uplift.md \
  | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
```

```bash
printf '%s\n' docs/contracts/parser_corpus_deck_upsert_behavior_uplift.md \
  | python3 tools/select_validation.py --base origin/main --paths-from-stdin
```

## Results

- corpus parity report: passed
- status: `partial_coverage_map_ready`
- summary: `45 families; committed=6, synthetic=16, report_only=17, blocked=6 [private=2, external=4], missing=0`
- parser_behavior_ready: `false`
- pipeline_activation_ready_for_issue_388: `false`
- `deck_api.deck_upsert`: `covered_report_only` with
  `["fixture_metadata_only"]` and `deck_upsert_boundary_report_v1`
- focused pytest: passed, 80 passed
- agent docs check: passed, errors 0, warnings 0
- Ruff: passed, all checks passed
- `git diff --check`: passed, no output
- contract-only secret/private-marker scan: passed, forbidden 0, warnings 0
- contract-only protected-surface scan: passed, forbidden 0, warnings 0
- selector sanity check: passed, `selection_status: ok`

After this report was added, Codex E reran the path-scoped package checks for
both untracked docs:

```bash
printf '%s\n' \
  docs/contracts/parser_corpus_deck_upsert_behavior_uplift.md \
  docs/contract_test_reports/parser_corpus_deck_upsert_behavior_uplift.md \
  | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
```

- passed: scanned paths 2, forbidden 0, warnings 0

```bash
printf '%s\n' \
  docs/contracts/parser_corpus_deck_upsert_behavior_uplift.md \
  docs/contract_test_reports/parser_corpus_deck_upsert_behavior_uplift.md \
  | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
```

- passed: changed paths 2, forbidden 0, warnings 0

```bash
printf '%s\n' \
  docs/contracts/parser_corpus_deck_upsert_behavior_uplift.md \
  docs/contract_test_reports/parser_corpus_deck_upsert_behavior_uplift.md \
  | python3 tools/select_validation.py --base origin/main --paths-from-stdin
```

- passed: `selection_status: ok`

```bash
python3 - <<'PY'
from pathlib import Path

paths = [
    Path("docs/contracts/parser_corpus_deck_upsert_behavior_uplift.md"),
    Path("docs/contract_test_reports/parser_corpus_deck_upsert_behavior_uplift.md"),
]
errors = []
for path in paths:
    text = path.read_text()
    for idx, line in enumerate(text.splitlines(), 1):
        if line.rstrip() != line:
            errors.append(f"{path}:{idx}: trailing whitespace")
    if not text.endswith("\n"):
        errors.append(f"{path}: missing final newline")
if errors:
    print("\n".join(errors))
    raise SystemExit(1)
print("whitespace check passed for untracked docs")
PY
```

- passed: whitespace check passed for untracked docs

## Finding Lifecycle Summary

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| none | none | `final_approval` | no findings | not_blocking | no mismatch found | focused validation passed | F |

## Confirmed Contract Matches

- The contract preserves #396's `deck_api.deck_upsert` report-only boundary.
- The contract does not authorize status movement for `deck_api.deck_upsert`.
- The contract does not authorize `parser_behavior_verified`.
- The contract does not reclassify EventSetDeck, SubmitDeckResp,
  submitted-deck cards, StartHook, deck-summary, deck-state, inventory, or
  collection evidence as deck-upsert behavior.
- The contract does not authorize fixture, manifest, session-ledger, parser,
  workbook, webhook, Apps Script, analytics, AI, coaching, readiness, or
  production changes.
- The contract preserves #388/#381 activation gates.

## Contract Mismatches

None found.

## Missing Tests

None blocking. This is a contract-only planning slice, so no implementation
tests are required in #490.

## Drift Notes

No repo, workbook, deployment, local-data, issue lifecycle, PR lifecycle, or
tracker drift was found during this review.

Current git status before final package checks showed only the contract artifact
as untracked.

## Recommendation

Approve for Codex F module submission as a contract/report-only package.

Do not route to Codex C. No implementation is authorized by this contract.

## Next Workflow Action

Next role: Codex F: Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #490.

Review and submit the contract-only package for
deck_api.deck_upsert behavior uplift planning:

- docs/contracts/parser_corpus_deck_upsert_behavior_uplift.md
- docs/contract_test_reports/parser_corpus_deck_upsert_behavior_uplift.md

Do not stage unrelated files. Do not target main directly unless explicitly
approved by the active workflow. Do not promote deck_api.deck_upsert or add
parser_behavior_verified. Do not activate #388 or #381. Do not claim dedicated
deck-upsert API support, parser support, readiness, production behavior,
analytics truth, AI truth, coaching truth, full corpus parity, or tracker
completion.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/490"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  related_pipeline_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  parent_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/488"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/489"
  previous_merge_commit: "73f615d59211397f8a783b3971e43b2060b6ccfa"
  prior_boundary_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/396"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contracts/parser_corpus_deck_upsert_behavior_uplift.md"
  target_artifact: "docs/contract_test_reports/parser_corpus_deck_upsert_behavior_uplift.md"
  verdict: "ready_for_module_submitter"
  risk_tier: "High"
  branch: "codex/parser-corpus-deck-upsert-behavior-uplift-490"
  base_branch: "main"
  selected_family: "deck_api.deck_upsert"
  current_status: "covered_report_only"
  selected_path: "preserve_report_only_dedicated_deck_upsert_evidence_or_taxonomy_reframe_required_before_behavior_uplift"
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  validation:
    - "PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json --out /tmp/mythic_edge_issue_490_corpus_report.json"
    - "PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_client_actions_parser.py tests/test_parsers.py"
    - "python3 tools/check_agent_docs.py"
    - "python3 -m ruff check src tests tools"
    - "git diff --check"
    - "path-scoped secret/private-marker scan passed"
    - "path-scoped protected-surface gate passed"
    - "path-scoped validation selector passed"
  stop_conditions:
    - "Do not target main directly unless explicitly approved."
    - "Do not close tracker #158, pipeline tracker #388, parent issue #434, or issue #490."
    - "Do not activate #388 or #381."
    - "Do not promote deck_api.deck_upsert or add parser_behavior_verified from adjacent evidence."
    - "Do not claim dedicated deck-upsert API support, parser support, readiness, production behavior, analytics truth, AI truth, coaching truth, full corpus parity, or tracker completion."
```
