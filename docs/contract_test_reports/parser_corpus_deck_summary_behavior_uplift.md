# Parser Corpus Deck Summary Behavior Uplift Contract-Test Report

## Metadata

- issue: https://github.com/Tahjali11/Mythic-Edge/issues/488
- tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
- related_pipeline_tracker: https://github.com/Tahjali11/Mythic-Edge/issues/388
- parent_issue: https://github.com/Tahjali11/Mythic-Edge/issues/434
- previous_issue: https://github.com/Tahjali11/Mythic-Edge/issues/482
- previous_pr: https://github.com/Tahjali11/Mythic-Edge/pull/487
- previous_merge_commit: `a046b4550aae18a07a61cd8222ac2927ea930b6e`
- prior_boundary_issue: https://github.com/Tahjali11/Mythic-Edge/issues/394
- related_start_hook_issue: https://github.com/Tahjali11/Mythic-Edge/issues/392
- contract: `docs/contracts/parser_corpus_deck_summary_behavior_uplift.md`
- branch: `codex/parser-corpus-deck-summary-behavior-uplift-488`
- base_branch: `main`
- selected_family: `deck_api.deck_summary`
- current_status: `covered_report_only`
- risk_tier: High

## Findings

No blocking findings.

No non-blocking contract mismatches were found.

## Contract-Test Verdict

Pass. The #488 contract preserves `deck_api.deck_summary` as
`covered_report_only` and explicitly rejects adding `parser_behavior_verified`
from the existing StartHook `DeckSummaries` evidence.

The contract correctly keeps #392 StartHook behavior evidence owned by
`deck_api.start_hook_deck_snapshot`, keeps #394 deck-summary coverage as a
report-only boundary, and requires either a future taxonomy split or distinct
standalone deck-summary parser evidence before any behavior uplift can proceed.

The contract does not authorize fixture changes, golden replay changes, corpus
manifest or session-ledger status changes, parser behavior changes, workbook or
webhook changes, Apps Script changes, analytics or AI truth changes, production
changes, tracker closure, or #388/#381 activation.

## Contract Matches

- `deck_api.deck_summary` remains `covered_report_only`.
- Current basis remains exactly `fixture_metadata_only`.
- Existing StartHook `DeckSummaries` evidence is not double-counted as
  standalone deck-summary parser behavior.
- `deck_api.start_hook_deck_snapshot` remains the bounded synthetic behavior
  row for StartHook deck snapshot evidence.
- Future uplift prerequisites are explicit:
  - taxonomy split for StartHook-bound deck-summary view versus standalone
    deck-summary API; or
  - distinct standalone parser-owned deck-summary evidence under a later
    contract.
- Required non-claims cover standalone deck-summary API support, deck identity,
  submitted-deck truth, active-deck truth, sideboard-delta truth,
  inventory/economy truth, analytics truth, AI truth, coaching truth, release
  readiness, production behavior, full corpus parity, tracker completion, and
  #388/#381 activation.

## Contract Mismatches

None found.

## Missing Tests Or Safeguards

No blocking gaps. This is a contract-only planning slice, so no implementation
tests are required in #488.

Recommended future implementation remains gated behind a new Codex A/B issue if
the project chooses taxonomy split or dedicated standalone evidence.

## Validation Run

```bash
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report \
  tests/fixtures/parser_corpus/corpus_manifest.v1.json \
  --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json \
  --out /tmp/mythic_edge_issue_488_corpus_report.json
```

- passed
- status: `partial_coverage_map_ready`
- summary: `45 families; committed=6, synthetic=16, report_only=17, blocked=6 [private=2, external=4], missing=0`
- parser_behavior_ready: `false`
- pipeline_activation_ready_for_issue_388: `false`
- `deck_api.deck_summary`: `covered_report_only` with
  `["fixture_metadata_only"]` and `deck_summary_boundary_report_v1`

```bash
PYTHONPATH=src python3 -m pytest -q \
  tests/test_corpus_parity_report.py \
  tests/test_collection_parser.py \
  tests/test_event_schema_snapshots.py
```

- passed: 21 passed

```bash
python3 tools/check_agent_docs.py
```

- passed: errors 0, warnings 0

```bash
python3 -m ruff check src tests tools
```

- passed: all checks passed

```bash
git diff --check
```

- passed: no output

```bash
printf '%s\n' docs/contracts/parser_corpus_deck_summary_behavior_uplift.md \
  | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
```

- passed: scanned paths 1, forbidden 0, warnings 0

```bash
printf '%s\n' docs/contracts/parser_corpus_deck_summary_behavior_uplift.md \
  | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
```

- passed: changed paths 1, forbidden 0, warnings 0

```bash
printf '%s\n' docs/contracts/parser_corpus_deck_summary_behavior_uplift.md \
  | python3 tools/select_validation.py --base origin/main --paths-from-stdin
```

- passed: `selection_status: ok`
- required commands selected: diff check, protected-surface gate,
  secret/private-marker scan
- recommended command selected: agent docs checker

After this report was added, Codex E reran the path-scoped package checks for
both untracked docs:

```bash
printf '%s\n' \
  docs/contracts/parser_corpus_deck_summary_behavior_uplift.md \
  docs/contract_test_reports/parser_corpus_deck_summary_behavior_uplift.md \
  | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
```

- passed: scanned paths 2, forbidden 0, warnings 0

```bash
printf '%s\n' \
  docs/contracts/parser_corpus_deck_summary_behavior_uplift.md \
  docs/contract_test_reports/parser_corpus_deck_summary_behavior_uplift.md \
  | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
```

- passed: changed paths 2, forbidden 0, warnings 0

```bash
printf '%s\n' \
  docs/contracts/parser_corpus_deck_summary_behavior_uplift.md \
  docs/contract_test_reports/parser_corpus_deck_summary_behavior_uplift.md \
  | python3 tools/select_validation.py --base origin/main --paths-from-stdin
```

- passed: `selection_status: ok`

```bash
python3 - <<'PY'
from pathlib import Path

paths = [
    Path("docs/contracts/parser_corpus_deck_summary_behavior_uplift.md"),
    Path("docs/contract_test_reports/parser_corpus_deck_summary_behavior_uplift.md"),
]
errors = []
for path in paths:
    for idx, line in enumerate(path.read_text().splitlines(), 1):
        if line.rstrip() != line:
            errors.append(f"{path}:{idx}: trailing whitespace")
    if not path.read_text().endswith("\n"):
        errors.append(f"{path}: missing final newline")
if errors:
    print("\n".join(errors))
    raise SystemExit(1)
print("whitespace check passed for untracked docs")
PY
```

- passed: whitespace check passed for untracked docs

## Protected-Surface Status

Protected surfaces are preserved. Review found no authorization to change
parser behavior, parser event classes, parser state final reconciliation,
router semantics, corpus manifest status, session-ledger status, fixtures,
runtime behavior, workbook schema, webhook payload shape, Apps Script behavior,
Google Sheets sync, analytics truth, AI truth, coaching truth, CI gates, merge
readiness, deploy readiness, production behavior, or final integration policy.

## Secret And Private-Marker Status

The path-scoped secret/private-marker scan passed with 0 forbidden findings and
0 warnings for the new contract artifact.

No raw Player.log excerpts, UTC_Log excerpts, live MTGA output, local app-data
artifacts, generated artifacts, SQLite files, workbook exports, failed posts,
credentials, tokens, API keys, webhook URLs, private decklists, private deck
names, card choices, sideboard plans, or strategy notes were reviewed as inputs
or added by this report.

## Remaining Risks

- `deck_api.deck_summary` remains report-only and not parser-behavior-ready.
- Parser behavior readiness remains false.
- Pipeline activation for #388 remains false.
- Any future uplift needs a fresh issue and contract before taxonomy, fixture,
  parser, corpus metadata, or readiness changes are attempted.

## Next Recommended Role

Codex F: Module Submitter.

Reason: the contract-only artifact and this Codex E report are ready for a
governance/docs PR path. There are no blocking findings and no Codex C
implementation is authorized by #488.

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/488"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  related_pipeline_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  parent_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/482"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/487"
  previous_merge_commit: "a046b4550aae18a07a61cd8222ac2927ea930b6e"
  prior_boundary_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/394"
  related_start_hook_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/392"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contracts/parser_corpus_deck_summary_behavior_uplift.md"
  target_artifact: "docs/contract_test_reports/parser_corpus_deck_summary_behavior_uplift.md"
  verdict: "ready_for_module_submitter"
  risk_tier: "High"
  branch: "codex/parser-corpus-deck-summary-behavior-uplift-488"
  base_branch: "main"
  selected_family: "deck_api.deck_summary"
  current_status: "covered_report_only"
  selected_path: "preserve_report_only_taxonomy_or_distinct_evidence_required_before_behavior_uplift"
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  validation:
    - "PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json --out /tmp/mythic_edge_issue_488_corpus_report.json"
    - "PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py tests/test_collection_parser.py tests/test_event_schema_snapshots.py"
    - "python3 tools/check_agent_docs.py"
    - "python3 -m ruff check src tests tools"
    - "git diff --check"
    - "path-scoped secret/private-marker scan passed"
    - "path-scoped protected-surface gate passed"
    - "path-scoped validation selector passed"
  stop_conditions:
    - "Do not target main directly unless explicitly approved."
    - "Do not close tracker #158, pipeline tracker #388, parent issue #434, or issue #488."
    - "Do not activate #388 or #381."
    - "Do not promote deck_api.deck_summary or add parser_behavior_verified from StartHook evidence."
    - "Do not claim standalone deck-summary API support, parser support, readiness, production behavior, analytics truth, AI truth, coaching truth, full corpus parity, or tracker completion."
```
