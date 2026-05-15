# Code Hardening Seed ADRs Implementation Handoff

## Issue

Child issue: https://github.com/Tahjali11/Mythic-Edge/issues/64

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/33

Branch target: `codex/code-hardening-suite`

## Contract

Source contract: `docs/contracts/code_hardening_seed_adrs.md`

Supporting governance contracts:

- `docs/contracts/code_hardening_adr_policy.md`
- `docs/contracts/code_hardening_protected_surface_gate.md`
- `docs/contracts/code_hardening_pr_drift_budget.md`
- `docs/contracts/code_hardening_parser_event_schema_snapshots.md`

## Role Performed

Codex C: Module Implementer / comparison thread.

## Baseline And Source Check

- Confirmed current branch: `codex/code-hardening-suite`.
- Confirmed branch was at PR #63 merge commit `774076b` and aligned with `origin/codex/code-hardening-suite` before edits.
- Confirmed no numbered ADR files existed before this implementation.
- Confirmed `docs/decisions/README.md` and `docs/decisions/ADR_TEMPLATE.md` existed locally.
- Inspected local governance docs, hardening contracts, issue #33, and issue #64.
- Inspected remote-only parser/evidence source artifacts by remote ref without syncing, merging, rebasing, or copying them into this branch.

Remote source artifacts used as citations:

- `origin/main:docs/contracts/parser_models.md`
- `origin/main:docs/contracts/parser_state.md`
- `origin/main:docs/contracts/parser_outputs.md`
- `origin/main:docs/contracts/parser_sheet_schema.md`
- `origin/main:docs/contracts/parser_sheet_exports.md`
- `origin/main:docs/problem_representations/player_log_evidence_ledger.md`
- `origin/main:docs/contracts/player_log_evidence_ledger.md`

The same remote artifact paths were available on `origin/codex/parser-module-audit-suite` during inspection; no source-content conflict was observed for the cited artifacts.

## Worktree Hygiene

Pre-existing unrelated modified and untracked files were present outside this module. They were not edited, staged, or absorbed by this thread. This thread's intended files are limited to the four seed ADRs, the ADR README index, and this handoff.

## What Changed

Created the four contracted seed architecture decision records:

- `docs/decisions/ADR-0001-parser-owns-truth.md`
- `docs/decisions/ADR-0002-local-deterministic-scorer-decides-llm-explains.md`
- `docs/decisions/ADR-0003-player-log-drift-policy.md`
- `docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md`

Updated only the ADR index section in:

- `docs/decisions/README.md`

Produced this implementation handoff:

- `docs/implementation_handoffs/code_hardening_seed_adrs_comparison.md`

## Code Changed Or Docs-Only

Docs-only.

No Python code, tests, CI scripts, parser behavior, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, parser payload shapes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, production deployment behavior, or merge-to-main policy were changed.

## Contract Matches

- Created exactly four numbered ADR files with the contracted filenames.
- Used `Status: Accepted` for all four seed ADRs.
- Recorded that acceptance is effective after reviewed merge into the approved branch.
- Included issue #64, tracker #33, the seed ADR contract, and the ADR policy contract in each seed ADR.
- Included each ADR's required issue, PR, contract, source-document, and related-ADR citations.
- Kept ADR-0001's related ADRs as `None`.
- Cited earlier ADRs only where later ADRs depend on them.
- Included required decision statements, non-goals, alternatives, consequences, truth ownership impact, protected-surface boundaries, validation evidence, supersession fields, follow-ups, and notes.
- Explicitly stated in every seed ADR that it does not authorize the shared protected-surface changes listed by the contract.
- Added the contracted four-row ADR index in numeric order.
- Did not copy parser-audit or evidence-ledger source docs into the hardening branch.

## Contract Mismatches

Initial comparison found the expected contract gap:

- The ADR policy system existed, but the four contracted seed ADRs did not.
- The ADR README index still said no numbered ADRs existed.

Those gaps were resolved by the docs-only changes above.

No runtime, parser, schema, webhook, Apps Script, or deployment mismatch was identified or changed.

## Missing Safeguards Or Missing Tests

- No runtime tests were added because this pass changed only Markdown ADR and handoff files.
- There is no dedicated automated ADR linter yet for exact seed ADR sections, required citations, or index ordering.
- The protected-surface gate is useful for branch diff review, but when run against `HEAD` it does not inspect uncommitted docs-only files until they are committed. A scoped intended-path gate check is recommended in review if the reviewer wants local-file coverage before commit.

## Protected Surface Status

Protected surfaces intentionally not touched:

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
- sync-field names
- runtime family names
- runtime `event_type` values
- runtime `scope` values
- secrets, credentials, tokens, API keys, webhook URLs, and environment variables
- raw logs and local/private artifacts
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

Result: passed. Git emitted an unrelated line-ending warning for `tools/run_repo_checks.ps1`; no whitespace errors were reported.

```powershell
py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite
```

Result: passed with `changed_paths: 0`, `forbidden: 0`, and `warnings: 0`. This command compares the committed branch diff and therefore does not count uncommitted docs-only changes until they are committed.

```powershell
rg -n "ADR-0001|ADR-0002|ADR-0003|ADR-0004" docs\decisions\README.md docs\decisions\ADR-0001-parser-owns-truth.md docs\decisions\ADR-0002-local-deterministic-scorer-decides-llm-explains.md docs\decisions\ADR-0003-player-log-drift-policy.md docs\decisions\ADR-0004-protected-surfaces-and-schema-change-policy.md
```

Result: passed. All four ADRs are present in the index and files.

```powershell
rg -n "Status: Accepted|Related issues|Related PRs|Related contracts|Decision|Non-Goals|Protected Surfaces Touched|Supersedes|Superseded By" docs\decisions\ADR-0001-parser-owns-truth.md docs\decisions\ADR-0002-local-deterministic-scorer-decides-llm-explains.md docs\decisions\ADR-0003-player-log-drift-policy.md docs\decisions\ADR-0004-protected-surfaces-and-schema-change-policy.md
```

Result: passed. The required sections appear in all four seed ADRs.

Supplemental scoped checks:

```powershell
@('docs/decisions/README.md','docs/decisions/ADR-0001-parser-owns-truth.md','docs/decisions/ADR-0002-local-deterministic-scorer-decides-llm-explains.md','docs/decisions/ADR-0003-player-log-drift-policy.md','docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md','docs/implementation_handoffs/code_hardening_seed_adrs_comparison.md') | py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite --paths-from-stdin
```

Result: passed with `changed_paths: 6`, `forbidden: 0`, and `warnings: 0`.

```powershell
Get-ChildItem docs\decisions -Filter 'ADR-*.md' | Sort-Object Name | Select-Object -ExpandProperty Name
```

Result: exactly four numbered ADR files were present.

```powershell
rg -n "[ \t]+$" docs\decisions\README.md docs\decisions\ADR-0001-parser-owns-truth.md docs\decisions\ADR-0002-local-deterministic-scorer-decides-llm-explains.md docs\decisions\ADR-0003-player-log-drift-policy.md docs\decisions\ADR-0004-protected-surfaces-and-schema-change-policy.md docs\implementation_handoffs\code_hardening_seed_adrs_comparison.md
```

Result: passed with no trailing whitespace matches.

## Validation Selection

The contract states that full parser tests are not required for Markdown-only ADR creation. Parser tests were skipped because this thread did not touch runtime code, parser code, schema code, tests, CI behavior, workbook code, webhook code, Apps Script, secrets, local artifacts, or protected runtime surfaces.

## Still Unverified

- Reviewer has not yet performed the Codex E contract-test/readthrough pass.
- GitHub PR checks have not run for these uncommitted docs-only changes.
- No PR has been opened from this thread.
- No commit has been made.
- Live workbook state, deployed Apps Script state, production runtime behavior, and external services were intentionally not inspected.

## Reviewer Focus

Codex E should verify:

- Exactly four numbered ADR files exist and no extra numbered ADRs were created.
- Each ADR includes issue #64, tracker #33, `docs/contracts/code_hardening_seed_adrs.md`, and `docs/contracts/code_hardening_adr_policy.md`.
- ADR-0001 does not accidentally weaken parser truth ownership.
- ADR-0002 does not turn the current analytics sidecar into a future implementation contract.
- ADR-0003 cites remote Player.log evidence-ledger artifacts without importing them into the hardening branch.
- ADR-0004 preserves protected-surface authorization requirements and does not make warnings automatic authorization or automatic rejection.
- README index changed only in the ADR index section.

## Next Workflow Action

Next recommended role: Codex E: Module Reviewer / contract-test thread.

Pasteable prompt:

```text
Use $mythic-edge-workflow.
Use the Mythic Edge agent constitution.

Act as Codex E: Module Reviewer / contract-test thread for the Code Hardening child issue: Seed architecture decision records.

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/33

Child issue:
https://github.com/Tahjali11/Mythic-Edge/issues/64

Branch target:
codex/code-hardening-suite

Review artifacts:
- docs/contracts/code_hardening_seed_adrs.md
- docs/implementation_handoffs/code_hardening_seed_adrs_comparison.md
- docs/decisions/README.md
- docs/decisions/ADR-0001-parser-owns-truth.md
- docs/decisions/ADR-0002-local-deterministic-scorer-decides-llm-explains.md
- docs/decisions/ADR-0003-player-log-drift-policy.md
- docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md
- docs/contracts/code_hardening_adr_policy.md
- docs/contracts/code_hardening_protected_surface_gate.md
- docs/contracts/code_hardening_pr_drift_budget.md
- docs/contracts/code_hardening_parser_event_schema_snapshots.md

Remote citation context if absent locally:
- origin/main:docs/contracts/parser_models.md
- origin/main:docs/contracts/parser_state.md
- origin/main:docs/contracts/parser_outputs.md
- origin/main:docs/contracts/parser_sheet_schema.md
- origin/main:docs/contracts/parser_sheet_exports.md
- origin/main:docs/problem_representations/player_log_evidence_ledger.md
- origin/main:docs/contracts/player_log_evidence_ledger.md

Task:
Review the implementation against docs/contracts/code_hardening_seed_adrs.md. This is a docs-only ADR seed pass. Lead with findings, ordered by severity. Verify that exactly four seed ADRs were created, the README index was the only README section updated, required citations and decision statements are present, protected-surface non-authorization language is explicit, and no unrelated or protected files were absorbed.

Do not change parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, event kind values, parser payload shapes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, production deployment behavior, or merge-to-main policy.

Do not sync or merge main into the hardening branch. Do not copy parser-audit or evidence-ledger docs into this branch. Do not stage, commit, open a PR, merge, or mark tracker #33 complete unless explicitly asked.

Validation:
git diff --check
py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite
rg -n "ADR-0001|ADR-0002|ADR-0003|ADR-0004" docs\decisions\README.md docs\decisions\ADR-0001-parser-owns-truth.md docs\decisions\ADR-0002-local-deterministic-scorer-decides-llm-explains.md docs\decisions\ADR-0003-player-log-drift-policy.md docs\decisions\ADR-0004-protected-surfaces-and-schema-change-policy.md
rg -n "Status: Accepted|Related issues|Related PRs|Related contracts|Decision|Non-Goals|Protected Surfaces Touched|Supersedes|Superseded By" docs\decisions\ADR-0001-parser-owns-truth.md docs\decisions\ADR-0002-local-deterministic-scorer-decides-llm-explains.md docs\decisions\ADR-0003-player-log-drift-policy.md docs\decisions\ADR-0004-protected-surfaces-and-schema-change-policy.md

Produce:
docs/contract_test_reports/code_hardening_seed_adrs.md

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
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/64"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/33"
  completed_thread: "C"
  next_thread: "E"
  next_role: "Codex E: Module Reviewer / contract-test thread"
  source_artifact: "docs/contracts/code_hardening_seed_adrs.md"
  target_artifact: "docs/contract_test_reports/code_hardening_seed_adrs.md"
  implementation_artifact: "docs/implementation_handoffs/code_hardening_seed_adrs_comparison.md"
  risk_tier: "Medium"
  branch: "codex/code-hardening-suite"
  validation:
    - "git diff --check"
    - "py tools\\check_protected_surfaces.py --base origin/codex/code-hardening-suite"
    - "rg -n \"ADR-0001|ADR-0002|ADR-0003|ADR-0004\" docs\\decisions\\README.md docs\\decisions\\ADR-0001-parser-owns-truth.md docs\\decisions\\ADR-0002-local-deterministic-scorer-decides-llm-explains.md docs\\decisions\\ADR-0003-player-log-drift-policy.md docs\\decisions\\ADR-0004-protected-surfaces-and-schema-change-policy.md"
    - "rg -n \"Status: Accepted|Related issues|Related PRs|Related contracts|Decision|Non-Goals|Protected Surfaces Touched|Supersedes|Superseded By\" docs\\decisions\\ADR-0001-parser-owns-truth.md docs\\decisions\\ADR-0002-local-deterministic-scorer-decides-llm-explains.md docs\\decisions\\ADR-0003-player-log-drift-policy.md docs\\decisions\\ADR-0004-protected-surfaces-and-schema-change-policy.md"
  stop_conditions:
    - "Do not create additional numbered ADRs."
    - "Do not implement policy changes beyond the four ADR docs and README index."
    - "Do not change parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, event kind values, parser payload shapes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, production deployment behavior, or merge-to-main policy."
    - "Do not sync or merge main into the hardening branch."
    - "Do not copy parser-audit or evidence-ledger source docs into the hardening branch."
    - "Do not absorb unrelated local modified or untracked files."
    - "Do not target main."
    - "Do not mark tracker #33 complete."
    - "Do not stage, commit, open a PR, or merge unless explicitly asked."
```
