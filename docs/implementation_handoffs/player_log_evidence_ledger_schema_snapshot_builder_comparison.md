# Player.log Evidence Ledger Schema Snapshot Builder Implementation Handoff

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/175

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/11

## Contract

`docs/contracts/player_log_evidence_ledger_schema_snapshot_builder.md`

## Role Performed

Codex C: Module Implementer / comparison thread.

Codex D: Module Fixer follow-up for the Codex E privacy matcher gap.

## Branch And Status

- Branch: `codex/player-log-evidence-ledger-schema-snapshot-builder`
- Base branch: `codex/parser-reliability-intelligence`
- Starting status: branch matched `origin/codex/parser-reliability-intelligence` at `cc729500a6efeb832578096cc1acc06a03221ad0`; the issue #175 contract existed as an untracked source artifact.
- Ending status: added snapshot builder module, CLI wrapper, focused tests,
  committed expected snapshot fixture, and this handoff plus the untracked
  issue #175 contract source artifact. Codex D then fixed the embedded
  local-path privacy matcher gap and updated focused tests/report routing.

## Source Artifacts Inspected

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/agent_threads/module_fixer.md`
- `docs/contracts/player_log_evidence_ledger_schema_snapshot_builder.md`
- `docs/contract_test_reports/player_log_evidence_ledger_schema_snapshot_builder.md`
- `src/mythic_edge_parser/app/evidence_ledger.py`
- `tests/test_evidence_ledger.py`
- `tests/test_event_schema_snapshots.py`
- GitHub issue #175

## Current Behavior Compared To Contract

Before this pass, there was no evidence-ledger-specific schema snapshot builder, no local CLI wrapper, no focused snapshot tests, and no committed expected evidence-ledger schema snapshot fixture.

Existing parser event schema snapshots covered parser event, payload, workbook row, runtime row, sheet schema, and Apps Script parity surfaces. They did not snapshot the Player.log evidence-ledger provenance surface.

The evidence ledger already exposed the stable schema inputs named by the contract through `build_player_log_evidence_ledger()` and `validate_player_log_evidence_ledger()`. This pass observes those inputs only.

## Implementation Option Chosen

Implemented the smallest snapshot-only change authorized by the contract:

- Added `src/mythic_edge_parser/app/evidence_schema_snapshot.py`.
- Added `tools/build_evidence_schema_snapshot.py`.
- Added `tests/test_evidence_schema_snapshot.py`.
- Added `tests/fixtures/evidence_schema_snapshots/player_log_evidence_ledger_schema_snapshot.v1.json`.
- Produced this implementation handoff.

The snapshot builder projects only stable evidence-ledger schema surfaces:

- top-level ledger identity/version metadata
- privacy posture
- vocabulary values
- output family records
- entry records
- evidence signal records
- summary counts and deferred output fields
- snapshot policy and limitations

It does not read raw logs, fixture log contents, diagnostics reports, drift reports, golden replay reports, feature-equity reports, card-performance artifacts, runtime artifacts, workbook exports, generated data, live external state, secrets, or model-provider output.

## Files Changed

- `src/mythic_edge_parser/app/evidence_schema_snapshot.py`
- `tools/build_evidence_schema_snapshot.py`
- `tests/test_evidence_schema_snapshot.py`
- `tests/fixtures/evidence_schema_snapshots/player_log_evidence_ledger_schema_snapshot.v1.json`
- `docs/implementation_handoffs/player_log_evidence_ledger_schema_snapshot_builder_comparison.md`
- `docs/contract_test_reports/player_log_evidence_ledger_schema_snapshot_builder.md`

Source artifact present but not edited by this thread:

- `docs/contracts/player_log_evidence_ledger_schema_snapshot_builder.md`

## Exact Sections Added

### `src/mythic_edge_parser/app/evidence_schema_snapshot.py`

- Defines required constants:
  - `EVIDENCE_SCHEMA_SNAPSHOT_OBJECT`
  - `EVIDENCE_SCHEMA_SNAPSHOT_VERSION`
  - `EVIDENCE_SCHEMA_SNAPSHOT_COMPARISON_OBJECT`
  - `EVIDENCE_SCHEMA_SNAPSHOT_COMPARISON_VERSION`
  - `EXPECTED_EVIDENCE_SCHEMA_SNAPSHOT_PATH`
  - `UPDATE_ENV_VAR`
- Adds `build_evidence_schema_snapshot(...)`.
- Adds `compare_evidence_schema_snapshot(...)`.
- Adds `load_expected_evidence_schema_snapshot(...)`.
- Adds `write_evidence_schema_snapshot(...)`.
- Adds `main(...)`.
- Enforces deterministic JSON, stable `snapshot_id`, privacy/forbidden-content scanning, and opt-in update behavior.
- Codex D updates the local absolute path matcher so embedded `/Users/` and
  `C:\\Users\\` snippets are rejected anywhere in snapshot strings, not only at
  the beginning.
- Uses `evidence_ledger.validate_player_log_evidence_ledger(...)` before snapshot projection.

### `tools/build_evidence_schema_snapshot.py`

- Adds a thin local CLI wrapper for the module `main(...)`.

### `tests/test_evidence_schema_snapshot.py`

- Covers contracted top-level shape, stable projection fields, determinism, snapshot ID hashing, expected fixture matching, ledger validation before projection, missing/mismatched expected snapshot policy, update-mode gate, private/volatile content exclusion, comparison diffs, Tier 3 deferred `deck_state`, Tier 6/Tier 7 report boundaries, and explicit write mode.
- Codex D adds focused write-time and comparison-time regression coverage for
  embedded POSIX and Windows local profile path markers and verifies the raw
  private value is not dumped in errors or comparison output.

### Expected Snapshot Fixture

- Adds one committed deterministic expected snapshot:
  - `tests/fixtures/evidence_schema_snapshots/player_log_evidence_ledger_schema_snapshot.v1.json`
- Current snapshot ID:
  - `sha256:359bd4363318f6bbcade00042adcd759daa954bd97b76d7096cb0d8d285844f4`

## Code Changed

No parser behavior changed. The new code is local deterministic schema snapshot tooling over the existing evidence-ledger metadata.

No evidence-ledger entries, vocabulary, parser modules, parser state, router behavior, diagnostics behavior, drift behavior, golden replay behavior, feature-equity behavior, card-performance calculations, workbook schema, webhook payload, Apps Script behavior, runtime status schema, match/game identity, deduplication, analytics truth, AI truth, CI gate, merge policy, or deploy policy changed.

## Tests Changed

Added focused snapshot tests in `tests/test_evidence_schema_snapshot.py`.
Codex D added four focused privacy matcher regression cases for embedded
POSIX/Windows local profile path markers.

No existing parser, ledger, diagnostics, drift, golden replay, feature-equity, card-performance, workbook, webhook, or Apps Script tests were edited.

## Interface Changes

New local-only module/tool interface:

- `src/mythic_edge_parser/app/evidence_schema_snapshot.py`
- `tools/build_evidence_schema_snapshot.py`

New committed fixture:

- `tests/fixtures/evidence_schema_snapshots/player_log_evidence_ledger_schema_snapshot.v1.json`

The CLI supports:

- `--check`
- `--write PATH`
- `--update` only when `MYTHIC_EDGE_UPDATE_EVIDENCE_SCHEMA_SNAPSHOT=1`
- `--expected PATH`

No runtime, workbook, webhook, Apps Script, production, parser, or CI interface changed.

## Validation Run

```bash
MYTHIC_EDGE_UPDATE_EVIDENCE_SCHEMA_SNAPSHOT=1 python3 tools/build_evidence_schema_snapshot.py --update
python3 -m pytest -q tests/test_evidence_schema_snapshot.py
python3 tools/build_evidence_schema_snapshot.py --check
python3 -m pytest -q tests/test_evidence_ledger.py
python3 -m pytest -q tests/test_event_schema_snapshots.py
python3 -m pytest -q tests/test_golden_replay_harness.py tests/test_feature_equity_corpus_ratchet.py
python3 -m pytest -q tests/test_parser_diagnostics_mode.py tests/test_log_drift_sensor.py
python3 -m ruff check src tests tools
git diff --check
printf '%s\n' \
  src/mythic_edge_parser/app/evidence_schema_snapshot.py \
  tools/build_evidence_schema_snapshot.py \
  tests/test_evidence_schema_snapshot.py \
  tests/fixtures/evidence_schema_snapshots/player_log_evidence_ledger_schema_snapshot.v1.json \
  docs/contracts/player_log_evidence_ledger_schema_snapshot_builder.md \
  docs/implementation_handoffs/player_log_evidence_ledger_schema_snapshot_builder_comparison.md \
  docs/contract_test_reports/player_log_evidence_ledger_schema_snapshot_builder.md \
  | python3 tools/check_protected_surfaces.py --base origin/codex/parser-reliability-intelligence --paths-from-stdin
python3 -m pytest -q
```

Results:

- `python3 -m pytest -q tests/test_evidence_schema_snapshot.py` -> `19 passed`
- `python3 tools/build_evidence_schema_snapshot.py --check` -> status `pass`, no diff, no privacy findings
- `python3 -m pytest -q tests/test_evidence_ledger.py` -> `101 passed`
- `python3 -m pytest -q tests/test_event_schema_snapshots.py` -> `6 passed`
- `python3 -m pytest -q tests/test_golden_replay_harness.py tests/test_feature_equity_corpus_ratchet.py` -> `20 passed`
- `python3 -m pytest -q tests/test_parser_diagnostics_mode.py tests/test_log_drift_sensor.py` -> `14 passed`
- `python3 -m ruff check src tests tools` -> `All checks passed!`
- `git diff --check` -> passed with no output
- Path-scoped protected-surface check -> `changed_paths: 7`, `forbidden: 0`,
  `warnings: 0`, `result: passed`
- Full `python3 -m pytest -q` -> `979 passed`

## Protected-Surface Status

No protected parser/runtime/workbook/webhook/App Script/production surfaces were intentionally touched. The implementation diff is limited to the new snapshot module, wrapper, focused tests, expected snapshot fixture, the contract artifact, and this handoff.

## What Remains Unverified

- GitHub Actions were not run.
- Live workbook state was not checked.
- Deployed Apps Script state was not checked.
- Production behavior was not checked.
- Runtime status artifacts were not generated or checked.
- Snapshot comparison is review evidence only; it is not parser semantic correctness, CI truth, merge readiness, deploy readiness, tracker completion, or automatic baseline approval.
- Drift-report evaluation, invariant execution, runtime field-evidence attachment, and runtime/status exposure remain deferred.

## Reviewer Focus

Codex E should verify:

- The builder observes only `evidence_ledger.build_player_log_evidence_ledger()` and validates through `validate_player_log_evidence_ledger()`.
- Snapshot shape matches the contract and includes only stable schema fields.
- `snapshot_id` is deterministic and excludes the `snapshot_id` field itself from the hash.
- Expected fixture matches generated current snapshot.
- Missing or mismatched expected snapshots fail with the policy message.
- Update mode is opt-in only through `MYTHIC_EDGE_UPDATE_EVIDENCE_SCHEMA_SNAPSHOT=1`.
- The snapshot excludes timestamps, volatile runtime values, raw logs, raw payload values, local paths, runtime artifacts, failed posts, workbook exports, generated data, secrets, webhook URLs, and AI/model-provider output.
- Embedded `/Users/` and `C:\\Users\\` local path markers are rejected in both
  write-time and comparison-time privacy checks without dumping the private
  value.
- Comparison reports schema changes without dumping raw values.
- Tier 3 `deck_state` remains deferred and no fake deck-state truth is seeded.
- Tier 6 and Tier 7 report/analytics boundaries remain review/report evidence only.
- No parser/runtime/workbook/webhook/App Script behavior or protected surfaces changed.

## Next Workflow Action

Next role: Codex E: Module Reviewer / contract-test thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #175, the Player.log evidence-ledger schema snapshot builder under tracker #11.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/175

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/11

Previous issue:
https://github.com/Tahjali11/Mythic-Edge/issues/173

Previous PR:
https://github.com/Tahjali11/Mythic-Edge/pull/174

Previous merge commit:
cc729500a6efeb832578096cc1acc06a03221ad0

Base branch:
codex/parser-reliability-intelligence

Implementation branch:
codex/player-log-evidence-ledger-schema-snapshot-builder

Contract:
docs/contracts/player_log_evidence_ledger_schema_snapshot_builder.md

Implementation handoff:
docs/implementation_handoffs/player_log_evidence_ledger_schema_snapshot_builder_comparison.md

Changed files expected:
- docs/contracts/player_log_evidence_ledger_schema_snapshot_builder.md
- src/mythic_edge_parser/app/evidence_schema_snapshot.py
- tools/build_evidence_schema_snapshot.py
- tests/test_evidence_schema_snapshot.py
- tests/fixtures/evidence_schema_snapshots/player_log_evidence_ledger_schema_snapshot.v1.json
- docs/implementation_handoffs/player_log_evidence_ledger_schema_snapshot_builder_comparison.md
- docs/contract_test_reports/player_log_evidence_ledger_schema_snapshot_builder.md

Task:
Review the implementation against the #175 contract. Lead with findings ordered by severity. Verify that Codex C implemented only deterministic evidence-ledger schema snapshot tooling, focused tests, one expected snapshot fixture, and the implementation handoff, and that Codex D resolved the embedded local-path privacy matcher gap.

Check especially:
- build_evidence_schema_snapshot() returns the contracted object, schema version, snapshot version, privacy block, summary, vocabulary, output family records, entry records, evidence signal records, snapshot policy, limitations, and deterministic snapshot_id.
- The builder validates the current evidence ledger before projecting it.
- Snapshot generation is deterministic and does not mutate the source ledger.
- The committed expected snapshot matches the generated current snapshot.
- Missing expected snapshots and mismatches fail with the policy message.
- Update mode is disabled unless MYTHIC_EDGE_UPDATE_EVIDENCE_SCHEMA_SNAPSHOT=1 is set.
- The snapshot excludes timestamps, git/current branch data, local paths, raw logs, raw payload values, runtime artifacts, failed posts, workbook exports, generated data, secrets, webhook URLs, and AI/model-provider output.
- Embedded `/Users/` and `C:\\Users\\` local path markers are rejected in both write-time and comparison-time privacy checks without dumping the private value.
- Comparison reports added, removed, and changed output families, entries, evidence signals, vocabulary, and policies without raw values.
- Tier 3 deck_state remains deferred and is not seeded as fake parser truth.
- Tier 6 and Tier 7 report/analytics boundaries remain review/report evidence only, not CI, merge, deploy, workbook, analytics, model-provider, or AI truth.
- No parser behavior, parser state final reconciliation, parser event classes, router semantics, diagnostics report shape, runtime status schema, drift report implementation, invariant execution, golden replay behavior, feature-equity behavior, card-performance calculations, workbook schema, webhook payload shape, Apps Script behavior, output transport, match/game identity, deduplication, production behavior, analytics truth, AI truth, CI gates, merge policy, or deploy policy changed.

Suggested validation:
python3 -m pytest -q tests/test_evidence_schema_snapshot.py
python3 tools/build_evidence_schema_snapshot.py --check
python3 -m pytest -q tests/test_evidence_ledger.py
python3 -m pytest -q tests/test_event_schema_snapshots.py
python3 -m pytest -q tests/test_golden_replay_harness.py tests/test_feature_equity_corpus_ratchet.py
python3 -m pytest -q tests/test_parser_diagnostics_mode.py tests/test_log_drift_sensor.py
python3 -m ruff check src tests tools
git diff --check
printf '%s\n' \
  src/mythic_edge_parser/app/evidence_schema_snapshot.py \
  tools/build_evidence_schema_snapshot.py \
  tests/test_evidence_schema_snapshot.py \
  tests/fixtures/evidence_schema_snapshots/player_log_evidence_ledger_schema_snapshot.v1.json \
  docs/contracts/player_log_evidence_ledger_schema_snapshot_builder.md \
  docs/implementation_handoffs/player_log_evidence_ledger_schema_snapshot_builder_comparison.md \
  docs/contract_test_reports/player_log_evidence_ledger_schema_snapshot_builder.md \
  | python3 tools/check_protected_surfaces.py --base origin/codex/parser-reliability-intelligence --paths-from-stdin

Do not edit code in the review thread. Do not stage, commit, push, open a PR, merge, target main, close issue #175, or close tracker #11 unless explicitly asked.

Final output must include:
- role performed
- issue/tracker
- contract and handoff reviewed
- findings first
- contract matches
- contract mismatches
- missing tests or safeguards
- validation run and result
- protected-surface status
- remaining risks
- next recommended role: Codex F if no blocking findings, otherwise Codex D or Codex B
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/175"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/173"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/174"
  previous_merge_commit: "cc729500a6efeb832578096cc1acc06a03221ad0"
  completed_thread: "D"
  next_thread: "E"
  source_artifact: "docs/contract_test_reports/player_log_evidence_ledger_schema_snapshot_builder.md"
  target_artifact: "src/mythic_edge_parser/app/evidence_schema_snapshot.py; tests/test_evidence_schema_snapshot.py; docs/implementation_handoffs/player_log_evidence_ledger_schema_snapshot_builder_comparison.md; docs/contract_test_reports/player_log_evidence_ledger_schema_snapshot_builder.md"
  verdict: "fixer_pass_ready_for_module_reviewer"
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
