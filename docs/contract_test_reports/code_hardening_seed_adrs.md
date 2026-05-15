# Code Hardening Seed ADRs Contract-Test Report

## Findings

### P1 - Current working tree is not scoped to the seed ADR contract

`docs/contracts/code_hardening_seed_adrs.md` limits implementation ownership to
the seed ADR contract, the four ADR files, the README index section, and the
implementation handoff (`docs/contracts/code_hardening_seed_adrs.md:92`,
`docs/contracts/code_hardening_seed_adrs.md:96`). The same contract explicitly
keeps code/tests, environment variables, CI/tooling, parser/runtime behavior,
and unrelated local docs out of scope (`docs/contracts/code_hardening_seed_adrs.md:742`,
`docs/contracts/code_hardening_seed_adrs.md:749`,
`docs/contracts/code_hardening_seed_adrs.md:770`,
`docs/contracts/code_hardening_seed_adrs.md:772`).

The current working tree contains many files outside that scope, including:

- `.env.example`
- `.github/pull_request_template.md`
- `.github/workflows/repo-checks.yml`
- `.gitignore`
- `AGENTS.md`
- `README.md`
- `docs/agent_constitution.md`
- `docs/agent_threads/*.md`
- `docs/templates/*.md`
- `tests/test_check_protected_surfaces.py`
- `tools/check_protected_surfaces.py`
- `tools/run_repo_checks.ps1`
- `docs/codex_skills/mythic-edge-workflow/SKILL.md`
- `docs/local_artifacts_manifest.json`
- `docs/project_roadmap.md`
- `docs/python_tooling_inventory.md`
- `docs/validation_matrix.json`
- `docs/workbook_state_probe.example.json`
- `tests/test_agent_hardening_tools.py`
- `tools/check_agent_docs.py`
- `tools/check_local_environment.py`
- `tools/check_role_scope.py`
- `tools/check_secret_patterns.py`
- `tools/install_mythic_edge_skill.py`
- `tools/report_workbook_state.py`
- `tools/select_validation.py`

The implementation handoff acknowledges that unrelated modified and untracked
files were present and says the intended files are limited to the four seed
ADRs, README index, and handoff
(`docs/implementation_handoffs/code_hardening_seed_adrs_comparison.md:47`).
That protects the ADR content review, but it does not make the current mixed
working tree safe for submitter work. Codex F should not stage or open a PR
from this state until the seed ADR package is isolated from unrelated files.

## Open Questions Or Assumptions

- I treated the broad non-ADR working-tree changes as pre-existing unrelated
  work because the handoff says they were present before Codex C and were not
  intentionally absorbed by this module.
- I did not inspect the unrelated non-ADR file contents for correctness because
  that would broaden this contract-test review outside issue #64.
- I used remote `origin/main:<path>` source artifacts only as citation context;
  I did not sync or merge `main` into this branch and did not copy parser-audit
  or evidence-ledger docs into the hardening branch.

## Issue

Child issue: https://github.com/Tahjali11/Mythic-Edge/issues/64

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/33

## Contract

Reviewed contract:

- `docs/contracts/code_hardening_seed_adrs.md`

Supporting contracts reviewed:

- `docs/contracts/code_hardening_adr_policy.md`
- `docs/contracts/code_hardening_protected_surface_gate.md`
- `docs/contracts/code_hardening_pr_drift_budget.md`
- `docs/contracts/code_hardening_parser_event_schema_snapshots.md`

## Implementation Under Test

Branch: `codex/code-hardening-suite`

Branch freshness:

- `HEAD...origin/codex/code-hardening-suite` returned `0 0`.

Reviewed seed ADR artifacts:

- `docs/decisions/README.md`
- `docs/decisions/ADR-0001-parser-owns-truth.md`
- `docs/decisions/ADR-0002-local-deterministic-scorer-decides-llm-explains.md`
- `docs/decisions/ADR-0003-player-log-drift-policy.md`
- `docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md`
- `docs/implementation_handoffs/code_hardening_seed_adrs_comparison.md`

Remote citation context checked:

- `origin/main:docs/contracts/parser_models.md`
- `origin/main:docs/contracts/parser_state.md`
- `origin/main:docs/contracts/parser_outputs.md`
- `origin/main:docs/contracts/parser_sheet_schema.md`
- `origin/main:docs/contracts/parser_sheet_exports.md`
- `origin/main:docs/problem_representations/player_log_evidence_ledger.md`
- `origin/main:docs/contracts/player_log_evidence_ledger.md`

All listed remote source artifacts exist on `origin/main` and remain absent
from the local hardening branch, matching the contract caveat.

## Contract Summary

Issue #64 authorizes a docs-only seed ADR pass. The implementation may create
exactly four numbered ADRs, update only the `docs/decisions/README.md` ADR
index, and write the implementation handoff. It must not create additional
ADRs, change code/tests, sync or merge `main`, copy parser-audit/evidence-ledger
docs into the hardening branch, touch protected runtime surfaces, stage, commit,
open a PR, merge, or mark tracker #33 complete.

## Checks Run

```powershell
git fetch --prune origin main codex/code-hardening-suite
git rev-list --left-right --count HEAD...origin/codex/code-hardening-suite
gh issue view 64 --repo Tahjali11/Mythic-Edge --json number,title,state,body,comments
gh issue view 33 --repo Tahjali11/Mythic-Edge --comments
git diff --name-status
git ls-files --others --exclude-standard
git diff -- docs\decisions\README.md
Get-ChildItem docs\decisions -Filter 'ADR-*.md' | Sort-Object Name | Select-Object -ExpandProperty Name
git cat-file -e origin/main:docs/contracts/parser_models.md
git cat-file -e origin/main:docs/contracts/parser_state.md
git cat-file -e origin/main:docs/contracts/parser_outputs.md
git cat-file -e origin/main:docs/contracts/parser_sheet_schema.md
git cat-file -e origin/main:docs/contracts/parser_sheet_exports.md
git cat-file -e origin/main:docs/problem_representations/player_log_evidence_ledger.md
git cat-file -e origin/main:docs/contracts/player_log_evidence_ledger.md
git diff --check
py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite
rg -n "ADR-0001|ADR-0002|ADR-0003|ADR-0004" docs\decisions\README.md docs\decisions\ADR-0001-parser-owns-truth.md docs\decisions\ADR-0002-local-deterministic-scorer-decides-llm-explains.md docs\decisions\ADR-0003-player-log-drift-policy.md docs\decisions\ADR-0004-protected-surfaces-and-schema-change-policy.md
rg -n "Status: Accepted|Related issues|Related PRs|Related contracts|Decision|Non-Goals|Protected Surfaces Touched|Supersedes|Superseded By" docs\decisions\ADR-0001-parser-owns-truth.md docs\decisions\ADR-0002-local-deterministic-scorer-decides-llm-explains.md docs\decisions\ADR-0003-player-log-drift-policy.md docs\decisions\ADR-0004-protected-surfaces-and-schema-change-policy.md
@('docs/decisions/README.md','docs/decisions/ADR-0001-parser-owns-truth.md','docs/decisions/ADR-0002-local-deterministic-scorer-decides-llm-explains.md','docs/decisions/ADR-0003-player-log-drift-policy.md','docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md','docs/contracts/code_hardening_seed_adrs.md','docs/implementation_handoffs/code_hardening_seed_adrs_comparison.md') | py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite --paths-from-stdin
```

Supplemental broad working-tree check:

```powershell
$paths = @(); $paths += git diff --name-only; $paths += git ls-files --others --exclude-standard; $paths | Sort-Object -Unique | py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite --paths-from-stdin
```

## Results

- `git diff --check` passed with no whitespace errors. Git printed an
  unrelated line-ending warning for `tools/run_repo_checks.ps1`.
- Normal protected-surface gate passed with `changed_paths: 0`, `forbidden: 0`,
  `warnings: 0`. This command compares committed diff paths and does not see
  uncommitted working-tree files.
- Intended seed ADR plus review-report path-list protected-surface check passed
  with `changed_paths: 8`, `forbidden: 0`, `warnings: 0`.
- Broad working-tree path-list protected-surface check passed in exit-code
  terms but reported `changed_paths: 42`, `forbidden: 0`, `warnings: 14`.
  The warnings were for workflow authority docs, CI/runtime paths, and
  `tools/run_repo_checks.ps1`.
- ADR presence `rg` check passed.
- ADR required-section `rg` check passed.
- Exactly four numbered ADR files exist under `docs/decisions/`.

## Confirmed Contract Matches

- Exactly four numbered seed ADR files exist, with the contracted filenames
  (`docs/contracts/code_hardening_seed_adrs.md:814`,
  `docs/contracts/code_hardening_seed_adrs.md:815`).
- No additional numbered ADR files were found
  (`docs/contracts/code_hardening_seed_adrs.md:816`).
- All four ADRs use `Status: Accepted`.
- The README diff changes only the ADR Index section, replacing the old
  "No numbered ADRs exist yet" wording with the contracted four-row table
  (`docs/contracts/code_hardening_seed_adrs.md:709`,
  `docs/contracts/code_hardening_seed_adrs.md:727`,
  `docs/decisions/README.md:131`).
- ADR-0001 states parser/state truth ownership, names `state.py`, `models.py`,
  `sheet_schema.py`, and downstream consumer boundaries, and says moving truth
  ownership requires a new issue, module contract, review, validation, and ADR
  route (`docs/decisions/ADR-0001-parser-owns-truth.md:53`).
- ADR-0002 keeps analytics/coaching policy-level and says current
  analytics-sidecar files are context, not a future implementation contract
  (`docs/decisions/ADR-0002-local-deterministic-scorer-decides-llm-explains.md:37`).
- ADR-0003 cites the remote Player.log evidence-ledger artifacts without
  importing them and preserves the evidence-not-absolute-truth distinction
  (`docs/decisions/ADR-0003-player-log-drift-policy.md:26`,
  `docs/decisions/ADR-0003-player-log-drift-policy.md:48`).
- ADR-0004 preserves the protected-surface policy that warnings are review
  signals, not automatic authorization or rejection, and that passing tests are
  necessary but not sufficient (`docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md:53`).
- Each ADR includes `Related issues`, `Related PRs`, `Related contracts`,
  `Decision`, `Non-Goals`, `Protected Surfaces Touched`, `Supersedes`, and
  `Superseded By` sections.
- Each ADR explicitly states that it does not authorize protected-surface
  changes (`docs/decisions/ADR-0001-parser-owns-truth.md:107`,
  `docs/decisions/ADR-0002-local-deterministic-scorer-decides-llm-explains.md:100`,
  `docs/decisions/ADR-0003-player-log-drift-policy.md:145`,
  `docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md:110`).
- Parser/runtime tests were reasonably skipped for the seed ADR content
  because the intended module files are Markdown-only
  (`docs/contracts/code_hardening_seed_adrs.md:806`).

## Contract Mismatches

- No seed ADR content mismatch found.
- The current working tree scope mismatch in the Findings section blocks
  submitter readiness until the seed ADR files are isolated from unrelated
  modified/untracked files.

## Missing Safeguards Or Missing Tests

- No automated ADR linter exists yet for exact required citations, section
  completeness, status values, monotonic numbering, or README index order.
  This is a non-blocking test gap for the ADR content because the contract did
  not require a linter for issue #64.
- The normal protected-surface gate does not inspect uncommitted files, which
  is why the supplemental intended-path and broad-working-tree checks were
  needed in this local review.
- Full parser tests were not run because the reviewed seed ADR package is
  docs-only. If any of the unrelated code/tool/test changes are later included
  in a PR, that separate package will need its own validation.

## Drift Notes

- Repo drift: the intended seed ADR content is aligned with the contract, but
  the current working tree is mixed with unrelated modified and untracked
  files.
- Workbook drift: not applicable; no workbook state was inspected.
- Deployment drift: not applicable; no deployed Apps Script or production
  runtime state was inspected.
- Local-data drift: unrelated local docs and tooling files are present and
  must not be absorbed into issue #64.

## Recommendation

Request implementation/scope cleanup before submitter work.

Recommended next role: Codex D: Module Fixer / scope-isolation thread.

Codex D should not change ADR wording unless explicitly asked. Its job should
be to isolate the reviewed issue #64 package from unrelated working-tree files,
then route back to Codex E for a short cleanup confirmation or to Codex F if
the user confirms the isolation is sufficient.

## Next Workflow Action

Pasteable prompt:

```text
Use $mythic-edge-workflow.
Use the Mythic Edge agent constitution.

Act as Codex D: Module Fixer / scope-isolation thread for the Code Hardening child issue: Seed architecture decision records.

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/33

Child issue:
https://github.com/Tahjali11/Mythic-Edge/issues/64

Branch target:
codex/code-hardening-suite

Use:
- docs/contracts/code_hardening_seed_adrs.md
- docs/implementation_handoffs/code_hardening_seed_adrs_comparison.md
- docs/contract_test_reports/code_hardening_seed_adrs.md

Finding to fix:
The seed ADR content passed contract review, but the current working tree includes many unrelated modified/untracked files outside issue #64. Isolate the issue #64 package without deleting or reverting user work unless explicitly approved.

Intended issue #64 files:
- docs/contracts/code_hardening_seed_adrs.md
- docs/decisions/README.md
- docs/decisions/ADR-0001-parser-owns-truth.md
- docs/decisions/ADR-0002-local-deterministic-scorer-decides-llm-explains.md
- docs/decisions/ADR-0003-player-log-drift-policy.md
- docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md
- docs/implementation_handoffs/code_hardening_seed_adrs_comparison.md
- docs/contract_test_reports/code_hardening_seed_adrs.md

Do not change ADR wording unless explicitly asked. Do not stage, commit, open a PR, merge, or mark tracker #33 complete. Do not change parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, event kind values, parser payload shapes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, production deployment behavior, or merge-to-main policy.

Validation after isolation:
git diff --check
py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite
rg -n "ADR-0001|ADR-0002|ADR-0003|ADR-0004" docs\decisions\README.md docs\decisions\ADR-0001-parser-owns-truth.md docs\decisions\ADR-0002-local-deterministic-scorer-decides-llm-explains.md docs\decisions\ADR-0003-player-log-drift-policy.md docs\decisions\ADR-0004-protected-surfaces-and-schema-change-policy.md
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/64"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/33"
  completed_thread: "E"
  next_thread: "D"
  next_role: "Codex D: Module Fixer / scope-isolation thread"
  source_artifact: "docs/contract_test_reports/code_hardening_seed_adrs.md"
  target_artifact: "isolated issue #64 working tree or cleanup handoff"
  contract: "docs/contracts/code_hardening_seed_adrs.md"
  implementation_artifact: "docs/implementation_handoffs/code_hardening_seed_adrs_comparison.md"
  risk_tier: "Medium"
  branch: "codex/code-hardening-suite"
  validation:
    - "git diff --check -> passed; git printed unrelated tools/run_repo_checks.ps1 line-ending warning"
    - "py tools\\check_protected_surfaces.py --base origin/codex/code-hardening-suite -> passed; changed_paths 0, forbidden 0, warnings 0"
    - "intended issue #64 plus review-report path-list protected-surface check -> passed; changed_paths 8, forbidden 0, warnings 0"
    - "broad working-tree path-list protected-surface check -> passed but reported changed_paths 42 and warnings 14"
    - "ADR presence rg check -> passed"
    - "ADR required-section rg check -> passed"
    - "exactly four numbered ADR files found"
  stop_conditions:
    - "Do not delete, revert, or discard unrelated user work unless explicitly approved."
    - "Do not change ADR wording unless explicitly asked."
    - "Do not create additional numbered ADRs."
    - "Do not implement policy changes beyond the four ADR docs and README index."
    - "Do not change parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, event kind values, parser payload shapes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, production deployment behavior, or merge-to-main policy."
    - "Do not sync or merge main into the hardening branch."
    - "Do not copy parser-audit or evidence-ledger source docs into the hardening branch."
    - "Do not target main."
    - "Do not mark tracker #33 complete."
    - "Do not stage, commit, open a PR, or merge unless explicitly asked."
```
