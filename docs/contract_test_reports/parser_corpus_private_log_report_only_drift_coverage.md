# Parser Corpus Private Log Report-Only Drift Coverage Report

## Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/422
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/420
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/421
- Previous merge commit: `9a0a3538eab11dc4db5bc474c793f186d8c21ea5`

## Contract

- Source artifact:
  `docs/contracts/parser_corpus_private_log_report_only_drift_coverage.md`
- Selected path: `blocked_private_evidence`
- Risk tier: High

## Result

`mythic_edge.private_log_report_only_drift` is now represented as an inspected
private-evidence-blocked corpus boundary.

The row is not covered, synthetic, committed, parser-verified, diagnostics-only,
fixture-backed, or evidence-ledger-backed. It requires future approved
private/local evidence before Mythic Edge can make any stronger corpus parity
claim.

## Corpus Row

- `coverage_status`: `blocked_private_evidence`
- `coverage_basis`: `["local_report_only"]`
- `mythic_edge_entries`:
  - `private_log_report_only_drift_private_evidence_boundary_v1`
- `parser_event_families`: `[]`
- session-ledger entry: intentionally absent
- committed private report artifact: intentionally absent

## Non-Claims Preserved

This report does not claim:

- private smoke success
- live Player.log health
- parser support
- drift health
- release readiness
- deploy readiness
- production behavior
- analytics readiness
- analytics truth
- AI truth
- coaching truth
- full Mythic Edge corpus parity

Adjacent diagnostics, log-drift, unknown-entry, live diagnostics, evidence
ledger, golden replay, feature-equity, private-local readiness, and public
taxonomy surfaces remain non-claim context for this row.

## Report Evidence

The corpus parity report now returns:

```text
Corpus parity report: partial_coverage_map_ready (45 families, 6 committed, 1 missing)
```

The remaining missing family is `mythic_edge.analytics_readiness_labels`.

## Boundaries

No parser behavior, diagnostics behavior, log-drift behavior, status API
behavior, live app behavior, evidence-ledger behavior, golden replay behavior,
feature-equity behavior, workbook/webhook/App Script behavior, analytics
behavior, AI/model-provider behavior, CI policy, merge policy, deploy policy,
or production behavior was changed.

No raw private Player.log excerpts, private reports, private smoke outputs,
local runtime artifacts, generated data, SQLite files, workbook exports,
secrets, tokens, credentials, API keys, webhook URLs, IP/network traces,
decklists, private strategy notes, or local absolute paths were added.

## Validation

```bash
python3 -m json.tool tests/fixtures/parser_corpus/corpus_manifest.v1.json >/dev/null
PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
PYTHONPATH=src python3 -m pytest -q tests/test_parser_diagnostics_mode.py tests/test_log_drift_sensor.py tests/test_diagnostics.py
python3 tools/check_agent_docs.py
python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin
python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin
python3 -m ruff check src tests tools
git diff --check
python3 tools/select_validation.py --base origin/codex/parser-parity --paths-from-stdin
```

Results:

- manifest JSON check passed.
- focused corpus parity tests: 7 passed.
- corpus parity report: `partial_coverage_map_ready (45 families, 6 committed, 1 missing)`.
- adjacent diagnostics/drift support tests: 20 passed.
- agent docs check passed.
- changed-path secret/private-marker scan passed.
- changed-path protected-surface gate passed.
- Ruff passed.
- diff whitespace check passed.
- selector returned `selection_status: ok`.
- new-doc whitespace guard, ASCII scan, generated SQLite artifact scan, and
  protected source/runtime path diff were clean.

## Residual Risks

- The row remains blocked because no user-approved private/local drift report
  evidence is committed or referenced.
- A future stronger status needs a separate privacy and fixture-acceptance
  contract.
- Analytics readiness labels remain separately scoped.

## Next Recommended Role

Codex F: Module Submitter.

## Codex E Contract-Test Review

### Findings

No blocking findings.

### Contract-Test Verdict

Pass. The package moves only `mythic_edge.private_log_report_only_drift`
from `missing` to `blocked_private_evidence`, with `coverage_basis` exactly
`["local_report_only"]`, one manifest-only Mythic Edge entry
`private_log_report_only_drift_private_evidence_boundary_v1`, empty
`parser_event_families`, and no session-ledger entry.

The manifest entry is explicitly local/private/report-only boundary metadata:
`entry_type` is `local_private_report_summary`, `source_kind` is
`local_private_report_only`, `commit_status` is `local_report_only`,
`privacy_class` is `local_private_not_committed`, `sanitization_status` is
`requires_review`, and `paths` is `{}`. It does not add `covered_report_only`,
`parser_behavior_verified`, `diagnostics_only`, `fixture_metadata_only`, or
`evidence_ledger_only`.

Adjacent rows remain separate and unchanged in meaning:

| scenario_family | status |
| --- | --- |
| `mythic_edge.analytics_readiness_labels` | `missing` |
| `mythic_edge.live_diagnostics` | `covered_report_only` |
| `log_runtime.unknown_entry` | `covered_report_only` |
| `mythic_edge.evidence_ledger_provenance` | `covered_report_only` |

### Validation Results

```text
PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py
7 passed in 0.11s

PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
Corpus parity report: partial_coverage_map_ready (45 families, 6 committed, 1 missing)

PYTHONPATH=src python3 -m pytest -q tests/test_parser_diagnostics_mode.py tests/test_log_drift_sensor.py tests/test_diagnostics.py
20 passed in 0.06s

python3 tools/check_agent_docs.py
result: passed

python3 tools/check_secret_patterns.py --base origin/codex/parser-parity --paths-from-stdin
result: passed; forbidden: 0; warnings: 0

python3 tools/check_protected_surfaces.py --base origin/codex/parser-parity --paths-from-stdin
result: passed; forbidden: 0; warnings: 0

python3 tools/select_validation.py --base origin/codex/parser-parity --paths-from-stdin
selection_status: ok

python3 -m ruff check src tests tools
All checks passed!

git diff --check
passed

python3 -m json.tool tests/fixtures/parser_corpus/corpus_manifest.v1.json >/dev/null
passed

LC_ALL=C rg -n '[[:blank:]]$' <changed files>
no matches

LC_ALL=C rg -n '[^[:ascii:]]' <changed files>
no matches
```

### Protected-Surface Status

The changed package remains limited to:

- `docs/contracts/parser_corpus_private_log_report_only_drift_coverage.md`
- `docs/implementation_handoffs/parser_corpus_private_log_report_only_drift_coverage_comparison.md`
- `docs/contract_test_reports/parser_corpus_private_log_report_only_drift_coverage.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/test_corpus_parity_report.py`

`tests/fixtures/parser_corpus/session_ledger.v1.json` is unchanged. No parser,
router, diagnostics, drift, status API, live app, evidence-ledger, golden replay,
feature-equity, workbook, webhook, Apps Script, Google Sheets sync, output
transport, analytics, AI/model-provider, CI, merge/deploy, production, or
runtime-artifact behavior changed. No private Player.log, private report,
private smoke output, runtime artifact, generated data, SQLite file, workbook
export, secret, token, credential, API key, webhook URL, IP/network trace,
decklist, private strategy note, or local absolute path was added.

### Remaining Risks

The row remains intentionally blocked because there is no user-approved
private/local drift report evidence in scope. Any stronger status needs a new
contract, privacy review, and fixture/evidence acceptance path. Analytics
readiness labels remain separately scoped and still missing.

### Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/422"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/420"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/421"
  previous_merge_commit: "9a0a3538eab11dc4db5bc474c793f186d8c21ea5"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contract_test_reports/parser_corpus_private_log_report_only_drift_coverage.md"
  target_artifact: "draft PR for private-log report-only drift private-evidence boundary"
  verdict: "no_blocking_findings_ready_for_module_submitter"
  risk_tier: "High"
  branch: "codex/parser-corpus-private-log-report-only-drift-coverage"
  base_branch: "codex/parser-parity"
  selected_path: "blocked_private_evidence"
  validation:
    - "PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py"
    - "PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json"
    - "PYTHONPATH=src python3 -m pytest -q tests/test_parser_diagnostics_mode.py tests/test_log_drift_sensor.py tests/test_diagnostics.py"
    - "python3 tools/check_agent_docs.py"
    - "python3 -m ruff check src tests tools"
    - "git diff --check"
    - "path-scoped secret/private marker scan for changed files"
    - "path-scoped protected-surface gate for changed files"
    - "path-scoped validation selector sanity check for changed files"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close issue #422 or tracker #158 unless separately authorized."
    - "Do not run actual private app-data checks or Player.log checks."
    - "Do not use blocked-private-evidence metadata as private smoke success, live Player.log health, parser support, drift health, release readiness, deploy readiness, production behavior, analytics readiness, analytics truth, AI truth, coaching truth, or full-parity authority."
    - "Do not promote this family beyond blocked_private_evidence without a new contract, user-approved private/local evidence, and publish-safe privacy review."
    - "Do not add covered_report_only, parser_behavior_verified, diagnostics_only, fixture_metadata_only, evidence_ledger_only, private report artifacts, session-ledger entries, parser event families, committed logs, generated/private/runtime artifacts, SQLite files, workbook exports, secrets, tokens, API keys, webhook URLs, private report contents, IP/network traces, decklists, private strategy notes, or local absolute paths."
    - "Do not change parser behavior, parser state final reconciliation, parser event classes, router semantics, diagnostics behavior, log-drift behavior, status API behavior, live app behavior, evidence-ledger behavior, golden replay behavior, feature-equity behavior, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets sync, output transport, analytics behavior, AI/model-provider behavior, CI policy, merge policy, deploy policy, or production behavior."
```
