# Parser Corpus Parity Expansion Contract Test Report

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/291

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/158

## Contract

`docs/contracts/parser_corpus_parity_expansion.md`

## Implementation Under Test

Branch: `codex/parser-corpus-parity-expansion`

Base commit: `9cb5f5b9805f530edad827378d14bf3b373b526d`

Changed-file package under review:

- `docs/contracts/parser_corpus_parity_expansion.md`
- `docs/implementation_handoffs/parser_corpus_parity_expansion_comparison.md`
- `docs/templates/parser_corpus_session.md`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `tests/test_corpus_parity_report.py`

## Report Lifecycle

`report_lifecycle`: `fixer_pass_re_review`

## Codex D Fixer Addendum

Status: CPC-E-001 fixed in the contract and implementation handoff, confirmed
by Codex E re-review.

Codex D added checker-verifiable category-specific authorization evidence for
the protected `workflow_authority_docs` surface at
`docs/templates/parser_corpus_session.md`. The original Codex E finding below
remains historical evidence for the initial review.

Codex D validation:

- `python3 -m pytest -q tests/test_corpus_parity_report.py` -> `7 passed`
- `python3 -m pytest -q tests` -> `1697 passed`
- `python3 -m ruff check src tests tools` -> passed
- `python3 tools/check_agent_docs.py` -> passed
- untracked package whitespace scan -> passed
- package-scoped secret/private-marker scan -> passed, `forbidden: 0`,
  `warnings: 0`
- package-scoped protected-surface gate -> passed, `forbidden: 0`,
  `warnings: 1`
- protected-surface authorization checker -> `authorization_status: ok`,
  `authorized: 1`, `missing_authorization: 0`

## Contract Summary

Issue #291 defines the first corpus parity metadata/report scaffold under
tracker #158. The implementation must provide manifest/session-ledger metadata,
a category-level compatibility report, and focused validation while preserving
parser truth ownership and keeping external Manasight material category-only.

The module must not import external logs, commit private/raw artifacts, change
parser behavior, change protected downstream surfaces, or let corpus coverage
decide parser truth, merge readiness, deploy readiness, tracker completion,
analytics truth, workbook truth, gameplay advice, or AI truth.

## Internal Project Area Reviewed

Parser Reliability / Corpus Evidence.

## Bridge-Code Status Reviewed

`shared_support` metadata/report scaffold.

## Findings

### Blocking

No blocking findings remain after the Codex D fixer pass.

### Resolved

#### CPC-E-001: Protected workflow-template authorization is now checker-verifiable

Original finding: `docs/templates/parser_corpus_session.md` is a protected
workflow authority surface. The initial contract listed the template as an
authorized implementation artifact at
`docs/contracts/parser_corpus_parity_expansion.md:131`, but the
protected-surface authorization checker did not accept that wording as
category-specific authorization.

Original evidence:

```bash
printf '%s\n' docs/templates/parser_corpus_session.md | python3 tools/check_surface_authorization.py --base origin/main --paths-from-stdin --authorization-file contract=docs/contracts/parser_corpus_parity_expansion.md --authorization-file handoff=docs/implementation_handoffs/parser_corpus_parity_expansion_comparison.md
```

Result:

```text
protected: 1
forbidden: 0
authorized: 0
missing_authorization: 1
MISSING_AUTHORIZATION workflow_authority_docs docs/templates/parser_corpus_session.md - No accepted category-specific authorization evidence found.
authorization_status: review
```

Fix verification:

```bash
printf '%s\n' docs/templates/parser_corpus_session.md | python3 tools/check_surface_authorization.py --base origin/main --paths-from-stdin --authorization-file contract=docs/contracts/parser_corpus_parity_expansion.md --authorization-file handoff=docs/implementation_handoffs/parser_corpus_parity_expansion_comparison.md
```

Result:

```text
protected: 1
forbidden: 0
authorized: 1
missing_authorization: 0
AUTHORIZED workflow_authority_docs docs/templates/parser_corpus_session.md
authorization_status: ok
```

Resolution: Codex D added accepted category-specific authorization evidence to
the contract and handoff:
`Protected-surface authorization: Authorized drift - workflow_authority_docs -
docs/templates/parser_corpus_session.md - issue #291 and
docs/contracts/parser_corpus_parity_expansion.md.`

### Non-Blocking

- The implementation package is currently untracked. Literal
  `git diff --check` and changed-file diff commands do not inspect untracked
  files until Codex F stages or commits them. I ran explicit path-scoped scans
  for the package.
- A local ignored runtime log exists under `data/runtime_logs/`. It is ignored
  by `.gitignore`, not tracked, and not part of this package. Submitter should
  continue to avoid staging generated/private/local artifacts.
- Direct `python3 -m mythic_edge_parser.app.corpus_parity_report ...` imported
  an installed editable package from another local worktree in this environment
  and did not see the untracked module. With `PYTHONPATH=src`, the module CLI
  produced the expected report summary. This is local environment pathing, not
  a package behavior blocker after staging/install.

## Checks Run

```bash
gh issue view 291 --repo Tahjali11/Mythic-Edge --json number,title,state,body,labels,comments,url
gh issue view 158 --repo Tahjali11/Mythic-Edge --json number,title,state,url
gh repo view manasight/manasight-corpus --json name,defaultBranchRef,pushedAt,url
gh api repos/manasight/manasight-corpus/contents --jq '.[].name'
python3 -m pytest -q tests/test_corpus_parity_report.py
python3 -m pytest -q tests/test_golden_replay_harness.py tests/test_feature_equity_corpus_ratchet.py
python3 -m pytest -q tests
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
python3 -m ruff check src tests tools
python3 tools/check_agent_docs.py
git diff --check
printf '%s\n' docs/contracts/parser_corpus_parity_expansion.md docs/implementation_handoffs/parser_corpus_parity_expansion_comparison.md docs/templates/parser_corpus_session.md docs/contract_test_reports/parser_corpus_parity_expansion.md src/mythic_edge_parser/app/corpus_parity_report.py tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' docs/contracts/parser_corpus_parity_expansion.md docs/implementation_handoffs/parser_corpus_parity_expansion_comparison.md docs/templates/parser_corpus_session.md docs/contract_test_reports/parser_corpus_parity_expansion.md src/mythic_edge_parser/app/corpus_parity_report.py tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
printf '%s\n' docs/contracts/parser_corpus_parity_expansion.md docs/implementation_handoffs/parser_corpus_parity_expansion_comparison.md docs/templates/parser_corpus_session.md docs/contract_test_reports/parser_corpus_parity_expansion.md src/mythic_edge_parser/app/corpus_parity_report.py tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py | python3 tools/select_validation.py --base origin/main --paths-from-stdin
printf '%s\n' docs/templates/parser_corpus_session.md | python3 tools/check_surface_authorization.py --base origin/main --paths-from-stdin --authorization-file contract=docs/contracts/parser_corpus_parity_expansion.md --authorization-file handoff=docs/implementation_handoffs/parser_corpus_parity_expansion_comparison.md
python3 tools/run_pyright_advisory_report.py
find . -path './.git' -prune -o \( -name '*.log' -o -name '*.log.gz' -o -name '*.sqlite' -o -name '*.sqlite3' -o -name '*.db' -o -name '*.db-wal' -o -name '*.db-shm' -o -name '*.zip' -o -name '*.jsonl' \) -print
```

## Results

Passed:

- `python3 -m pytest -q tests/test_corpus_parity_report.py` -> `7 passed`
- `python3 -m pytest -q tests/test_golden_replay_harness.py tests/test_feature_equity_corpus_ratchet.py` -> `20 passed`
- `python3 -m pytest -q tests` -> `1697 passed`
- `PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report ...` -> `partial_coverage_map_ready`
- `python3 -m ruff check src tests tools` -> passed
- `python3 tools/check_agent_docs.py` -> passed
- `git diff --check` -> passed
- path-scoped secret/private-marker scan -> passed, `forbidden: 0`, `warnings: 0`
- path-scoped protected-surface gate -> passed, `forbidden: 0`, `warnings: 1`
- path-scoped validation selector -> `selection_status: warning`, expected protected workflow-template warning
- protected-surface authorization checker -> passed, `authorization_status: ok`,
  `authorized: 1`, `missing_authorization: 0`
- `python3 tools/run_pyright_advisory_report.py` -> advisory findings, `tooling_config_blockers: 0`

Failed review gate:

- None after Codex D fixer pass and Codex E re-review.

External reference check:

- Live GitHub metadata for `manasight/manasight-corpus` still matches the issue
  context at review time: default branch `main`, pushed
  `2026-05-28T21:22:52Z`, with top-level `corpus`, `sessions.md`, and
  `smoke-corpus-manifest.toml`. No external files were copied into the package.

Artifact sweep note:

- The package files do not include external logs, Manasight compressed files,
  private Player.log excerpts, SQLite files, JSONL files, or generated data.
- An ignored local `data/runtime_logs/` artifact exists in the worktree. It is
  not tracked and not part of the package.

## Finding Lifecycle Summary

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CPC-E-001 | High | `resolved_by_fixer` | Protected workflow-template authorization is checker-verifiable | non-blocking | Initial `check_surface_authorization.py` reported `MISSING_AUTHORIZATION workflow_authority_docs` and `authorization_status: review` | Re-review `check_surface_authorization.py` reports `AUTHORIZED workflow_authority_docs`, `authorized: 1`, `missing_authorization: 0`, `authorization_status: ok` | F |

## Confirmed Contract Matches

- The implementation is metadata/report-only and does not change parser
  behavior, parser state, event classes, router semantics, workbook schema,
  webhook shape, Apps Script, Google Sheets, local app, Match Journal, SQLite,
  analytics truth, AI/model-provider behavior, or production behavior.
- `src/mythic_edge_parser/app/corpus_parity_report.py` builds a deterministic
  compatibility report from explicit manifest/session-ledger inputs.
- The committed corpus manifest and session ledger validate cleanly.
- The compatibility report uses the contracted vocabulary and retains
  limitations that prevent overclaiming parser correctness, merge readiness,
  deploy readiness, tracker completion, analytics truth, workbook truth,
  gameplay advice, or AI truth.
- External Manasight material remains category/reference-only. No external
  logs, compressed corpus files, raw session rows, hashes, parser source, or
  manifest/session mirrors were copied.
- Privacy tests reject local paths and external log-like artifacts without
  echoing sensitive values.
- Focused tests, adjacent golden replay/feature-equity tests, full pytest,
  Ruff, agent docs, and path-scoped secret/private-marker scan pass.

## Contract Mismatches

No contract mismatches remain after the Codex D fixer pass.

## Missing Tests

No blocking test gaps in the implementation behavior were found. The focused
test suite covers manifest/session validation, report vocabulary, private path
redaction, external artifact blocking, redaction flags, and CLI behavior.

## Drift Notes

- Local environment drift: direct `python3 -m mythic_edge_parser...` imports an
  installed editable package from another local worktree unless `PYTHONPATH=src`
  is supplied. This did not affect pytest or the package behavior under the
  repo's test configuration.
- Local ignored artifact drift: `data/runtime_logs/` exists locally and is
  ignored. It must not be staged or submitted.
- External reference drift: Manasight repo metadata was checked live; future
  reviews should re-check because external categories can change.

## Recommendation

Route to Codex F: Module Submitter. CPC-E-001 is resolved and no blocking
findings remain.

## Next Workflow Action

Next role: Codex F: Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #291, parser corpus parity expansion.

Review the Codex E contract-test report and Codex D fixer addendum:
docs/contract_test_reports/parser_corpus_parity_expansion.md

Goal:
Stage only the reviewed parser corpus parity expansion package, commit, push,
and open or update a draft PR for issue #291. Do not target main directly.

Reviewed files:
- docs/contracts/parser_corpus_parity_expansion.md
- docs/implementation_handoffs/parser_corpus_parity_expansion_comparison.md
- docs/contract_test_reports/parser_corpus_parity_expansion.md
- docs/templates/parser_corpus_session.md
- src/mythic_edge_parser/app/corpus_parity_report.py
- tests/fixtures/parser_corpus/corpus_manifest.v1.json
- tests/fixtures/parser_corpus/session_ledger.v1.json
- tests/test_corpus_parity_report.py

Validation:
python3 -m pytest -q tests/test_corpus_parity_report.py
python3 -m pytest -q tests/test_golden_replay_harness.py tests/test_feature_equity_corpus_ratchet.py
python3 -m pytest -q tests
python3 -m ruff check src tests tools
python3 tools/check_agent_docs.py
git diff --check
printf '%s\n' docs/contracts/parser_corpus_parity_expansion.md docs/implementation_handoffs/parser_corpus_parity_expansion_comparison.md docs/templates/parser_corpus_session.md docs/contract_test_reports/parser_corpus_parity_expansion.md src/mythic_edge_parser/app/corpus_parity_report.py tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' docs/contracts/parser_corpus_parity_expansion.md docs/implementation_handoffs/parser_corpus_parity_expansion_comparison.md docs/templates/parser_corpus_session.md docs/contract_test_reports/parser_corpus_parity_expansion.md src/mythic_edge_parser/app/corpus_parity_report.py tests/fixtures/parser_corpus/corpus_manifest.v1.json tests/fixtures/parser_corpus/session_ledger.v1.json tests/test_corpus_parity_report.py | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
printf '%s\n' docs/templates/parser_corpus_session.md | python3 tools/check_surface_authorization.py --base origin/main --paths-from-stdin --authorization-file contract=docs/contracts/parser_corpus_parity_expansion.md --authorization-file handoff=docs/implementation_handoffs/parser_corpus_parity_expansion_comparison.md

Do not:
- Target main directly.
- Close tracker #158.
- Change parser behavior, parser state final reconciliation, parser event classes, router semantics, workbook schema, webhook payload shape, Apps Script behavior, output transport, runtime status schema, Match Journal behavior, overlay behavior, SQLite behavior, Google Sheets behavior, analytics truth, AI truth, OpenAI/model-provider behavior, CI gates, merge policy, deploy policy, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed delivery artifacts, workbook exports, or production behavior.
- Import, copy, mirror, or commit external corpus logs, compressed files, raw session rows, hashes, parser source, private Player.log excerpts, local diagnostics artifacts, local runtime artifacts, API keys, tokens, credentials, webhook URLs, or generated data.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/291"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contract_test_reports/parser_corpus_parity_expansion.md"
  target_artifact: "draft PR for parser corpus parity expansion package"
  verdict: "no_blocking_findings_ready_for_module_submitter"
  risk_tier: "High"
  branch: "codex/parser-corpus-parity-expansion"
  base_commit: "9cb5f5b9805f530edad827378d14bf3b373b526d"
  validation:
    - "python3 -m pytest -q tests/test_corpus_parity_report.py -> 7 passed"
    - "python3 -m pytest -q tests/test_golden_replay_harness.py tests/test_feature_equity_corpus_ratchet.py -> 20 passed"
    - "python3 -m pytest -q tests -> 1697 passed"
    - "PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json -> partial_coverage_map_ready"
    - "python3 -m ruff check src tests tools -> passed"
    - "python3 tools/check_agent_docs.py -> passed"
    - "git diff --check -> passed"
    - "path-scoped secret/private-marker scan -> passed"
    - "path-scoped protected-surface gate -> warning workflow_authority_docs"
    - "tools/check_surface_authorization.py -> authorization_status ok, authorized 1, missing_authorization 0"
    - "python3 tools/run_pyright_advisory_report.py -> advisory findings, tooling_config_blockers 0"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close tracker #158."
    - "Do not change parser behavior or protected runtime/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
    - "Do not import or commit Manasight logs/source or raw/private Player.log content."
    - "Do not commit generated/private/runtime artifacts or secrets."
```
