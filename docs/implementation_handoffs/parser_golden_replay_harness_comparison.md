# Parser Golden Replay Harness Implementation Comparison

Issue: https://github.com/Tahjali11/Mythic-Edge/issues/48

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/47

Related evidence/resilience issue: https://github.com/Tahjali11/Mythic-Edge/issues/11

Branch: `codex/parser-reliability-intelligence`

Source artifact: `docs/contracts/parser_golden_replay_harness.md`

Implementation role: Codex C, Module Implementer

Risk tier: High

## Summary

Implemented the v1 deterministic local golden replay harness requested by the
contract. The harness replays explicit sanitized Player.log fixture slices
through `LineBuffer`, `Router`, parser modules, transforms, diagnostics
evidence, and parser state, then compares observed parser-owned outputs against
explicit reduced expected manifests.

No parser behavior, parser state final reconciliation, workbook schema, webhook
payload shape, Apps Script behavior, output transport, parser event classes,
match/game identity, deduplication, secrets, environment variables, raw logs,
generated data, runtime status files, failed posts, or workbook exports were
changed.

## Confirmed Matches

- Contract source artifact exists at `docs/contracts/parser_golden_replay_harness.md`.
- New harness module exists at `src/mythic_edge_parser/app/golden_replay.py`.
- Focused tests exist at `tests/test_golden_replay_harness.py`.
- Explicit expected manifests exist under `tests/fixtures/golden_replay/`.
- Harness public API provides:
  - `build_golden_replay_report(manifest_paths)`
  - `run_golden_replay(manifest_path)`
  - `main(argv=None)`
- CLI entrypoint works with:
  - `python3 -m mythic_edge_parser.app.golden_replay tests/fixtures/golden_replay`
- Inputs are explicit manifest files or manifest directories; the harness does
  not read private local Player.log paths implicitly.
- Fixture paths must be repo-relative, non-absolute, and stay under the project
  root.
- Manifest privacy fields are required before replay.
- Manifest comparison uses reduced expected facts rather than broad whole-object
  snapshots.
- Report object follows `mythic_edge_golden_replay_report` /
  `parser_golden_replay_report.v1`.
- Fixture result statuses are `pass`, `degraded`, `review`, `diff`, and `fail`.
- Suite status precedence is `fail`, `diff`, `review`, `degraded`, `pass`.
- CLI exits nonzero for `fail`, `diff`, and unexpected `review`.
- Expected `degraded` outcomes are explicitly metadata-declared as exit code 0
  for v1.
- No bless/update mode was added.
- Generated reports are written only when `--out` is explicitly supplied.
- Diagnostics mode is reused as observer evidence and does not replace
  parser-owned expected facts.
- Saved-event replay remains separate and is not used as a raw log replay
  substitute.

## Contract Mismatches Fixed

- No dedicated golden replay harness existed before this implementation.
- No machine-readable manifest layer existed for committed parser regression
  slices.
- Existing parser regression snapshots were broad useful oracles, but did not
  separate privacy metadata, coverage, expected degradation, diagnostics
  evidence, parser state, final reconciliation, and selected parser-owned rows.
- Existing fixture sanitization labels were comments only; the new manifests add
  machine-readable sanitization status and privacy fields.

## Missing Safeguards Added

- Rejects malformed manifest object/schema/version fields.
- Rejects missing linked issue or contract authorization fields.
- Rejects invalid source kind, sanitization status, privacy class, and
  `raw_private_log_committed != false`.
- Rejects absolute fixture paths and parent traversal.
- Rejects unreadable fixture paths without searching private local paths.
- Scans manifest and fixture text for narrow forbidden private marker patterns
  and reports only category labels, not raw fixture lines or full marker values.
- Uses an empty deterministic fixture card lookup during replay so golden replay
  does not depend on ignored/generated local card catalog data.
- Resets parser runtime state before and after each replay.
- Compares only manifest-listed expected fields, including reduced nested list
  items, so extra observed parser fields do not silently become new manifest
  obligations.

## Missing Or Weak Tests Added

- Passing suite over the committed Bo1 and Bo3 manifests.
- Reduced expected manifest diff reporting with JSON pointer and truth layer.
- Required privacy field failure before replay.
- Absolute/private fixture path rejection.
- Legacy/unclassified fixture metadata producing `review`.
- Forbidden fixture content failure without raw marker leakage in reports.
- CLI directory discovery and explicit local report output.
- CLI nonzero behavior for review status.
- CLI explicit input requirement.

## Changes Made

- Added `src/mythic_edge_parser/app/golden_replay.py`.
- Added `tests/test_golden_replay_harness.py`.
- Added `tests/fixtures/golden_replay/bo1_match_win_basic.manifest.json`.
- Added `tests/fixtures/golden_replay/bo3_sideboard_match_loss.manifest.json`.
- Added this handoff artifact.

## Validation Evidence

Commands run:

```bash
python3 -m pytest -q tests/test_golden_replay_harness.py
```

Result: `9 passed`.

```bash
python3 -m pytest -q tests/test_parser_regressions.py tests/test_parser_diagnostics_mode.py tests/test_saved_event_replay.py
```

Result: `38 passed`.

```bash
python3 -m ruff check src tests tools
```

Result: passed.

```bash
git diff --check
```

Result: passed.

```bash
python3 tools/check_protected_surfaces.py --base origin/main
```

Result: passed with 4 warnings on pre-existing branch changes relative to
`origin/main`: `src/mythic_edge_parser/app/transforms.py`,
`src/mythic_edge_parser/events.py`,
`src/mythic_edge_parser/parsers/__init__.py`, and
`src/mythic_edge_parser/parsers/truncation.py`.

```bash
printf '%s\n' src/mythic_edge_parser/app/golden_replay.py tests/test_golden_replay_harness.py tests/fixtures/golden_replay/bo1_match_win_basic.manifest.json tests/fixtures/golden_replay/bo3_sideboard_match_loss.manifest.json docs/contracts/parser_golden_replay_harness.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
```

Result: passed with 0 warnings.

```bash
python3 -m mythic_edge_parser.app.golden_replay tests/fixtures/golden_replay
```

Result: `Golden replay: pass (2 manifests, 2 pass, 0 degraded, 0 review, 0 diff, 0 fail)`.

Additional broader check run:

```bash
python3 -m pytest -q
```

Result: `704 passed`.

## Still-Unverified Layers

- `tools/check_secret_patterns.py` is not present on this branch, so no
  branch-native content scanner was run.
- `tools/select_validation.py` is not present on this branch.
- Live MTGA logs, live workbooks, Apps Script, webhook delivery, runtime status
  files, failed posts, generated data, and workbook exports were intentionally
  not queried or mutated.
- The committed manifests currently reuse existing sanitized regression slice
  fixtures rather than introducing new raw fixture slice files.

## Open Risks

- The v1 forbidden-content scanner is intentionally narrow and should not be
  treated as a full secret scanner.
- `git diff --check` does not include untracked files until they are added to
  the index; focused tests, Ruff, CLI execution, and the stdin protected-surface
  check were used to validate the new untracked implementation files.
- The golden replay manifests compare reduced parser-owned facts. Existing broad
  regression snapshots remain valuable separate coverage.
- The harness seeds an empty fixture card lookup to avoid generated local data,
  so opening-hand names are not a v1 golden assertion. Opening-hand size and
  parser-owned row fields are covered.

## Unrelated Local Files Observed

Unrelated untracked files remain outside this module:

- `docs/.DS_Store`
- `docs/contract_test_reports/repo_wide_hardening_orchestrator_local_full.md`
- `docs/contracts/repo_wide_llm_advisory_review_scaffold.md`
- `docs/implementation_handoffs/repo_wide_llm_advisory_review_scaffold_comparison.md`

The source contract `docs/contracts/parser_golden_replay_harness.md` is also
untracked in this checkout and is in scope for issue #48.

## Next Recommended Role

Codex E: Module Reviewer in contract-test mode.

If Codex E finds no blocking issues, proceed to Codex F: Module Submitter. If
Codex E finds implementation defects, route to Codex D: Module Fixer. If Codex
E finds contract ambiguity, route back to Codex B: Module Contract Writer.

## Pasteable Next-Thread Prompt

```yaml
prompt: |
  Use the Mythic Edge agent constitution.
  Use $mythic-edge-workflow.

  Act as Codex E: Module Reviewer in contract-test mode for issue #48 and docs/contracts/parser_golden_replay_harness.md.

  Goal:
    Verify the Codex C golden replay harness implementation against the parser golden replay harness contract. Confirm the harness replays committed sanitized Player.log fixture slices through the normal parser path and compares parser-owned observed outputs against explicit expected manifests without becoming a second parser or truth source.

  Context:
    - Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/47
    - Issue: https://github.com/Tahjali11/Mythic-Edge/issues/48
    - Related evidence/resilience issue: https://github.com/Tahjali11/Mythic-Edge/issues/11
    - Previous completed issue: https://github.com/Tahjali11/Mythic-Edge/issues/49
    - Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/110
    - Previous merge commit: a61ed4e5cd8898e25913796080a9c46e66fcff8a
    - Branch/base: codex/parser-reliability-intelligence

  Use:
    - AGENTS.md
    - docs/agent_constitution.md
    - docs/agent_rules.yml
    - docs/codex_module_workflow.md
    - docs/agent_threads/module_review.md
    - docs/contracts/parser_golden_replay_harness.md
    - docs/implementation_handoffs/parser_golden_replay_harness_comparison.md
    - docs/contracts/parser_diagnostics_mode.md
    - docs/contracts/parser_saved_event_replay.md
    - docs/contracts/code_hardening_golden_fixture_policy.md
    - docs/contracts/player_log_evidence_ledger.md
    - src/mythic_edge_parser/app/golden_replay.py
    - src/mythic_edge_parser/app/parser_diagnostics.py
    - src/mythic_edge_parser/app/saved_event_replay.py
    - src/mythic_edge_parser/app/state.py
    - src/mythic_edge_parser/app/transforms.py
    - src/mythic_edge_parser/log/entry.py
    - src/mythic_edge_parser/router.py
    - tests/test_golden_replay_harness.py
    - tests/test_parser_regressions.py
    - tests/test_parser_diagnostics_mode.py
    - tests/test_saved_event_replay.py
    - tests/fixtures/golden_replay/*.manifest.json
    - tests/fixtures/parser_regression_match_slice.log
    - tests/fixtures/parser_regression_match_expected.json
    - tests/fixtures/parser_regression_bo3_slice.log
    - tests/fixtures/parser_regression_bo3_expected.json

  Confirm:
    - build_golden_replay_report(), run_golden_replay(), and the module CLI preserve the contract public behavior.
    - Manifests must be explicit and fixture paths are repo-relative, non-absolute, and under project root.
    - Sanitization/privacy metadata is required and invalid metadata fails before replay.
    - Committed manifests compare reduced parser-owned facts, diagnostics evidence, truncation/data-loss evidence, final reconciliation, and selected parser-owned rows.
    - The harness uses LineBuffer, Router, parser modules, transforms, diagnostics evidence, and parser state rather than saved-event replay or a second parser.
    - Diagnostics mode remains observer evidence and transport health remains separate from parser truth.
    - Saved event replay behavior is unchanged and is not used as raw fixture replay.
    - No automatic expected-output bless/update behavior exists.
    - Generated reports are only written to an explicit --out path.
    - CLI returns nonzero for fail, diff, and unexpected review statuses; degraded v1 exit-code decision is explicit.
    - No parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, output transport, parser event classes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports changed.

  Validation:
    - python3 -m pytest -q tests/test_golden_replay_harness.py
    - python3 -m pytest -q tests/test_parser_regressions.py tests/test_parser_diagnostics_mode.py tests/test_saved_event_replay.py
    - python3 -m mythic_edge_parser.app.golden_replay tests/fixtures/golden_replay
    - python3 -m ruff check src tests tools
    - git diff --check
    - python3 tools/check_protected_surfaces.py --base origin/main
    - printf '%s\n' src/mythic_edge_parser/app/golden_replay.py tests/test_golden_replay_harness.py tests/fixtures/golden_replay/bo1_match_win_basic.manifest.json tests/fixtures/golden_replay/bo3_sideboard_match_loss.manifest.json docs/contracts/parser_golden_replay_harness.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
    - python3 -m pytest -q

  Output:
    - Findings first, if any.
    - Contract-test verdict.
    - Validation results.
    - Remaining non-blocking gaps.
    - Next recommended role: Codex F if no blocking findings, otherwise Codex D or Codex B.
    - workflow_handoff block.

  Do not:
    - Target main directly.
    - Close tracker #47 or related issue #11.
    - Change parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, output transport, parser event classes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports.
    - Reconstruct missing GameState data or infer match/game/card facts from incomplete evidence.
    - Copy Manasight source code.
    - Commit raw private Player.log excerpts.
    - Add automatic expected-output bless/update behavior.
    - Make golden replay a merge-readiness authority, deploy-readiness authority, parser truth source, workbook truth source, or AI truth source.
    - Stage or commit unless explicitly asked.

workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/48"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/47"
  related_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/49"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/110"
  previous_merge_commit: "a61ed4e5cd8898e25913796080a9c46e66fcff8a"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_golden_replay_harness.md"
  target_artifact: "docs/implementation_handoffs/parser_golden_replay_harness_comparison.md"
  risk_tier: "High"
  branch: "codex/parser-reliability-intelligence"
  validation:
    - "python3 -m pytest -q tests/test_golden_replay_harness.py"
    - "python3 -m pytest -q tests/test_parser_regressions.py tests/test_parser_diagnostics_mode.py tests/test_saved_event_replay.py"
    - "python3 -m mythic_edge_parser.app.golden_replay tests/fixtures/golden_replay"
    - "python3 -m ruff check src tests tools"
    - "git diff --check"
    - "python3 tools/check_protected_surfaces.py --base origin/main"
    - "focused stdin protected-surface check for issue #48 files"
    - "python3 -m pytest -q"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close tracker #47."
    - "Do not close related issue #11."
    - "Do not change parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, output transport, parser event classes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not reconstruct missing GameState data or infer match/game/card facts from incomplete evidence."
    - "Do not copy Manasight source code or commit raw private Player.log excerpts."
    - "Do not add automatic expected-output bless/update behavior."
    - "Do not make golden replay a merge-readiness authority, deploy-readiness authority, parser truth source, workbook truth source, or AI truth source."
```

## workflow_handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/48"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/47"
  related_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/11"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/49"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/110"
  previous_merge_commit: "a61ed4e5cd8898e25913796080a9c46e66fcff8a"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_golden_replay_harness.md"
  target_artifact: "docs/implementation_handoffs/parser_golden_replay_harness_comparison.md"
  risk_tier: "High"
  branch: "codex/parser-reliability-intelligence"
  validation:
    - "python3 -m pytest -q tests/test_golden_replay_harness.py -> 9 passed"
    - "python3 -m pytest -q tests/test_parser_regressions.py tests/test_parser_diagnostics_mode.py tests/test_saved_event_replay.py -> 38 passed"
    - "python3 -m mythic_edge_parser.app.golden_replay tests/fixtures/golden_replay -> pass"
    - "python3 -m ruff check src tests tools -> passed"
    - "git diff --check -> passed"
    - "python3 tools/check_protected_surfaces.py --base origin/main -> passed with 4 pre-existing branch warnings"
    - "focused stdin protected-surface check for issue #48 files -> passed with 0 warnings"
    - "python3 -m pytest -q -> 704 passed"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close tracker #47."
    - "Do not close related issue #11."
    - "Do not change parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, output transport, parser event classes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not reconstruct missing GameState data or infer match/game/card facts from incomplete evidence."
    - "Do not copy Manasight source code or commit raw private Player.log excerpts."
    - "Do not add automatic expected-output bless/update behavior."
    - "Do not make golden replay a merge-readiness authority, deploy-readiness authority, parser truth source, workbook truth source, or AI truth source."
```
