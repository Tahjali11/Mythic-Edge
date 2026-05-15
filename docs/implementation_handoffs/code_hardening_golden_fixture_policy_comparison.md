# Code Hardening Golden Fixture Policy Comparison

## Issue

Child issue: https://github.com/Tahjali11/Mythic-Edge/issues/68

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/33

Related evidence-ledger issue: https://github.com/Tahjali11/Mythic-Edge/issues/11

## Contract

Source contract: `docs/contracts/code_hardening_golden_fixture_policy.md`

Related ADRs:

- `docs/decisions/ADR-0001-parser-owns-truth.md`
- `docs/decisions/ADR-0003-player-log-drift-policy.md`
- `docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md`

Remote evidence-ledger context:

- `origin/main:docs/problem_representations/player_log_evidence_ledger.md`
- `origin/main:docs/contracts/player_log_evidence_ledger.md`

## Role Performed

Codex C: Module Implementer / comparison thread.

## Branch And Worktree Check

- Confirmed branch: `codex/code-hardening-suite`.
- Confirmed tracker #33 and child issue #68 are open.
- Fetched `origin` before comparison.
- Observed current HEAD: `0d84dc7`.
- Observed worktree before editing: `docs/contracts/code_hardening_golden_fixture_policy.md` was untracked and treated as the source artifact for this pass.
- No unrelated modified files were edited, staged, committed, pushed, or absorbed.

## What Golden Fixtures Are Supposed To Do

Golden fixtures are committed, reviewed, deterministic test artifacts that preserve known-good behavior or approved expected degradation. In this contract, they may be sanitized Player.log excerpts, parser replay fixtures, expected parser output snapshots, schema snapshots, future drift-report expected outputs, evidence-ledger fixtures, or repo-side workbook/Apps Script parity snapshots.

They are supposed to be sanitized or synthetic, minimal, reviewable, paired with expected outputs or focused assertions, tied to an issue and contract, and protected from accidental update. They must not become raw log dumps, a second parser, a downstream truth owner, an unreviewed schema drift mechanism, or a way to bless behavior just because a test failed.

## Current Behavior Summary

Current fixtures and tests already provide useful deterministic coverage:

- Parser replay slices exist under `tests/fixtures/` and are paired with expected parser-output JSON.
- Schema snapshots exist under `tests/fixtures/schema_snapshots/` and have explicit opt-in update behavior through `MYTHIC_EDGE_UPDATE_SCHEMA_SNAPSHOTS=1`.
- Schema snapshot tests reject selected forbidden private, local, webhook, deployment, failed-post, and runtime path snippets.
- Drift sensor tests use a sanitized fixture slice copied into temporary `Player.log` paths and assert focused drift behavior without committing runtime reports.
- The protected-surface gate forbids raw local log and local artifact paths outside documented fixture exceptions, while allowing `tests/fixtures/` paths.

The main remaining gap is policy metadata and future fixture governance, not a current parser behavior defect.

## Files Inspected

Governance and workflow:

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`

Contracts and ADRs:

- `docs/contracts/code_hardening_golden_fixture_policy.md`
- `docs/contracts/code_hardening_protected_surface_gate.md`
- `docs/contracts/code_hardening_pr_drift_budget.md`
- `docs/contracts/code_hardening_parser_event_schema_snapshots.md`
- `docs/decisions/ADR-0001-parser-owns-truth.md`
- `docs/decisions/ADR-0003-player-log-drift-policy.md`
- `docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md`

Remote evidence-ledger artifacts:

- `origin/main:docs/problem_representations/player_log_evidence_ledger.md`
- `origin/main:docs/contracts/player_log_evidence_ledger.md`

Fixture, test, and tool surfaces:

- `tests/fixtures/`
- `tests/test_parser_regressions.py`
- `tests/test_event_schema_snapshots.py`
- `tests/test_log_drift_sensor.py`
- `tests/test_check_protected_surfaces.py`
- `src/mythic_edge_parser/app/log_drift_sensor.py`
- `tools/check_protected_surfaces.py`

## Fixture Class Comparison

| Contract fixture class | Current status | Notes |
| --- | --- | --- |
| `sanitized_player_log_excerpt` | Exists, legacy/unclassified | Four `.log` fixture slices have comments labeling them sanitized or sourced from a sanitized corpus. No machine-readable redaction metadata exists. |
| `parser_replay_fixture` | Exists | `parser_regression_match_slice.log` and `parser_regression_bo3_slice.log` replay through `LineBuffer`, `Router`, parser transforms, and parser state. |
| `parser_expected_output_snapshot` | Exists | `parser_regression_match_expected.json` and `parser_regression_bo3_expected.json` are paired with parser replay inputs and compared as full snapshots. |
| `schema_snapshot_fixture` | Exists | Six JSON schema snapshots cover event classes, payload keys, workbook row keys, sheet schema surfaces, runtime export row keys, and repo-side Apps Script parity. |
| `drift_report_expected_output` | Missing by design | Drift sensor tests assert selected report fields using temporary files. No committed full drift-report expected-output JSON or baseline exists. |
| `evidence_ledger_fixture` | Missing by design | Evidence-ledger implementation is absent; no Tier 0-7 ledger fixture validates value-source, confidence, finality, drift flags, or invariants. |
| `workbook_or_apps_script_parity_snapshot` | Exists repo-side only | `apps_script_repo_parity.json` and related workbook/schema snapshots compare committed repo surfaces. They do not inspect live workbook or deployed Apps Script state. |

## Contract Matches

- Current committed `.log` fixtures live under `tests/fixtures/`, the documented allowed fixture path.
- Fixture comments identify the current `.log` slices as sanitized or from a sanitized corpus.
- Parser regression fixtures are paired with expected JSON outputs and asserted deterministically.
- Parser regression expected outputs cover event traces, router stats, parser context, match summary debug dictionaries, match rows, match-log rows, and game-log rows.
- Schema snapshots include stable `schema_snapshot_version` values.
- Schema snapshot update mode is explicit and opt-in.
- Schema snapshot mismatch text warns not to auto-update without issue, contract, and review approval.
- Schema snapshot tests check for forbidden snapshot snippets including webhook URLs, deployment markers, spreadsheet IDs, local user paths, runtime logs, failed posts, and runtime status paths.
- Drift sensor tests keep report and baseline files in temporary paths, not committed runtime status paths.
- `_entry_signature()` privacy behavior is tested with an identity-bearing sample and returns a prefix label instead of the full line.
- Protected-surface gate forbids raw `Player.log`, data logs, runtime logs, runtime status files, failed posts, bad events, generated card/tier data, workbook exports, secret filenames, webhook credentials, and local review artifacts outside allowed fixtures.
- Protected-surface gate allows documented fixture paths under `tests/fixtures/`, including `Player.log`-style names, matching the current policy exception.
- Protected warnings remain non-failing, while forbidden paths fail.
- `tools/check_secret_patterns.py` is absent on this branch, matching the contract's observed-current-state note.

## Contract Gaps

These are expected policy gaps, not implementation bugs in this comparison pass:

- No central fixture manifest, sidecar metadata, Markdown index, or test-owned declaration records the required provenance fields.
- Existing fixtures are effectively `legacy_unclassified`; no machine-readable `fixture_id`, `fixture_class`, `source_issue`, `source_contract`, `source_privacy_class`, `redaction_status`, `redaction_method`, `evidence_ledger_tiers`, or update-approval metadata exists.
- Redaction is documented by comments and review history rather than by a recorded sanitizer method or redaction category list.
- There is no content secret scanner on this branch, so fixture privacy currently depends on path gates, focused test guards, review, and manual inspection.
- The protected-surface gate allows any path under `tests/fixtures/` by path alone for local log and workbook-export exceptions; it does not prove the fixture is sanitized, minimal, or paired with metadata.
- Parser expected-output snapshots do not include evidence-ledger value-source, confidence, finality, drift flag, or invariant metadata because the ledger is not implemented.
- No evidence-ledger fixture validates Tier 0 through Tier 7 metadata.
- No full committed `drift_report_expected_output` fixture exists.
- `log_drift_sensor.py` runtime reports include volatile `analyzed_at` and local `source_path` values, which is acceptable for local runtime reports but unsuitable for committed expected-output baselines without normalization.
- Drift baseline refresh policy remains out of scope and unimplemented.
- Repo-side workbook/Apps Script parity snapshots do not prove live workbook or deployed Apps Script state, which is correct but still unverified.

## Contract Mismatches

No clear contract mismatch required code, test, fixture, or tool changes in this pass.

The contract explicitly says existing fixtures are not retroactively rejected and may continue to be used while a future issue decides whether to add metadata, rename fixtures, split fixtures, or create a central manifest.

## Missing Safeguards Or Missing Tests

- Missing automated fixture provenance enforcement.
- Missing automated redaction metadata checks.
- Missing content-level secret/private-data scanner on this branch.
- Missing test that every parser replay input has provenance metadata.
- Missing test that every parser replay fixture is paired with either expected output, focused assertion target, or future ledger fixture metadata.
- Missing committed drift-report expected-output fixture, by design.
- Missing evidence-ledger fixture coverage, by design.

## Stale Or Bridge-Code Areas

- `flush_timing_corpus_slice.log` is labeled as an original `manasight-parser` sanitized corpus slice. It remains useful but should be treated as legacy/unclassified until a future metadata retrofit.
- Current schema snapshots are strong local guardrails but predate the general golden-fixture policy manifest question.
- Current drift sensor behavior is runtime-local and baseline-capable, but committed baseline refresh policy has not been designed yet.

## Files Changed

- `docs/implementation_handoffs/code_hardening_golden_fixture_policy_comparison.md`

## Code Changed Or Docs-Only

Docs-only comparison artifact.

No code, tests, fixtures, schema snapshots, expected outputs, drift baselines, runtime status files, parser behavior, workbook schema, webhook payload shape, Apps Script behavior, secrets, generated data, failed posts, workbook exports, or local-only artifacts were changed.

## Interface Changes

None.

No function signatures, parser payload fields, event classes, event `kind` values, workbook columns, webhook payloads, Apps Script entrypoints, environment variables, runtime status shapes, fixture data, expected-output schemas, or protected runtime surfaces changed.

## Tests Added Or Updated

None.

## Protected Surface Status

No protected runtime surface was touched.

This pass did not change:

- parser behavior
- parser state final reconciliation
- workbook schema
- webhook payload shape
- Apps Script behavior
- parser event classes
- event `kind` values
- parser payload shapes
- match identity
- game identity
- deduplication
- sync field names
- runtime family names
- runtime `event_type` values
- runtime `scope` values
- secrets, credentials, tokens, API keys, webhook URLs, or environment variables
- raw local logs
- generated card or tier data
- runtime status files
- failed posts
- workbook exports
- production deployment behavior
- merge-to-main policy

## Validation Run

```powershell
git diff --check
```

Result: passed.

```powershell
py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite
```

Result: passed with `changed_paths: 0`, `forbidden: 0`, and `warnings: 0` before this handoff was created.

This command compares committed branch diff against `HEAD`; it does not count uncommitted docs-only files until they are committed. A scoped uncommitted-path check was also run:

```powershell
@('docs/contracts/code_hardening_golden_fixture_policy.md','docs/implementation_handoffs/code_hardening_golden_fixture_policy_comparison.md') | py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite --paths-from-stdin
```

Result: passed with `changed_paths: 2`, `forbidden: 0`, and `warnings: 0`.

```powershell
py -m pytest -q tests\test_parser_regressions.py tests\test_event_schema_snapshots.py tests\test_log_drift_sensor.py tests\test_check_protected_surfaces.py
```

Result: passed, `65 passed in 0.71s`.

```powershell
py -m ruff check src tests tools
```

Result: passed, `All checks passed!`.

## Still Unverified

- No Codex E contract-test review has been performed yet for this comparison artifact.
- No fixture metadata manifest or sidecar design has been selected.
- No content scanner has been implemented or run because `tools/check_secret_patterns.py` is absent on this branch.
- No live workbook state or deployed Apps Script state was inspected.
- No drift detector baseline refresh policy was implemented or validated.
- No evidence-ledger runtime or fixture implementation exists yet.
- No PR checks have run for this uncommitted docs-only handoff.

## Reviewer Focus

Codex E should verify:

- This handoff did not understate the risk of allowing `tests/fixtures/` by path while lacking content/provenance checks.
- Existing fixtures are correctly treated as legacy/unclassified rather than unsafe or fully policy-compliant.
- No fixture creation, fixture data change, expected-output update, schema snapshot update, drift baseline refresh, parser behavior change, or protected-surface change was made.
- The comparison accurately distinguishes current runtime drift reports from future committed drift-report expected-output fixtures.
- The next recommended work stays in contract-test/review mode, not fixture creation.

## Next Workflow Action

Next recommended role: Codex E: Module Reviewer / contract-test thread.

Pasteable prompt:

```text
Use $mythic-edge-workflow.
Use the Mythic Edge agent constitution.

Act as Codex E: Module Reviewer / contract-test thread for the Code Hardening child issue: Golden fixture policy linked to the evidence ledger.

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/33

Child issue:
https://github.com/Tahjali11/Mythic-Edge/issues/68

Branch target:
codex/code-hardening-suite

Review artifacts:
- docs/contracts/code_hardening_golden_fixture_policy.md
- docs/implementation_handoffs/code_hardening_golden_fixture_policy_comparison.md
- docs/contracts/code_hardening_protected_surface_gate.md
- docs/contracts/code_hardening_pr_drift_budget.md
- docs/contracts/code_hardening_parser_event_schema_snapshots.md
- docs/decisions/ADR-0001-parser-owns-truth.md
- docs/decisions/ADR-0003-player-log-drift-policy.md
- docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md
- tests/test_parser_regressions.py
- tests/test_event_schema_snapshots.py
- tests/test_log_drift_sensor.py
- tests/test_check_protected_surfaces.py
- src/mythic_edge_parser/app/log_drift_sensor.py
- tools/check_protected_surfaces.py
- tests/fixtures/

Remote citation context if absent locally:
- origin/main:docs/problem_representations/player_log_evidence_ledger.md
- origin/main:docs/contracts/player_log_evidence_ledger.md

Task:
Review the implementation comparison against docs/contracts/code_hardening_golden_fixture_policy.md. This was a docs-only comparison pass. Lead with findings, ordered by severity. Verify that the comparison accurately classifies current fixture classes, legacy/unclassified fixture gaps, redaction/provenance gaps, expected-output pairing, schema snapshot policy, drift sensor behavior, protected-surface behavior, and remaining risks.

Do not create fixture files, add sanitized fixture data, sanitize raw logs, implement sanitizer tooling, implement the evidence ledger, implement drift detector baseline refresh policy, refresh or commit drift baselines, or modify parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, event kind values, parser payload shapes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, or local-only artifacts.

Do not target main. Do not mark tracker #33 complete. Do not stage, commit, open a PR, or merge unless explicitly asked.

Validation:
git diff --check
py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite
py -m pytest -q tests\test_parser_regressions.py tests\test_event_schema_snapshots.py tests\test_log_drift_sensor.py tests\test_check_protected_surfaces.py
py -m ruff check src tests tools

Produce:
docs/contract_test_reports/code_hardening_golden_fixture_policy.md

Final review must include:
- role performed
- issue/tracker
- contract reviewed
- artifacts reviewed
- findings first
- files changed, if any
- validation run and result
- remaining risks
- next recommended role
- pasteable next-thread prompt
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/68"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/33"
  completed_thread: "C"
  next_thread: "E"
  next_role: "Codex E: Module Reviewer / contract-test thread"
  source_artifact: "docs/contracts/code_hardening_golden_fixture_policy.md"
  target_artifact: "docs/contract_test_reports/code_hardening_golden_fixture_policy.md"
  implementation_artifact: "docs/implementation_handoffs/code_hardening_golden_fixture_policy_comparison.md"
  risk_tier: "Medium"
  branch: "codex/code-hardening-suite"
  validation:
    - "git diff --check"
    - "py tools\\check_protected_surfaces.py --base origin/codex/code-hardening-suite"
    - "py -m pytest -q tests\\test_parser_regressions.py tests\\test_event_schema_snapshots.py tests\\test_log_drift_sensor.py tests\\test_check_protected_surfaces.py"
    - "py -m ruff check src tests tools"
  stop_conditions:
    - "Do not create fixture files or add sanitized fixture data."
    - "Do not sanitize raw logs or implement sanitizer tooling."
    - "Do not implement the evidence ledger."
    - "Do not implement drift detector baseline refresh policy."
    - "Do not refresh or commit drift baselines."
    - "Do not modify parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, event kind values, parser payload shapes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, or local-only artifacts."
    - "Do not target main; hardening work belongs on codex/code-hardening-suite."
    - "Do not mark tracker #33 complete."
    - "Do not stage, commit, open a PR, or merge unless explicitly asked."
```
