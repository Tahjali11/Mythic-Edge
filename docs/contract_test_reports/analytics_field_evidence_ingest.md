# Analytics Field-Evidence Ingest Contract-Test Report

report_lifecycle: initial_contract_test
role_performed: Codex E: Module Reviewer / contract-test thread
branch: codex/analytics-foundation
risk_tier: Medium

followup_lifecycle: followup_after_fixer
followup_role_performed: Codex E: Module Reviewer / confirmation thread
followup_fixer_handoff: `docs/implementation_handoffs/analytics_field_evidence_ingest_fixer.md`

## Source Artifacts

- Contract: `docs/contracts/analytics_field_evidence_ingest.md`
- Implementation handoff: `docs/implementation_handoffs/analytics_field_evidence_ingest_comparison.md`
- Workflow guide: `docs/agent_threads/contract_test.md`
- Template: `docs/templates/contract_test_report.md`

## Files Reviewed

- `src/mythic_edge_parser/app/analytics_ingest.py`
- `tests/test_analytics_field_evidence_ingest.py`
- `tests/test_analytics_gameplay_action_ingest.py`
- `tests/test_analytics_opponent_card_observation_ingest.py`
- `tests/test_analytics_parser_normalized_replay_ingest.py`
- `src/mythic_edge_parser/app/evidence_ledger.py`
- `src/mythic_edge_parser/app/runtime_field_evidence.py`
- `src/mythic_edge_parser/app/analytics_migrations/0001_initial_analytics_schema.sql`

## Findings

### Follow-up Confirmation: Prior P1 fixed

finding_id: analytics_field_evidence_ingest_001
finding_lifecycle: fixed_state_followup
finding_status: fixed
blocking_status: resolved
next_route: Codex F

Codex D tightened `source_payload_paths` label validation in `src/mythic_edge_parser/app/analytics_ingest.py:1487` so root-level local path roots and slash-prefixed drive-letter local path shapes are rejected before the JSON-pointer compatibility allowance can persist them.

Verification evidence:

- Direct runtime reproduction rejected all reviewed unsafe shapes with zero field-evidence provenance rows.
- Direct runtime reproduction confirmed a valid parser JSON-pointer label still writes one field-evidence provenance row.
- `tests/test_analytics_field_evidence_ingest.py:271` now covers root-level local path roots and slash-prefixed drive-letter local path shapes.
- Focused tests, related evidence-ledger tests, Ruff, `git diff --check`, agent-doc checks, secret/private-marker scan, protected-surface scan, and generated SQLite artifact checks passed.

No remaining blocking findings were found in the confirmation pass.

### P1: JSON-pointer compatibility accepts root-level local absolute paths into `fact_provenance`

finding_id: analytics_field_evidence_ingest_001
finding_lifecycle: original_finding
finding_status: superseded_by_fixed_state_followup
blocking_status: resolved
next_route: Codex F

`docs/contracts/analytics_field_evidence_ingest.md:246` requires field-evidence ingest to reject local absolute paths and private runtime artifact paths, while `docs/contracts/analytics_field_evidence_ingest.md:262` limits `source_payload_paths` to safe labels or JSON-pointer-like paths.

The implementation filters out canonical `evidence_ledger.validate_field_evidence()` absolute-path errors for `source_payload_paths`, then applies a local allowlist in `src/mythic_edge_parser/app/analytics_ingest.py:1486`. That local check rejects paths with a trailing path segment under known local roots, but it does not reject the root path values themselves. As a result, root-level local directory labels for temp, home, restricted, and runtime roots, plus slash-prefixed drive-letter local path shapes, can be treated as JSON-pointer-compatible labels and written into durable `fact_provenance.source_payload_paths`.

Reproduction evidence from the public ingest API:

```text
accepted synthetic root-level temp label
accepted synthetic root-level user-home label
accepted synthetic root-level private-directory label
accepted synthetic root-level runtime-directory label
accepted synthetic slash-prefixed drive-letter local path shape
```

The focused malformed-attachment test covers a Windows-drive path, a slash-prefixed user-home path containing a raw-log filename, and a webhook-like URL at `tests/test_analytics_field_evidence_ingest.py:269`, but it does not cover root-only local path values or slash-prefixed drive-letter paths. This leaves the contract privacy guarantee incomplete.

Expected fix: keep valid JSON-pointer-like labels such as `/match_log_rows/0/match_id` accepted, but reject root-level local absolute paths, slash-prefixed drive paths, and any other local path shape before persistence. Add focused regression coverage that fails without leaving partial rows.

## Finding Lifecycle Summary

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| analytics_field_evidence_ingest_001 | P1 | `fixed_state_followup` | fixed | resolved | Runtime probe accepted root-level local path values into `fact_provenance.source_payload_paths`. | D fix rejects reviewed unsafe path shapes with zero field-evidence provenance rows while preserving valid parser JSON-pointer labels. | F |

## Confirmed Contract Matches

- Field evidence is no longer reported as deferred or skipped for valid entries.
- Valid canonical field-evidence records are validated through `evidence_ledger.validate_field_evidence()`, with an explicit compatibility filter for JSON-pointer-like `source_payload_paths`.
- Valid field evidence writes deterministic `field_evidence:{sha256(...)}` rows into `fact_provenance`.
- Multiple field-evidence records can attach to the same `fact_table`, `fact_id`, and `fact_field` without collapsing.
- Re-ingesting the same replay remains idempotent.
- Existing automatic provenance rows are preserved.
- Field evidence writes only `fact_provenance`; reviewed tests confirm the target fact row itself is not mutated.
- Missing canonical fields, invalid vocabulary, review-required mismatches, malformed attachment fields, and missing target fact rows fail and roll back.
- Target fact table checks use an explicit fact-table allowlist and existing-row lookup.
- No SQLite schema or migration files were changed.
- No parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, live ingest, CLI, Google Sheets sync, AI/OpenAI runtime behavior, or production behavior change was found in this slice.

## Contract Mismatches

- Resolved in follow-up: privacy validation for `source_payload_paths` now rejects the reviewed local absolute path shapes after the JSON-pointer compatibility filter.

## Missing Tests Or Safeguards

- Resolved in follow-up: regression coverage now includes root-only local directory labels for temp, home, restricted, and runtime roots, plus slash-prefixed drive paths in `source_payload_paths`.
- Non-blocking residual gap: focused field-evidence tests use the `matches` table as the representative target. Broader match/game/action/opponent-observation target coverage remains unverified, although the implementation path is generic and uses an explicit fact-table allowlist.

## Validation Run

- `git status --short --branch` -> branch confirmed as `codex/analytics-foundation`; field-evidence package is uncommitted alongside the broader analytics ingest package state.
- `py -m pytest -q tests\test_analytics_field_evidence_ingest.py tests\test_analytics_opponent_card_observation_ingest.py tests\test_analytics_gameplay_action_ingest.py tests\test_analytics_parser_normalized_replay_ingest.py tests\test_analytics_schema.py tests\test_analytics_migration_loader.py` -> 123 passed.
- `py -m pytest -q tests\test_evidence_ledger.py tests\test_runtime_field_evidence.py` -> 128 passed.
- `py -m ruff check src tests tools` -> passed.
- `git diff --check` -> passed.
- `py tools\check_agent_docs.py` -> passed with 0 errors and 0 warnings.
- Path-scoped secret/private-marker scan over contract, handoff, `analytics_ingest.py`, and focused tests -> forbidden 0, warnings 0.
- Path-scoped protected-surface scan over contract, handoff, `analytics_ingest.py`, and focused tests -> forbidden 0, warnings 0.
- Generated SQLite artifact status check -> no changed or untracked SQLite DB, WAL, SHM, or journal artifacts found.

Follow-up confirmation validation:

- Direct runtime reproduction check -> unsafe root/local path shapes rejected with field-evidence provenance rows 0; valid parser JSON-pointer label persisted with one field-evidence provenance row.
- `py -m pytest -q tests\test_analytics_field_evidence_ingest.py` -> 29 passed.
- `py -m pytest -q tests\test_analytics_field_evidence_ingest.py tests\test_analytics_opponent_card_observation_ingest.py tests\test_analytics_gameplay_action_ingest.py tests\test_analytics_parser_normalized_replay_ingest.py tests\test_analytics_schema.py tests\test_analytics_migration_loader.py` -> 128 passed.
- `py -m pytest -q tests\test_evidence_ledger.py tests\test_runtime_field_evidence.py` -> 128 passed.
- `py -m ruff check src tests tools` -> passed.
- `git diff --check` -> passed.
- `py tools\check_agent_docs.py` -> passed.
- Path-scoped secret/private-marker scan including fixer handoff and report -> forbidden 0, warnings 0.
- Path-scoped protected-surface scan including fixer handoff and report -> forbidden 0, warnings 0.
- Generated SQLite artifact status check -> no changed or untracked SQLite DB, WAL, SHM, journal, or `data/analytics` artifacts found.

## Protected-Surface Status

No forbidden parser/runtime/workbook/webhook/App Script/protected production surfaces were touched in the reviewed field-evidence scope.

## Secret / Private-Marker Status

Static path-scoped scan found no forbidden private or secret markers. Runtime review found a blocking privacy validation gap for synthetic local path-shaped `source_payload_paths` values.

Follow-up runtime review confirmed the reviewed unsafe local path shapes are rejected before durable SQLite persistence.

## Generated SQLite Artifact Status

No generated SQLite database, WAL, SHM, or journal files were found.

## Forbidden Scope

Forbidden scope was not otherwise touched. The blocker is inside the authorized analytics field-evidence ingest validation boundary.

## Recommendation

Approve for Codex F. The prior P1 is resolved, and no new blocking findings were found in the confirmation pass.

## Next Workflow Action

Next role: Codex F: Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for analytics_field_evidence_ingest.

Branch:
codex/analytics-foundation

Contract:
docs/contracts/analytics_field_evidence_ingest.md

Implementation handoff:
docs/implementation_handoffs/analytics_field_evidence_ingest_comparison.md

Review artifact:
docs/contract_test_reports/analytics_field_evidence_ingest.md

Fixer handoff:
docs/implementation_handoffs/analytics_field_evidence_ingest_fixer.md

Submit only the reviewed field-evidence ingest package. Before staging, inspect `git status --short --branch` and stage only the intended analytics field-evidence package files.

Do not change parser/runtime/workbook/webhook/App Script behavior. Do not alter SQLite schema or create database files. Do not store raw Player.log data or touch secrets/generated/runtime artifacts. Do not target main, merge, or close issues unless explicitly asked.

Run:
py -m pytest -q tests\test_analytics_field_evidence_ingest.py
py -m pytest -q tests\test_analytics_field_evidence_ingest.py tests\test_analytics_opponent_card_observation_ingest.py tests\test_analytics_gameplay_action_ingest.py tests\test_analytics_parser_normalized_replay_ingest.py tests\test_analytics_schema.py tests\test_analytics_migration_loader.py
py -m pytest -q tests\test_evidence_ledger.py tests\test_runtime_field_evidence.py
py -m ruff check src tests tools
py tools\check_agent_docs.py
git diff --check

Also run path-scoped secret/private-marker and protected-surface checks over the changed files if available.
```

```yaml
workflow_handoff:
  role_performed: "Codex E: Module Reviewer / contract-test thread"
  completed_thread: "E"
  next_thread: "F"
  next_role: "Codex F: Module Submitter"
  branch: "codex/analytics-foundation"
  contract_artifact: "docs/contracts/analytics_field_evidence_ingest.md"
  implementation_handoff: "docs/implementation_handoffs/analytics_field_evidence_ingest_comparison.md"
  fixer_handoff: "docs/implementation_handoffs/analytics_field_evidence_ingest_fixer.md"
  review_artifact: "docs/contract_test_reports/analytics_field_evidence_ingest.md"
  findings:
    - "Prior P1 fixed: JSON-pointer compatibility no longer accepts reviewed root-level local absolute path shapes into fact_provenance.source_payload_paths."
  validation:
    - "direct runtime reproduction check -> unsafe root/local path shapes rejected with field-evidence provenance rows 0; valid parser JSON-pointer label persisted with one row"
    - "py -m pytest -q tests\\test_analytics_field_evidence_ingest.py -> 29 passed"
    - "py -m pytest -q tests\\test_analytics_field_evidence_ingest.py tests\\test_analytics_opponent_card_observation_ingest.py tests\\test_analytics_gameplay_action_ingest.py tests\\test_analytics_parser_normalized_replay_ingest.py tests\\test_analytics_schema.py tests\\test_analytics_migration_loader.py -> 123 passed"
    - "confirmation rerun of analytics/evidence validation slice after fixer -> 128 passed"
    - "py -m pytest -q tests\\test_evidence_ledger.py tests\\test_runtime_field_evidence.py -> 128 passed"
    - "py -m ruff check src tests tools -> passed"
    - "git diff --check -> passed"
    - "py tools\\check_agent_docs.py -> passed"
    - "path-scoped secret/private-marker scan -> forbidden 0, warnings 0"
    - "path-scoped protected-surface scan -> forbidden 0, warnings 0"
    - "generated SQLite artifact check -> no changed or untracked SQLite DB/journal/WAL/SHM artifacts found"
  forbidden_scope_touched: false
  remaining_risks:
    - "Full repository test suite was not run in the confirmation pass."
    - "GitHub Actions not run locally."
    - "Broader output-family coverage beyond representative analytics fact targets remains unverified."
  route: "Codex F"
```
