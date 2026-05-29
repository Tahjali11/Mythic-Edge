# Analytics Replay/View Validation Harness Implementation Handoff

## Issue

<https://github.com/Tahjali11/Mythic-Edge/issues/193>

## Tracker

<https://github.com/Tahjali11/Mythic-Edge/issues/190>

## Source Contract

`docs/contracts/analytics_replay_view_validation_harness.md`

## Role Performed

Codex C: Module Implementer.

## Branch And Starting State

- Branch: `codex/analytics-foundation`
- Starting HEAD: `81f058a`
- `HEAD...origin/codex/analytics-foundation`: `0 0`
- Live GitHub state checked: issue #193 open, tracker #190 open.
- Starting worktree contained the untracked source contract
  `docs/contracts/analytics_replay_view_validation_harness.md`.

## Implementation Summary

Compared the replay-to-view harness contract with the current analytics ingest
implementation, migration SQL views, and focused analytics tests. The contract
route is test-only, and no current contradiction required production changes.

Added a focused in-memory pytest harness that sends one compact synthetic
parser-normalized replay through `ingest_parser_normalized_replay(...)` and
then queries the derived SQL views. The harness proves the combined path:

```text
parser-normalized replay input
  -> analytics ingest
  -> SQLite fact tables
  -> derived SQL views
```

It also ingests the same replay twice into the same in-memory database and
asserts stable ingest id, row counts, table counts, selected view row identity,
and field-evidence row identity.

No parser behavior, runtime behavior, workbook schema, webhook payload shape,
Apps Script behavior, output transport, Match Journal behavior, overlay
behavior, Google Sheets behavior, AI/OpenAI behavior, CI gates, merge policy,
deploy policy, or production behavior was changed.

## Files Changed

- `tests/test_analytics_replay_view_harness.py`
- `docs/implementation_handoffs/analytics_replay_view_validation_harness_comparison.md`

Source artifact present but not edited by this thread:

- `docs/contracts/analytics_replay_view_validation_harness.md`

## Contract-To-Code Comparison

### Confirmed Matches

- The harness is test-only; no production module, CLI, default database opener,
  environment-variable contract, runtime ingest, saved replay change, golden
  replay change, Google Sheets sync, webhook sender, Apps Script interaction,
  Match Journal/overlay behavior, or model-provider interface was added.
- Tests use `sqlite3.connect(":memory:")` and inline synthetic replay data.
- The representative replay uses `source_kind = "sanitized_golden_replay"` and
  `source_artifact_label = "analytics_replay_view_harness_v1"`.
- Replay contents cover one synthetic match with two games, preboard and
  postboard labels, Play and Draw games, known win and loss rows, opening hand
  card names, `1` mulligan and `0` mulligan rows, turn counts, durations,
  queue/format/event/sync labels, two gameplay actions, one linked opponent
  observation, and one canonical field-evidence entry.
- The primary composition test calls `ingest_parser_normalized_replay(...)`
  before querying derived views; it does not directly insert parser fact rows.
- The harness queries and asserts behavior through:
  `v_opening_hand_cards`, `v_opening_lines`,
  `v_gameplay_action_review`, `v_mulligan_outcomes`,
  `v_game1_vs_postboard`, `v_play_draw_splits`,
  `v_sample_size_warnings`, and
  `v_opponent_card_observation_review`.
- Field evidence survives the replay ingest path into `fact_provenance` with
  review/degradation labels preserved.
- The idempotency test repeats the same replay and checks stable table counts,
  selected view snapshots, `row_counts`, `ingest_run_id`, and nonduplicated
  field-evidence rows.
- No generated SQLite files were created by the harness.

### Contract Mismatches Fixed

None. The implementation found no production analytics mismatch that required
changing ingest code or SQL view definitions.

### Missing Safeguards

None blocking. The harness stays in-memory and synthetic, avoids raw logs and
local paths, and includes an artifact-scan assertion around the primary test.

### Missing Or Weak Tests

No blocking gaps for this contract. Human matchup-label performance remains
covered by `tests/test_analytics_derived_views.py`; it was intentionally not
added to this parser-normalized replay harness because human labels are not
part of parser-normalized replay input.

The harness does not include unknown/degraded game-result rows. It covers
degraded/review-required opponent-observation and field-evidence labels, while
unknown/degraded game-result math remains covered by direct derived-view tests.

## Interface Changes

No public or production interface changes.

New test-only helpers are local to
`tests/test_analytics_replay_view_harness.py`.

## Validation Run

```bash
python3 -m pytest -q tests/test_analytics_replay_view_harness.py
python3 -m pytest -q tests/test_analytics_parser_normalized_replay_ingest.py tests/test_analytics_derived_views.py
python3 -m pytest -q tests/test_analytics_gameplay_action_ingest.py tests/test_analytics_opponent_card_observation_ingest.py tests/test_analytics_field_evidence_ingest.py
python3 -m pytest -q tests/test_analytics_schema.py tests/test_analytics_migration_loader.py
python3 -m ruff check src tests tools
find data -type f \( -name '*.sqlite' -o -name '*.sqlite3' -o -name '*.db' -o -name '*-wal' -o -name '*-shm' -o -name '*-journal' \) -print
git diff --check
git diff --no-index --check /dev/null docs/contracts/analytics_replay_view_validation_harness.md
git diff --no-index --check /dev/null tests/test_analytics_replay_view_harness.py
git diff --no-index --check /dev/null docs/implementation_handoffs/analytics_replay_view_validation_harness_comparison.md
printf '%s\n' \
  docs/contracts/analytics_replay_view_validation_harness.md \
  tests/test_analytics_replay_view_harness.py \
  docs/implementation_handoffs/analytics_replay_view_validation_harness_comparison.md \
  | python3 tools/check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
printf '%s\n' \
  docs/contracts/analytics_replay_view_validation_harness.md \
  tests/test_analytics_replay_view_harness.py \
  docs/implementation_handoffs/analytics_replay_view_validation_harness_comparison.md \
  | python3 tools/check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
```

Results recorded during implementation:

- `tests/test_analytics_replay_view_harness.py`: `2 passed`
- parser-normalized ingest and derived-view suite: `32 passed`
- gameplay-action, opponent-observation, and field-evidence ingest suite:
  `77 passed`
- schema and migration loader suite: `27 passed`
- Ruff: `All checks passed!`
- SQLite artifact scan: passed with no output
- `git diff --check`: passed with no output
- no-index whitespace checks for the untracked contract, test, and handoff
  files: passed with no output; `git diff --no-index` returned the expected
  diff-present status for added files
- Secret/private marker scan: `scanned_paths: 3`, `forbidden: 0`,
  `warnings: 0`, `result: passed`
- Protected-surface gate: `changed_paths: 3`, `forbidden: 0`,
  `warnings: 0`, `result: passed`

## Still Unverified

- GitHub Actions were not run.
- No live SQLite database, Match Journal, overlay, Google Sheets, workbook,
  webhook, Apps Script, AI/OpenAI, CI, merge, or deploy behavior was checked.
- The harness is representative validation evidence only; it does not decide
  parser truth, analytics truth, merge readiness, deploy readiness, gameplay
  advice, hidden-card inference, archetype classification, or AI coaching.
- Future historical replay fixtures remain deferred; this first harness uses
  inline synthetic replay data as required by the contract.

## Reviewer Focus

Codex E should focus on:

- whether the new harness truly exercises the ingest-to-view composition path
  rather than duplicating direct table-insert view tests
- whether the representative replay is compact but covers all required
  families
- whether idempotency checks prove stable fact and view rows after repeated
  ingest
- whether provenance, availability, degradation, and review labels survive
  where the current view shapes expose them
- whether the file scope remains test-only plus handoff documentation
- whether any future consumer could overread this harness as merge/deploy,
  parser-truth, AI/coaching, or analytics-truth authority

## Next Recommended Role

Codex E: Module Reviewer / Contract Tester.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / Contract Tester for issue #193, analytics replay-to-view validation harness, under tracker #190.

Context:
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/190
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/193
- Branch: codex/analytics-foundation
- Source contract: docs/contracts/analytics_replay_view_validation_harness.md
- Implementation handoff: docs/implementation_handoffs/analytics_replay_view_validation_harness_comparison.md
- Risk tier: Medium

Review:
- Verify the diff against the issue, contract, handoff, and tests.
- Lead with findings, if any.
- Confirm whether the implementation stays test-only and does not change production analytics, parser, runtime, workbook, webhook, Apps Script, Match Journal, overlay, Google Sheets, AI/OpenAI, CI, merge, or deploy behavior.
- Confirm whether tests use in-memory SQLite, inline synthetic parser-normalized replay data, the real ingest API, and derived SQL view queries.
- Confirm whether repeated ingest proves stable ingest id, row counts, fact table counts, selected view row identities, and nonduplicated field-evidence rows.
- Confirm whether the harness preserves identity, provenance, availability, degradation, and review labels where the current view shapes expose them.
- Confirm whether any validation gaps remain before Codex F.

Suggested validation:
- python3 -m pytest -q tests/test_analytics_replay_view_harness.py
- python3 -m pytest -q tests/test_analytics_parser_normalized_replay_ingest.py tests/test_analytics_derived_views.py
- python3 -m pytest -q tests/test_analytics_gameplay_action_ingest.py tests/test_analytics_opponent_card_observation_ingest.py tests/test_analytics_field_evidence_ingest.py
- python3 -m pytest -q tests/test_analytics_schema.py tests/test_analytics_migration_loader.py
- python3 -m ruff check src tests tools
- git diff --check

Do not:
- Fix code silently in review-only mode.
- Target main directly.
- Close tracker #190.
- Create or commit SQLite database files, WAL, SHM, journal files, raw logs, generated data, runtime artifacts, failed posts, workbook exports, secrets, credentials, API keys, tokens, or webhook URLs.
- Store raw Player.log payloads in SQLite.
- Change parser/runtime/workbook/webhook/App Script/AI/OpenAI/Match Journal/overlay/Google Sheets behavior.
- Let analytics views or analytics harnesses become parser truth, merge readiness, deploy readiness, gameplay advice, player-mistake labels, hidden-card inference, archetype classification, or AI coaching.
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/193"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/190"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/analytics_replay_view_validation_harness.md"
  target_artifact: "docs/implementation_handoffs/analytics_replay_view_validation_harness_comparison.md"
  verdict: "implementation_ready_for_review"
  risk_tier: "Medium"
  branch: "codex/analytics-foundation"
  validation:
    - "python3 -m pytest -q tests/test_analytics_replay_view_harness.py -> 2 passed"
    - "python3 -m pytest -q tests/test_analytics_parser_normalized_replay_ingest.py tests/test_analytics_derived_views.py -> 32 passed"
    - "python3 -m pytest -q tests/test_analytics_gameplay_action_ingest.py tests/test_analytics_opponent_card_observation_ingest.py tests/test_analytics_field_evidence_ingest.py -> 77 passed"
    - "python3 -m pytest -q tests/test_analytics_schema.py tests/test_analytics_migration_loader.py -> 27 passed"
    - "python3 -m ruff check src tests tools -> passed"
    - "SQLite artifact scan -> passed with no output"
    - "git diff --check -> passed"
    - "no-index whitespace checks for untracked contract/test/handoff files -> passed with no output"
    - "path-scoped secret/private marker scan -> passed"
    - "path-scoped protected-surface gate -> passed"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close tracker #190."
    - "Do not create or commit SQLite database files, WAL, SHM, journal files, raw logs, generated data, runtime artifacts, failed posts, workbook exports, secrets, credentials, API keys, tokens, or webhook URLs."
    - "Do not store raw Player.log payloads in SQLite."
    - "Do not change parser/runtime/workbook/webhook/App Script/AI/OpenAI/Match Journal/overlay/Google Sheets behavior."
    - "Do not let analytics views or analytics harnesses become parser truth, merge readiness, deploy readiness, gameplay advice, player-mistake labels, hidden-card inference, archetype classification, or AI coaching."
```
