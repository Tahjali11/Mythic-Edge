# Analytics Field-Evidence Ingest Fixer Handoff

## Issue

Analytics foundation child work for field-evidence ingest into local SQLite.

## Branch

`codex/analytics-foundation`

## Contract

`docs/contracts/analytics_field_evidence_ingest.md`

## Review Artifact

`docs/contract_test_reports/analytics_field_evidence_ingest.md`

## Implementation Handoff Used

`docs/implementation_handoffs/analytics_field_evidence_ingest_comparison.md`

## Role Performed

Codex D: Module Fixer.

## Finding Fixed

P1: JSON-pointer compatibility accepted root-level local absolute path shapes
into `fact_provenance.source_payload_paths`.

The reviewed gap allowed values such as `/tmp`, `/Users`, `/private`, `/var`,
and slash-prefixed drive path shapes to pass as JSON-pointer-compatible labels.

## Fault Category

Implementation validation gap inside the authorized analytics field-evidence
ingest boundary.

The contract remains valid. No route-back to Codex B was needed.

## What Changed

Tightened `source_payload_paths` label validation in
`src/mythic_edge_parser/app/analytics_ingest.py`:

- local absolute path roots are now rejected both as root values and nested
  values, for example `/tmp` and `/tmp/file`;
- slash-prefixed drive-path shapes are rejected;
- valid JSON-pointer-like parser labels such as `/match_log_rows/0/match_id`
  remain accepted.

## Files Changed

- `src/mythic_edge_parser/app/analytics_ingest.py`
- `tests/test_analytics_field_evidence_ingest.py`
- `docs/implementation_handoffs/analytics_field_evidence_ingest_fixer.md`

The broader reviewed field-evidence package remains present in the working
tree:

- `docs/contracts/analytics_field_evidence_ingest.md`
- `docs/implementation_handoffs/analytics_field_evidence_ingest_comparison.md`
- `docs/contract_test_reports/analytics_field_evidence_ingest.md`
- `src/mythic_edge_parser/app/analytics_ingest.py`
- `tests/test_analytics_field_evidence_ingest.py`
- `tests/test_analytics_gameplay_action_ingest.py`
- `tests/test_analytics_opponent_card_observation_ingest.py`
- `tests/test_analytics_parser_normalized_replay_ingest.py`

## Code Changed

Runtime code changed: yes, limited to
`src/mythic_edge_parser/app/analytics_ingest.py`.

Changed sections:

- renamed the local path prefix tuple into root labels without trailing slashes;
- added a slash-prefixed drive-path regex;
- updated `_validate_safe_field_evidence_label(...)` to reject root-level local
  paths and slash-prefixed drive paths before persistence.

## Tests Added Or Updated

Updated `tests/test_analytics_field_evidence_ingest.py`.

Added regression coverage for rejected `source_payload_paths` values:

- `/tmp`
- `/Users`
- `/private`
- `/var`
- a slash-prefixed drive path shape assembled in the test without storing a
  literal private path

The existing malformed-attachment test verifies rejection leaves no partial
analytics fact or provenance rows.

## Interface Changes

None.

No public function signatures, input fields, SQLite schema, migration files,
parser outputs, workbook columns, webhook payloads, Apps Script behavior, or
environment variables changed.

## Validation Run

```powershell
direct runtime reproduction check for /tmp, /Users, /private, /var, and slash-prefixed drive shape
# all rejected; fact_provenance rows=0 for each value

py -m pytest -q tests\test_analytics_field_evidence_ingest.py
# 29 passed

py -m pytest -q tests\test_analytics_field_evidence_ingest.py tests\test_analytics_opponent_card_observation_ingest.py tests\test_analytics_gameplay_action_ingest.py tests\test_analytics_parser_normalized_replay_ingest.py tests\test_analytics_schema.py tests\test_analytics_migration_loader.py
# 128 passed

py -m pytest -q tests\test_evidence_ledger.py tests\test_runtime_field_evidence.py
# 128 passed

py -m ruff check src tests tools
# passed

git diff --check
# passed

py tools\check_agent_docs.py
# passed; errors 0, warnings 0

generated SQLite artifact check
# no changed or untracked SQLite DB/journal/WAL/SHM/data analytics artifacts found

path-scoped secret/private-marker scan over the field-evidence package
# forbidden 0, warnings 0

path-scoped protected-surface scan over the field-evidence package
# forbidden 0, warnings 0
```

## Protected-Surface Status

No forbidden parser/runtime/workbook/webhook/App Script/protected production
surfaces were touched.

## Secret And Private-Marker Status

The runtime reproduction now rejects the reviewed local path shapes before
durable SQLite persistence. The path-scoped secret/private-marker scan passed
with forbidden 0 and warnings 0 after removing literal private-path-shaped test
documentation.

## Generated SQLite Artifact Status

No generated SQLite database, WAL, SHM, journal, or `data/analytics` artifacts
were found.

## Still Unverified

- Full repository test suite.
- Live workbook state.
- Deployed Apps Script state.
- Production behavior.
- Broader output-family coverage beyond representative existing analytics fact
  targets.

## Reviewer Focus

Ask Codex E to verify:

- valid JSON-pointer-like parser labels remain accepted;
- root-level local absolute paths are rejected;
- slash-prefixed drive paths are rejected;
- rejected values leave no partial fact or provenance rows;
- no parser/runtime/workbook/webhook/App Script/protected production behavior
  changed.

## Forbidden Scope Status

Forbidden scope was not touched.

## Next Workflow Action

Next role: Codex E: Module Reviewer / confirmation thread.

```yaml
workflow_handoff:
  role_performed: "Codex D: Module Fixer"
  completed_thread: "D"
  next_thread: "E"
  next_role: "Codex E: Module Reviewer / confirmation thread"
  branch: "codex/analytics-foundation"
  contract_artifact: "docs/contracts/analytics_field_evidence_ingest.md"
  implementation_handoff: "docs/implementation_handoffs/analytics_field_evidence_ingest_comparison.md"
  review_artifact: "docs/contract_test_reports/analytics_field_evidence_ingest.md"
  fixer_handoff: "docs/implementation_handoffs/analytics_field_evidence_ingest_fixer.md"
  finding_fixed:
    - "P1: JSON-pointer compatibility accepted root-level local absolute path shapes into fact_provenance.source_payload_paths."
  validation:
    - "direct runtime reproduction check -> /tmp, /Users, /private, /var, and slash-prefixed drive shape rejected with fact_provenance rows=0"
    - "py -m pytest -q tests\\test_analytics_field_evidence_ingest.py -> 29 passed"
    - "py -m pytest -q tests\\test_analytics_field_evidence_ingest.py tests\\test_analytics_opponent_card_observation_ingest.py tests\\test_analytics_gameplay_action_ingest.py tests\\test_analytics_parser_normalized_replay_ingest.py tests\\test_analytics_schema.py tests\\test_analytics_migration_loader.py -> 128 passed"
    - "py -m pytest -q tests\\test_evidence_ledger.py tests\\test_runtime_field_evidence.py -> 128 passed"
    - "py -m ruff check src tests tools -> passed"
    - "git diff --check -> passed"
    - "py tools\\check_agent_docs.py -> passed"
    - "generated SQLite artifact check -> no changed or untracked SQLite DB/journal/WAL/SHM/data analytics artifacts found"
    - "path-scoped secret/private-marker scan -> forbidden 0, warnings 0"
    - "path-scoped protected-surface scan -> forbidden 0, warnings 0"
  forbidden_scope_touched: false
  route: "Codex E confirmation before Codex F"
```
