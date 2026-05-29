# Match Journal Service Contract Test Report

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/200

Previous issue:

- https://github.com/Tahjali11/Mythic-Edge/issues/198

Previous PR:

- https://github.com/Tahjali11/Mythic-Edge/pull/199

Prior Match Journal foundation:

- https://github.com/Tahjali11/Mythic-Edge/issues/196
- https://github.com/Tahjali11/Mythic-Edge/pull/197

## Tracker

N/A. No dedicated Match Journal tracker is currently open.

## Contract

- `docs/contracts/match_journal_service.md`
- `docs/agent_constitution.md`
- `docs/agent_threads/contract_test.md`
- `docs/templates/contract_test_report.md`

## Implementation Under Test

Branch:

```text
codex/match-journal-service
```

Base:

```text
main
```

Changed-file scope reviewed:

- `docs/contracts/match_journal_service.md`
- `docs/implementation_handoffs/match_journal_service_comparison.md`
- `src/mythic_edge_parser/app/match_journal_service.py`
- `tests/test_match_journal_service.py`

## Report Lifecycle

`report_lifecycle`: `final_approval`

## Findings First

No blocking findings remain after Codex E re-review. MJSVC-E-001 is verified
fixed: invalid service command values are rejected before attachment context
resolution can create journal match/game containers.

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MJSVC-E-001 | High | `fixed_state_followup` | Service validation failures are rejected before attachment containers are created. | not_blocking | Original Codex E repro showed `record_match_note({"parser_match_id": ...}, ..., note_format="not_allowed")` and `propose_display_correction({"parser_match_id": ...}, {"target_surface": "not_allowed", ...})` raising `MatchJournalServiceValidationError` after creating `journal_matches` rows. | Codex E re-ran the direct repro after Codex D's fix: invalid `note_format` and invalid `target_surface` both raised `MatchJournalServiceValidationError` with `journal_matches before=0 after=0`. Focused service tests cover invalid `note_format`, invalid/missing display-correction values, invalid `flag_status`, and invalid common option values without partial journal rows. | F |

## Contract Summary

The Match Journal service must provide a narrow local human-intent boundary over
the Match Journal repository. It packages common journal actions, keeps parser
IDs as caller-provided references only, preserves unattached notes, keeps
pilot-error status and reason separately queryable, keeps display corrections
`journal_display_only`, and avoids parser/runtime/status/analytics/overlay/
Sheets/workbook/webhook/App Script/OpenAI behavior changes.

## Checks Run

```bash
git status --short --branch
git fetch --prune
gh issue view 200 --repo Tahjali11/Mythic-Edge --json number,title,state,body,labels,comments
python3 -m pytest -q tests/test_match_journal_service.py
python3 -m pytest -q tests/test_match_journal_schema.py
python3 -m pytest -q tests/test_match_journal_repository.py
python3 -m pytest -q tests/test_analytics_schema.py tests/test_analytics_replay_view_harness.py
PYTHONPATH=src python3 - <<'PY'
import sqlite3
from mythic_edge_parser.app.match_journal_repository import MatchJournalRepository, ensure_match_journal_schema
from mythic_edge_parser.app.match_journal_service import MatchJournalService, MatchJournalServiceValidationError

connection = sqlite3.connect(':memory:')
connection.row_factory = sqlite3.Row
ensure_match_journal_schema(connection)
service = MatchJournalService(MatchJournalRepository(connection))

cases = [
    (
        'record_match_note invalid note_format',
        lambda: service.record_match_note({'parser_match_id': 'parser-match-note'}, 'Synthetic note', note_format='not_allowed'),
    ),
    (
        'propose_display_correction invalid target_surface',
        lambda: service.propose_display_correction(
            {'parser_match_id': 'parser-match-override'},
            {'target_surface': 'not_allowed', 'target_field': 'review', 'proposed_value_label': 'x'},
        ),
    ),
]
for name, operation in cases:
    before = connection.execute('SELECT COUNT(*) AS count FROM journal_matches').fetchone()['count']
    try:
        operation()
    except MatchJournalServiceValidationError as exc:
        after = connection.execute('SELECT COUNT(*) AS count FROM journal_matches').fetchone()['count']
        print(f'{name}: raised {type(exc).__name__}; journal_matches before={before} after={after}')
    else:
        after = connection.execute('SELECT COUNT(*) AS count FROM journal_matches').fetchone()['count']
        print(f'{name}: no error; journal_matches before={before} after={after}')
PY
python3 -m ruff check src tests tools
git diff --check
printf '%s\n' docs/contracts/match_journal_service.md docs/contract_test_reports/match_journal_service.md docs/implementation_handoffs/match_journal_service_comparison.md src/mythic_edge_parser/app/match_journal_service.py tests/test_match_journal_service.py | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' docs/contracts/match_journal_service.md docs/contract_test_reports/match_journal_service.md docs/implementation_handoffs/match_journal_service_comparison.md src/mythic_edge_parser/app/match_journal_service.py tests/test_match_journal_service.py | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
find . -path './.git' -prune -o \( -name '*.sqlite' -o -name '*.sqlite3' -o -name '*.db' -o -name '*.sqlite-wal' -o -name '*.sqlite-shm' -o -name '*.sqlite-journal' \) -print
git diff --cached --name-only
python3 -m pytest -q
```

## Results

- `python3 -m pytest -q tests/test_match_journal_service.py` passed:
  21 passed.
- `python3 -m pytest -q tests/test_match_journal_schema.py` passed:
  23 passed.
- `python3 -m pytest -q tests/test_match_journal_repository.py` passed:
  18 passed.
- `python3 -m pytest -q tests/test_analytics_schema.py tests/test_analytics_replay_view_harness.py`
  passed: 14 passed.
- Direct partial-write repro passed after the fix:
  invalid `note_format` and invalid `target_surface` both raised
  `MatchJournalServiceValidationError` with `journal_matches before=0 after=0`.
- `python3 -m ruff check src tests tools` passed.
- `git diff --check` passed with no output.
- No-index whitespace checks for the five untracked #200 files passed with no
  whitespace-error output.
- Path-scoped secret/private marker scan passed: scanned 5 paths, forbidden 0,
  warnings 0.
- Path-scoped protected-surface gate passed: changed paths 5, forbidden 0,
  warnings 0.
- Local generated SQLite artifact scan printed no matching artifacts.
- `git diff --cached --name-only` printed no staged files.
- `python3 -m pytest -q` passed:
  1412 passed.

## Confirmed Contract Matches

- `MATCH_JOURNAL_SERVICE_VERSION` is present and equals
  `match_journal_service.v1`.
- Public service error classes are present.
- `MatchJournalService` accepts an existing `MatchJournalRepository`.
- `MatchJournalService.from_connection` uses caller-owned SQLite connections
  and only ensures schema when explicitly requested.
- Service construction does not open a default Match Journal database path,
  read environment variables, or create files.
- Service operations are implemented for match, game, sideboarding, and
  unattached notes.
- Service operations are implemented for experiment labels, pilot-error status,
  pilot-error reason, manual opponent labels, review flags, display-only
  corrections, and local journal bundles.
- Parser match/game IDs remain caller-provided references and are not generated
  by the service.
- Duplicate parser-match mappings raise a service conflict error.
- Explicit missing journal match/game IDs raise service not-found errors.
- Unattached notes are preserved.
- Pilot-error status and reason remain separately queryable in the covered
  happy path.
- Opponent archetype/tier labels are manual labels and not classifier output.
- Display corrections are constrained to `journal_display_only` when the
  effect scope is supplied.
- `get_journal_bundle` reads Match Journal repository data only in the covered
  test path.
- No Match Journal schema or repository public behavior change was observed.
- `journal_sheet_sync_queue` remains deferred.
- No generated SQLite/local/private artifact was found.

## Contract Mismatches

None remain after the Codex D fixer update.

Codex D fixed MJSVC-E-001 by prevalidating service-owned option values and
display-correction request values before `_resolve_attachment_context(...,
allow_create=True)` can create journal match/game containers.

## Missing Tests

No focused gap remains for MJSVC-E-001 in the Codex D fixer pass.

Added service tests prove invalid downstream command values with parser context
do not create `journal_matches`, `journal_games`, notes, labels, review flags,
reference values, or field overrides.

## Drift Notes

- Repo drift: none found beyond the intended four-file #200 scope plus this
  contract-test report.
- Workbook drift: none found.
- Deployment drift: none found.
- Local-data drift: none found; no SQLite database artifacts were printed by
  the local artifact scan.
- Issue lifecycle drift: none found; issue #200 is open.
- PR lifecycle drift: no PR was reviewed in this Codex E pass.
- Tracker drift: no dedicated Match Journal tracker is currently open.

## Recommendation

Route to Codex F: Module Submitter.

The original blocking partial-write mismatch has a focused service-owned fix,
regression coverage, and passing Codex E validation. The module can move to
submitter custody.

## Next Workflow Action

Next role: Codex F: Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #200, Match Journal local service/use-case boundary.

Context:
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/200
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/198
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/199
- Branch: codex/match-journal-service
- Base: main
- Contract: docs/contracts/match_journal_service.md
- Contract-test report: docs/contract_test_reports/match_journal_service.md
- Implementation handoff: docs/implementation_handoffs/match_journal_service_comparison.md

Goal:
Prepare the reviewed #200 Match Journal service package for submitter handoff without merging or closing the issue.

Codex E verdict:
- No blocking findings remain.
- MJSVC-E-001 is verified fixed.
- Invalid service command values are rejected before context container creation.
- Invalid `note_format` and invalid/missing display-correction values do not leave partial rows.
- No Match Journal schema, repository public API, parser/runtime/workbook/webhook/App Script/analytics/overlay/AI behavior drift was found.

Validation:
- python3 -m pytest -q tests/test_match_journal_service.py
- python3 -m pytest -q tests/test_match_journal_schema.py
- python3 -m pytest -q tests/test_match_journal_repository.py
- python3 -m pytest -q tests/test_analytics_schema.py tests/test_analytics_replay_view_harness.py
- python3 -m ruff check src tests tools
- git diff --check
- path-scoped secret/private marker check for the changed #200 files
- path-scoped protected-surface check for the changed #200 files
- python3 -m pytest -q

Do not:
- Change Match Journal schema or repository public behavior unless routed back to Codex B.
- Create or commit SQLite/generated/private/runtime artifacts.
- Change parser behavior, parser state final reconciliation, parser event classes, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, output transport, analytics ingest, analytics views, production behavior, Google Sheets sync behavior, overlay behavior, OpenAI/model-provider behavior, or AI/coaching behavior.
- Let Match Journal records, service result shapes, or bundles become parser truth, analytics truth, gameplay advice, hidden-card inference, archetype classification, player-mistake labels, merge readiness, deploy readiness, or AI coaching.
- Merge or close issue #200 unless the approved deployer workflow explicitly authorizes it.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/200"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/198"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/199"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contracts/match_journal_service.md"
  target_artifact: "docs/contract_test_reports/match_journal_service.md"
  verdict: "no_blocking_findings_ready_for_module_submitter"
  risk_tier: "Medium-High"
  base_branch: "main"
  branch: "codex/match-journal-service"
  validation:
    - "python3 -m pytest -q tests/test_match_journal_service.py -> 21 passed"
    - "python3 -m pytest -q tests/test_match_journal_schema.py -> 23 passed"
    - "python3 -m pytest -q tests/test_match_journal_repository.py -> 18 passed"
    - "python3 -m pytest -q tests/test_analytics_schema.py tests/test_analytics_replay_view_harness.py -> 14 passed"
    - "direct partial-write repro -> validation errors with journal_matches before=0 after=0"
    - "python3 -m ruff check src tests tools -> passed"
    - "git diff --check -> passed with no output"
    - "no-index whitespace checks for untracked #200 files -> passed with no output"
    - "path-scoped secret/private marker scan -> passed, scanned 5 paths, forbidden 0, warnings 0"
    - "path-scoped protected-surface gate -> passed, changed paths 5, forbidden 0, warnings 0"
    - "local generated SQLite artifact scan -> no output"
    - "git diff --cached --name-only -> no staged files"
    - "python3 -m pytest -q -> 1412 passed"
  stop_conditions:
    - "Do not change Match Journal service behavior during submitter custody unless a submitter preflight finds a concrete blocker and routes back to Codex D or Codex B."
    - "Do not change Match Journal schema or repository public behavior unless routed back to Codex B."
    - "Do not create or commit SQLite/generated/private/runtime artifacts."
    - "Do not change parser behavior, parser state final reconciliation, parser event classes, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, output transport, analytics ingest, analytics views, production behavior, Google Sheets sync behavior, overlay behavior, OpenAI/model-provider behavior, or AI/coaching behavior."
    - "Do not let Match Journal records, service result shapes, or bundles become parser truth, analytics truth, gameplay advice, hidden-card inference, archetype classification, player-mistake labels, merge readiness, deploy readiness, or AI coaching."
    - "Do not merge or close issue #200 unless the approved deployer workflow explicitly authorizes it."
```
