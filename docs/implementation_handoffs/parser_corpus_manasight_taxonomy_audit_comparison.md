# Parser Corpus Manasight Taxonomy Audit Implementation Handoff

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/352

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/158

## Contract

docs/contracts/parser_corpus_manasight_taxonomy_audit.md

## Internal Project Area

Corpus / Provenance

## Truth Owner

- Mythic Edge coverage truth:
  `src/mythic_edge_parser/app/corpus_parity_report.py`,
  `tests/fixtures/parser_corpus/corpus_manifest.v1.json`, and
  `tests/fixtures/parser_corpus/session_ledger.v1.json`
- Parser behavior truth: parser modules, router, event classes, and parser
  state
- Public external metadata truth: public `manasight/manasight-corpus`
  repository

## Bridge-Code Status

bridge_code

## Role Performed

Codex C: Module Implementer / Metadata-only Audit Reporter

## What Changed

Created the required metadata-only taxonomy audit report:

- `docs/contract_test_reports/parser_corpus_manasight_taxonomy_audit.md`

Created this implementation handoff:

- `docs/implementation_handoffs/parser_corpus_manasight_taxonomy_audit_comparison.md`

No code, tests, parser fixtures, external corpus files, runtime artifacts, or
generated private artifacts were added or changed.

## Dependency Check

#351 was verified as merged:

- dependency issue: https://github.com/Tahjali11/Mythic-Edge/issues/351
- dependency PR: https://github.com/Tahjali11/Mythic-Edge/pull/353
- PR state: merged
- merge commit: f91e38e7de421e52e44f2e6d9e693c40bbe7218b
- local branch HEAD: f91e38e7de421e52e44f2e6d9e693c40bbe7218b

The current Mythic Edge corpus parity report shows
`drift_debug.gsm_truncation` as `covered_synthetic`, so the audit is not
provisional for #351.

## Current Mythic Edge Snapshot

Generated from repo-owned inputs:

- report status: partial_coverage_map_ready
- total_scenario_families: 45
- covered_committed: 6
- covered_synthetic: 2
- covered_report_only: 0
- partial: 3
- missing: 28
- deferred: 0
- blocked_private_evidence: 0
- blocked_external_boundary: 6

## Public Manasight Metadata Snapshot

Observed through bounded public GitHub metadata:

- repository: https://github.com/manasight/manasight-corpus
- default_branch: main
- observed main commit: ea4d1a86c3711717b5ef9a354c7f9279598c43c3
- pushed_at: 2026-05-28T21:22:52Z
- corpus_tag: manasight-corpus-v1
- public manifest metadata entry count: 44
- public session heading count observed: 149

Only category-level metadata was used. No external corpus files, compressed log
files, raw session bodies, hash lists, byte-size lists, capture-date row lists,
or parser source were copied into Mythic Edge.

## Files Changed

- `docs/contracts/parser_corpus_manasight_taxonomy_audit.md`
  - Existing untracked Codex B contract.
- `docs/contract_test_reports/parser_corpus_manasight_taxonomy_audit.md`
  - New Codex C audit report.
- `docs/implementation_handoffs/parser_corpus_manasight_taxonomy_audit_comparison.md`
  - New Codex C handoff.

## Code Changed

None.

## Tests Added Or Updated

None.

## Interface Changes

None. No Python APIs, CLI flags, environment variables, schemas, workbook
columns, webhook fields, Apps Script mappings, runtime routes, issue lifecycle
rules, or PR lifecycle rules changed.

## Contracted Area Status

Stayed inside the contracted Corpus / Provenance report-only scope. The audit
maps public reference taxonomy to current Mythic Edge corpus coverage states,
but it does not make external metadata executable, parser-owned, analytics
owned, workbook-owned, AI-owned, merge-readiness, deploy-readiness, or
tracker-completion truth.

## Validation Run

```bash
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
```

- passed: `Corpus parity report: partial_coverage_map_ready (45 families, 6 committed, 28 missing)`

```bash
python3 -m pytest -q tests/test_corpus_parity_report.py
```

- passed: 7 passed

```bash
python3 tools/check_agent_docs.py
```

- passed: errors 0, warnings 0

```bash
git diff --check
```

- passed with no output for tracked local diffs

```bash
git diff --no-index --check /dev/null <untracked-doc>
```

- passed for the untracked contract, audit report, and handoff with no
  whitespace output

```bash
git diff --name-only origin/main...HEAD | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
git diff --name-only origin/main...HEAD | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
git diff --name-only origin/main...HEAD | python3 tools/select_validation.py --base origin/main --paths-from-stdin
```

- passed, but scanned 0 paths because this Codex C work is uncommitted and the
  branch has no committed delta from `origin/main...HEAD`

Because this work is uncommitted and includes untracked Markdown files,
explicit changed-file scans were also run over:

- `docs/contracts/parser_corpus_manasight_taxonomy_audit.md`
- `docs/contract_test_reports/parser_corpus_manasight_taxonomy_audit.md`
- `docs/implementation_handoffs/parser_corpus_manasight_taxonomy_audit_comparison.md`

Results:

- explicit changed-file secret/private-marker scan: passed, scanned_paths 3,
  forbidden 0, warnings 0
- explicit changed-file protected-surface gate: passed, changed_paths 3,
  forbidden 0, warnings 0
- explicit changed-file validation selector: selection_status ok; required
  checks were diff check, protected-surface gate, and secret/private-marker
  scan; recommended check was agent docs checker

## Still Unverified

- No CI was inspected.
- No PR was opened.
- No tracker update was performed.
- No parser/runtime/workbook/webhook/App Script/local app/analytics/AI or
  production behavior was exercised because those layers are outside this
  contract.

## Reviewer Focus

Codex E should pay special attention to:

- Whether the audit overclaims full parity from category mapping alone.
- Whether external public metadata is bounded to category-level reference only.
- Whether any row accidentally treats Manasight metadata as Mythic Edge parser
  support.
- Whether #351 is correctly treated as merged and non-provisional.
- Whether follow-up recommendations route behavior work to future Codex A/B
  issues instead of implementing behavior here.

## Next Workflow Action

Next role: Codex E / Module Reviewer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer for issue #352 under tracker #158.

Branch:
codex/manasight-corpus-taxonomy-audit

Contract:
docs/contracts/parser_corpus_manasight_taxonomy_audit.md

Audit report:
docs/contract_test_reports/parser_corpus_manasight_taxonomy_audit.md

Implementation handoff:
docs/implementation_handoffs/parser_corpus_manasight_taxonomy_audit_comparison.md

Review focus:
- Confirm the audit is metadata-only and report-only.
- Confirm #351 is treated as merged and `drift_debug.gsm_truncation` maps to
  `covered_synthetic`.
- Confirm public Manasight metadata is used only as bounded reference taxonomy.
- Confirm no Manasight raw logs, compressed corpus files, external raw session
  rows, hash lists, byte-size row lists, capture-date row lists, parser source,
  private logs, generated artifacts, credentials, tokens, keys, or webhook URLs
  were committed.
- Confirm the audit does not claim full Mythic Edge corpus parity, parser
  support from category mapping, merge readiness, deploy readiness, or tracker
  completion.
- Confirm follow-up recommendations route future behavior or fixture work to
  future #158 child issues.

Validation to review or rerun:
- PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
- python3 -m pytest -q tests/test_corpus_parity_report.py
- python3 tools/check_agent_docs.py
- git diff --check
- path-scoped secret/private-marker scan for changed files
- path-scoped protected-surface gate for changed files
- path-scoped validation selector for changed files

Do not:
- Implement parser behavior changes.
- Open a PR.
- Close #158 or #352.
- Target main directly.
- Import, copy, mirror, or commit Manasight raw logs, compressed corpus files,
  raw session payloads, or external corpus contents.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/352"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  dependency_completed: "https://github.com/Tahjali11/Mythic-Edge/issues/351"
  dependency_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/353"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_corpus_manasight_taxonomy_audit.md"
  target_artifact: "docs/contract_test_reports/parser_corpus_manasight_taxonomy_audit.md"
  expected_handoff: "docs/implementation_handoffs/parser_corpus_manasight_taxonomy_audit_comparison.md"
  verdict: "metadata_only_taxonomy_audit_ready_for_review"
  risk_tier: "High"
  branch: "codex/manasight-corpus-taxonomy-audit"
  base_commit: "f91e38e7de421e52e44f2e6d9e693c40bbe7218b"
  validation:
    - "PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json"
    - "python3 -m pytest -q tests/test_corpus_parity_report.py"
    - "python3 tools/check_agent_docs.py"
    - "git diff --check"
    - "path-scoped secret/private-marker scan for changed files"
    - "path-scoped protected-surface gate for changed files"
    - "path-scoped validation selector for changed files"
  stop_conditions:
    - "Do not implement parser behavior changes."
    - "Do not open a PR."
    - "Do not close #158 or #352."
    - "Do not target main directly."
    - "Do not import, copy, mirror, or commit Manasight raw logs, compressed corpus files, raw session payloads, or external corpus contents."
    - "Use public Manasight corpus metadata only as reference taxonomy."
    - "Do not claim full Mythic Edge corpus parity from taxonomy mapping alone."
```
