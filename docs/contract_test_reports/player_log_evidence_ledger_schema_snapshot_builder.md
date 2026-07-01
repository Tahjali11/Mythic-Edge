# Player.log Evidence Ledger Schema Snapshot Builder Contract Test Report

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/175

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/11

## Contract

- `docs/contracts/player_log_evidence_ledger_schema_snapshot_builder.md`
- `docs/agent_constitution.md`
- `docs/agent_threads/contract_test.md`
- `docs/templates/contract_test_report.md`

## Implementation Under Test

Branch/worktree:

- `codex/player-log-evidence-ledger-schema-snapshot-builder`
- `/Users/<redacted>/Documents/New project/Mythic-Edge-issue-175`

Changed/untracked files reviewed:

- `docs/contracts/player_log_evidence_ledger_schema_snapshot_builder.md`
- `src/mythic_edge_parser/app/evidence_schema_snapshot.py`
- `tools/build_evidence_schema_snapshot.py`
- `tests/test_evidence_schema_snapshot.py`
- `tests/fixtures/evidence_schema_snapshots/player_log_evidence_ledger_schema_snapshot.v1.json`
- `docs/implementation_handoffs/player_log_evidence_ledger_schema_snapshot_builder_comparison.md`
- `docs/contract_test_reports/player_log_evidence_ledger_schema_snapshot_builder.md`

## Contract Summary

Issue #175 authorizes deterministic, local, evidence-ledger-specific schema
snapshot tooling only. The builder may project stable evidence-ledger metadata
into one committed sanitized snapshot fixture and compare the generated current
snapshot with the expected fixture. It must not change parser behavior,
runtime behavior, diagnostics/drift/golden replay/feature-equity behavior,
workbook or webhook shape, Apps Script behavior, CI/merge/deploy policy,
production behavior, analytics truth, AI truth, or protected surfaces. Snapshot
comparison remains review evidence only.

## Findings

No blocking findings remain.

### Resolved By Codex D And Confirmed By Codex E

1. `src/mythic_edge_parser/app/evidence_schema_snapshot.py:49` previously only matched
   private local path markers at the beginning of a string. The contract
   requires forbidden/volatile snippet coverage for `"/Users/"` and
   `"C:\\Users\\"` in snapshot content (`docs/contracts/player_log_evidence_ledger_schema_snapshot_builder.md:471`).
   Codex D removed the start-of-string anchoring and added focused write-time
   and comparison-time tests for embedded POSIX and Windows profile path
   markers.

   Reviewer repro:

   ```bash
   python3 - <<'PY'
   import sys
   from pathlib import Path
   sys.path.insert(0, 'src')
   from mythic_edge_parser.app import evidence_schema_snapshot as s
   for value in ('/Users/example/private.py',
                 'repo note /Users/example/private.py',
                 'C:\\Users\\Example Name\\private.py',
                 'prefix C:\\Users\\Example Name\\private.py'):
       snapshot = s.build_evidence_schema_snapshot()
       snapshot['entries'][0]['parser_owner'] = value
       try:
           s.write_evidence_schema_snapshot(Path('/tmp/mythic_edge_review_snapshot.json'), snapshot)
       except ValueError:
           print(f'{value!r}: rejected')
       else:
           print(f'{value!r}: accepted')
   PY
   ```

   Original result:

   ```text
   '/Users/example/private.py': rejected
   'repo note /Users/example/private.py': accepted
   'C:\\Users\\Example Name\\private.py': rejected
   'prefix C:\\Users\\Example Name\\private.py': accepted
   ```

   Codex D result:

   ```text
   '/Users/example/private.py': rejected; raw_value_in_error=False
   'repo note /Users/example/private.py': rejected; raw_value_in_error=False
   'C:\\Users\\Example Name\\private.py': rejected; raw_value_in_error=False
   'prefix C:\\Users\\Example Name\\private.py': rejected; raw_value_in_error=False
   ```

   Any snapshot or expected-snapshot value containing these private local path
   markers now produces a privacy finding without printing the private value.
   Codex E re-ran the repro and confirmed all four leading/embedded POSIX and
   Windows path cases are rejected with `raw_value_in_error=False`.

## Confirmed Contract Matches

- `build_evidence_schema_snapshot()` returns the contracted top-level object,
  schema version, snapshot version, source/parent issues, privacy block,
  summary block, vocabulary, output families, entries, evidence signals,
  snapshot policy, limitations, and deterministic `snapshot_id`.
- The builder validates the current evidence ledger before projection.
- Snapshot generation is deterministic and does not mutate the source ledger.
- The committed expected fixture matches the generated current snapshot.
- Missing expected snapshots and snapshot mismatches fail the check path with
  the policy message.
- Update mode is disabled unless
  `MYTHIC_EDGE_UPDATE_EVIDENCE_SCHEMA_SNAPSHOT=1`.
- The comparison object reports added, removed, and changed output families,
  entries, evidence signals, vocabulary, and policies by stable identifiers
  rather than dumping raw values.
- Tier 3 `deck_state` remains deferred; no fake `deck_state` truth is seeded.
- Tier 6 and Tier 7 report/analytics boundaries remain review/report evidence
  only.
- The implementation is additive: no existing parser, parser state, router,
  diagnostics, drift, golden replay, feature-equity, workbook, webhook, Apps
  Script, CI, merge/deploy, production, analytics, or AI behavior files were
  changed.

## Contract Mismatches

- Resolved: embedded POSIX/Windows local path snippets are now rejected by the
  write-time and comparison-time privacy matcher.

## Missing Tests Or Safeguards

- Resolved: focused coverage now rejects embedded local path markers such as
  `"prefix /Users/example/private.py"` and
  `"prefix C:\\Users\\Example Name\\private.py"` in both write-time and
  comparison-time privacy checks, without dumping raw private values.

## Validation Run

```bash
python3 -m pytest -q tests/test_evidence_schema_snapshot.py
python3 tools/build_evidence_schema_snapshot.py --check
python3 -m pytest -q tests/test_evidence_ledger.py
python3 -m pytest -q tests/test_event_schema_snapshots.py
python3 -m pytest -q tests/test_golden_replay_harness.py tests/test_feature_equity_corpus_ratchet.py
python3 -m pytest -q tests/test_parser_diagnostics_mode.py tests/test_log_drift_sensor.py
python3 -m ruff check src tests tools
git diff --check
printf '%s\n' \
  docs/contracts/player_log_evidence_ledger_schema_snapshot_builder.md \
  src/mythic_edge_parser/app/evidence_schema_snapshot.py \
  tools/build_evidence_schema_snapshot.py \
  tests/test_evidence_schema_snapshot.py \
  tests/fixtures/evidence_schema_snapshots/player_log_evidence_ledger_schema_snapshot.v1.json \
  docs/implementation_handoffs/player_log_evidence_ledger_schema_snapshot_builder_comparison.md \
  docs/contract_test_reports/player_log_evidence_ledger_schema_snapshot_builder.md \
  | python3 tools/check_protected_surfaces.py --base origin/codex/parser-reliability-intelligence --paths-from-stdin
python3 -m pytest -q
```

Results:

- `tests/test_evidence_schema_snapshot.py` -> 19 passed.
- `tools/build_evidence_schema_snapshot.py --check` -> status `pass`.
- `tests/test_evidence_ledger.py` -> 101 passed.
- `tests/test_event_schema_snapshots.py` -> 6 passed.
- `tests/test_golden_replay_harness.py tests/test_feature_equity_corpus_ratchet.py` -> 20 passed.
- `tests/test_parser_diagnostics_mode.py tests/test_log_drift_sensor.py` -> 14 passed.
- `python3 -m ruff check src tests tools` -> All checks passed.
- `git diff --check` -> passed with no output.
- Path-scoped protected-surface check -> changed_paths 7, forbidden 0,
  warnings 0, result passed.
- Full `python3 -m pytest -q` -> 979 passed.

## Drift Notes

- Repo drift: no unrelated tracked file changes found. The implementation
  artifacts are currently untracked in the issue #175 worktree and should be
  staged only by the appropriate submitter/fixer workflow after review.
- Workbook drift: none found.
- Webhook/App Script drift: none found.
- Parser/runtime drift: none found.
- Local-data drift: none found; no raw logs, failed posts, runtime status
  files, generated data, workbook exports, secrets, webhook URLs, or local
  runtime artifacts were included in the reviewed file set.
- Tracker drift: tracker #11 remains open, as expected.

## Recommendation

Approve for submitter workflow.

Next role: Codex F / Module Submitter.

Codex F should stage only the reviewed issue #175 files, keep the PR targeted
to `codex/parser-reliability-intelligence`, and preserve tracker #11 as open.

## workflow_handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/175"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/173"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/174"
  previous_merge_commit: "cc729500a6efeb832578096cc1acc06a03221ad0"
  completed_thread: "E"
  next_thread: "F"
  source_artifact: "docs/contract_test_reports/player_log_evidence_ledger_schema_snapshot_builder.md"
  target_artifact: "draft PR for issue #175 targeting codex/parser-reliability-intelligence"
  verdict: "no_blocking_findings_ready_for_codex_f"
  risk_tier: "High"
  base_branch: "codex/parser-reliability-intelligence"
  implementation_branch: "codex/player-log-evidence-ledger-schema-snapshot-builder"
  validation:
    - "python3 -m pytest -q tests/test_evidence_schema_snapshot.py -> 19 passed"
    - "python3 tools/build_evidence_schema_snapshot.py --check -> status pass"
    - "python3 -m pytest -q tests/test_evidence_ledger.py -> 101 passed"
    - "python3 -m pytest -q tests/test_event_schema_snapshots.py -> 6 passed"
    - "python3 -m pytest -q tests/test_golden_replay_harness.py tests/test_feature_equity_corpus_ratchet.py -> 20 passed"
    - "python3 -m pytest -q tests/test_parser_diagnostics_mode.py tests/test_log_drift_sensor.py -> 14 passed"
    - "python3 -m ruff check src tests tools -> All checks passed"
    - "git diff --check -> passed"
    - "path-scoped protected-surface check -> changed_paths 7, forbidden 0, warnings 0, result passed"
    - "python3 -m pytest -q -> 979 passed"
  stop_conditions:
    - "Do not close issue #11."
    - "Do not target main directly."
    - "Do not change parser behavior, parser state final reconciliation, parser event classes, router semantics, diagnostics report shape, runtime status schema, drift report implementation, invariant execution, golden replay behavior, feature-equity behavior, card-performance calculations, workbook schema, webhook payload shape, Apps Script behavior, output transport, ActionLogRow shape, match/game identity, deduplication, Match Journal behavior, overlay behavior, SQLite behavior, Google Sheets sync behavior, production behavior, analytics truth, AI truth, OpenAI/model-provider behavior, CI gates, merge policy, deploy policy, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, or local runtime artifacts."
    - "Do not implement drift report evaluation, invariant execution, runtime field-evidence attachment, diagnostics/golden replay/feature-equity integration, runtime status exposure, CI gates, merge/deploy gates, or automatic issue generation."
    - "Do not infer hidden cards, complete decklists, classify archetypes, provide gameplay advice, create sideboarding recommendations, label player mistakes, or move analytics/AI truth into parser truth."
    - "Do not commit raw private Player.log excerpts, raw local analytics artifacts, raw payload values, local runtime artifacts, runtime status files, failed posts, workbook exports, API keys, tokens, credentials, webhook URLs, generated data, or local paths."
    - "Do not auto-update snapshots without explicit issue, contract, and review approval."
```
