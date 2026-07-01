# Quality Ruff First Exact-Code Blocking Promotion Contract

## Module

`quality_ruff_first_exact_code_blocking_promotion`

This contract decides whether Mythic Edge's first validated exact Ruff
zero-baseline tranche may move from advisory dry-run evidence to a blocking
validation gate.

Blocking means a future local check or GitHub Actions check may fail when one
of the selected exact rule codes is violated. This contract does not implement
that failure behavior by itself.

## Source Artifacts

- Issue: <https://github.com/Tahjali11/Mythic-Edge/issues/601>
- Tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/567>
- Project roadmap: <https://github.com/Tahjali11/Mythic-Edge/issues/568>
- Source candidate-selection issue: <https://github.com/Tahjali11/Mythic-Edge/issues/596>
- Source dry-run issue: <https://github.com/Tahjali11/Mythic-Edge/issues/599>
- Source dry-run PR: <https://github.com/Tahjali11/Mythic-Edge/pull/600>
- Dry-run merge commit:
  `cf7147554cdc3c92bfde5d38f4f7afd265bd8b46`
- Source contract:
  `docs/contracts/quality_ruff_zero_baseline_candidate_selection.md`
- Source dry-run handoff:
  `docs/implementation_handoffs/quality_ruff_first_exact_code_dry_run_comparison.md`
- Source dry-run review:
  `docs/contract_test_reports/quality_ruff_first_exact_code_dry_run.md`

## Role And Scope

Role performed: Codex B / Module Contract Writer.

This is a contract-only artifact. It does not edit `pyproject.toml`, change CI,
promote Ruff, run Ruff autofix, run unsafe-fix, rerun the all-rules Ruff
advisory measurement, perform broad cleanup, or change product behavior.

## Truth Ownership

Ruff owns only static-analysis findings for an exact command, configured rule
selection, ref/commit, Ruff version, and scan scope.

Ruff does not own parser truth, fixture authority, corpus status, security or
privacy assurance, release readiness, deploy readiness, production readiness,
analytics truth, AI truth, or coaching truth.

## Observed Current Behavior

Current committed Ruff configuration remains:

```toml
[tool.ruff.lint]
select = ["E", "F", "I"]
```

Current GitHub Actions lint command:

```powershell
py -m ruff check src tests tools
```

Current local repo-check lint command:

```powershell
py -m ruff check src tests
```

The source dry-run report confirms:

- PR #600 merged into `main`.
- Merge commit: `cf7147554cdc3c92bfde5d38f4f7afd265bd8b46`.
- GitHub Repo Checks passed.
- GitHub CodeQL checks passed.
- Exact selected-code Ruff validation passed:

```powershell
py -m ruff check src tests tools --select DTZ002,DTZ003,DTZ004,DTZ006,DTZ011,DTZ012,DTZ901
```

- Existing repo Ruff validation passed:

```powershell
py -m ruff check src tests tools
```

- No CI workflow, required status check, Ruff config, local repo-check helper,
  broad Ruff family, all-rules gate, autofix, unsafe-fix, parser behavior,
  fixture, corpus, production, analytics, AI, or coaching behavior changed.

## Readiness Verdict

The first exact-code DTZ tranche is ready for a narrowly scoped blocking
promotion implementation, provided Codex C revalidates the exact codes on the
current base before editing configuration.

No additional advisory dry-run window is required when the implementation base
is still the dry-run merge commit or a descendant that passes the same exact
DTZ command.

```yaml
blocking_promotion_ready: true
additional_dry_run_required_before_codex_c: false
selected_exact_codes:
  - DTZ002
  - DTZ003
  - DTZ004
  - DTZ006
  - DTZ011
  - DTZ012
  - DTZ901
allowed_promotion_shape: exact_codes_only
broad_family_promotion_allowed: false
autofix_allowed: false
unsafe_fix_allowed: false
all_rules_gate_allowed: false
```

## Selected Blocking Tranche

Only these exact rule codes may be promoted under #601:

| Code | Rule title from local Ruff 0.15.12 | Promotion status |
| --- | --- | --- |
| `DTZ002` | `call-datetime-today` | allowed for first blocking tranche |
| `DTZ003` | `call-datetime-utcnow` | allowed for first blocking tranche |
| `DTZ004` | `call-datetime-utcfromtimestamp` | allowed for first blocking tranche |
| `DTZ006` | `call-datetime-fromtimestamp` | allowed for first blocking tranche |
| `DTZ011` | `call-date-today` | allowed for first blocking tranche |
| `DTZ012` | `call-date-fromtimestamp` | allowed for first blocking tranche |
| `DTZ901` | `datetime-min-max` | allowed for first blocking tranche |

Do not promote the broad `DTZ` family. Do not promote `DTZ001`, `DTZ005`, or
`DTZ007` under this issue.

## Recommended Implementation Shape

The safest future Codex C implementation is a single-source Ruff configuration
promotion:

1. Update `pyproject.toml` to add only the selected exact DTZ codes to the
   existing `E`, `F`, and `I` selection.
2. Keep `.github/workflows/repo-checks.yml` using:

```powershell
py -m ruff check src tests tools
```

3. Update `tools/run_repo_checks.ps1` to use the same path scope as CI:

```powershell
py -m ruff check src tests tools
```

4. Do not add a new helper for this first promotion unless Codex C proves that
   native Ruff output is too unclear.
5. Do not pass `--select DTZ...` in CI or repo-check scripts after promotion;
   exact rule ownership should live in `pyproject.toml`.

Rationale:

- `pyproject.toml` is the clearest single source for configured blocking Ruff
  rules.
- Leaving GitHub Actions command shape unchanged avoids duplicating rule codes
  in workflow YAML.
- Aligning the local repo-check helper with CI path scope avoids a split where
  CI checks `tools` but local repo checks do not.
- A separate helper would add ceremony before the first tiny gate needs it.

## Local And CI Parity Contract

After implementation, both local and CI validation should use:

```powershell
py -m ruff check src tests tools
```

Local and CI may differ in runner environment, but they must not differ in Ruff
path scope or selected blocking codes.

`tools/select_validation.py` may continue to recommend the repo Ruff command.
Codex C should update selector metadata only if it discovers stale wording or
a concrete test expectation tied to the old local scope.

## Failure Output Contract

Native Ruff output is acceptable for the first tranche if it reports:

- repo-relative path;
- line/column;
- exact rule code;
- clear rule message;
- no raw private path;
- no raw Ruff JSON;
- no local-only artifact content;
- no secrets, credentials, tokens, webhook URLs, spreadsheet IDs, raw logs,
  generated SQLite content, failed-post queue artifacts, workbook exports, or
  private payloads.

The implementation handoff or PR body must explain that the first new blocking
codes are exact DTZ timezone/naive-datetime guardrails. It must also say this
is not a security, privacy, parser correctness, release readiness, production
readiness, analytics truth, AI truth, or coaching truth claim.

If native Ruff output is not understandable enough in focused validation,
Codex C must stop and route back to Codex B instead of inventing a broad helper
or suppressing messages.

## Stale-Ref Policy

PR #600 proved the exact DTZ command on merge commit
`cf7147554cdc3c92bfde5d38f4f7afd265bd8b46`.

Later roles must apply these rules:

- If the implementation branch starts from `cf714755...`, Codex C still runs
  the exact DTZ command before editing config.
- If `main` advances before or during implementation, Codex C must rebase or
  otherwise refresh and rerun the exact DTZ command on the current base.
- Codex E must treat a missing current-base exact-code validation as a blocking
  contract mismatch.
- Codex G must verify CI/check evidence after any rebase, merge-base change, or
  final push before recommending closure.

## CI Promotion Blockers

Codex C must not implement the gate if any of these are true:

- the current base fails the exact DTZ command before config changes;
- implementation requires source cleanup before the gate is clean;
- implementation would enable broad `DTZ`, broad `ALL`, or any broad family;
- implementation would promote `DTZ001`, `DTZ005`, or `DTZ007`;
- implementation would promote advisory or protected-surface-review-required
  rules;
- implementation would run Ruff autofix, fix-only, or unsafe-fix;
- implementation would rerun or depend on the all-rules advisory scan;
- implementation would commit raw Ruff JSON, raw terminal logs, generated
  artifacts, local-only files, private paths, raw snippets, or fix diffs;
- local and CI command scopes would remain intentionally divergent without a
  documented reason;
- failure output would expose private/local/generated artifacts or imply
  parser/security/release/production/analytics/AI/coaching truth.

## Rollback Or Parking Policy

If the future gate becomes noisy, environment-dependent, or incompatible with
current project conventions, do not broaden ignores or suppressions casually.

Allowed routes:

- Codex D may make a narrow implementation fix if the failure is caused by the
  promotion mechanics.
- Codex E may route back to Codex B if the selected gate shape is wrong.
- Codex G may park the issue open if CI proves unstable or base drift invalidates
  the dry-run evidence.
- A later rollback issue may remove the exact DTZ codes from the blocking
  selection if repeated false positives or environment drift are proven.

Forbidden rollback shortcuts:

- broad `# noqa` additions;
- broad `per-file-ignores`;
- switching to `ALL`;
- running autofix/unsafe-fix;
- weakening existing `E`, `F`, or `I` behavior without a separate contract.

## Protected Surfaces

This contract touches workflow and validation policy only.

Protected surfaces preserved:

- parser behavior;
- parser state final reconciliation;
- parser event classes;
- match/game identity and deduplication;
- fixtures, snapshots, corpus status, and raw evidence promotion;
- #388 and #381 activation state;
- workbook schema;
- webhook payload shape;
- Apps Script and Google Sheets behavior;
- analytics truth;
- AI/coaching/model-provider behavior;
- production behavior;
- secrets, credentials, raw logs, generated data, runtime artifacts,
  failed-post queue artifacts, workbook exports, and local-only artifacts.

CI and validation gates are workflow protected surfaces. This contract may
authorize a later scoped Codex C implementation, but Codex B does not edit CI,
config, scripts, or source.

## Validation Requirements

For this Codex B contract:

```powershell
git status --short --branch
git diff --check -- docs\contracts\quality_ruff_first_exact_code_blocking_promotion.md
py tools\check_agent_docs.py
@'
docs/contracts/quality_ruff_first_exact_code_blocking_promotion.md
'@ | py tools\check_protected_surfaces.py --base origin/main --paths-from-stdin
@'
docs/contracts/quality_ruff_first_exact_code_blocking_promotion.md
'@ | py tools\check_secret_patterns.py --base origin/main --paths-from-stdin
```

For Codex C implementation:

```powershell
git status --short --branch
py -m ruff check src tests tools --select DTZ002,DTZ003,DTZ004,DTZ006,DTZ011,DTZ012,DTZ901
py -m ruff check src tests tools
git diff --check
py tools\check_agent_docs.py
```

If Codex C changes `tools/run_repo_checks.ps1`, run a focused repo-check helper
validation that proves the helper invokes the intended lint scope. If Codex C
changes selector metadata, run the selector tests.

Codex C must also run path-scoped protected-surface and secret/private-marker
scans on changed files and produce:

`docs/implementation_handoffs/quality_ruff_first_exact_code_blocking_promotion_comparison.md`

For Codex E:

- verify exact codes only;
- verify no broad families;
- verify current-base exact DTZ validation;
- verify `pyproject.toml` is the single rule-selection authority;
- verify local and CI command scopes match;
- verify existing `E`, `F`, and `I` behavior remains intact;
- verify no autofix, unsafe-fix, all-rules scan, raw artifact, parser behavior,
  fixture, corpus, production, analytics, AI, or coaching change occurred;
- produce:

`docs/contract_test_reports/quality_ruff_first_exact_code_blocking_promotion.md`

For Codex G:

- verify PR target is `main` only because this quality-tooling lane explicitly
  targets `main`;
- verify CI/check status after final push;
- verify #601 can close only after reviewed implementation merges;
- update tracker #567 without closing it unless the whole Ruff tracker is
  complete.

## Acceptance Criteria

- The contract records that #599 / PR #600 passed exact-code dry-run validation.
- The contract selects exact DTZ codes only.
- The contract authorizes a later Codex C implementation path.
- The contract recommends `pyproject.toml` as the single source of blocking
  Ruff rule selection.
- The contract keeps GitHub Actions command shape simple.
- The contract requires local repo-check scope parity with CI.
- The contract forbids broad families, autofix, unsafe-fix, all-rules gates,
  advisory/protected rule promotion, and truth/readiness overclaims.
- The contract defines Codex C/E/G validation expectations.
- Codex B changes only this contract artifact.

## Out Of Scope

- Editing `pyproject.toml` in Codex B.
- Editing CI in Codex B.
- Editing repo-check helpers in Codex B.
- Running Ruff autofix, fix-only, or unsafe-fix.
- Rerunning the all-rules advisory measurement.
- Broad lint cleanup.
- Broad Ruff family promotion.
- Parser behavior changes.
- Fixture, snapshot, corpus, #388, or #381 activation changes.
- Workbook/webhook/App Script/Sheets changes.
- Production, analytics, AI, coaching, or model-provider changes.
- Security/privacy assurance, release readiness, production readiness, parser
  correctness, analytics truth, AI truth, or coaching truth claims.

## Pasteable Codex C Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison thread.

Repository:
Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/601

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/567

Project roadmap:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Branch:
codex/ruff-first-exact-code-blocking-contract-567 or a fresh implementation
branch from current main if this branch remains contract-only.

Contract:
docs/contracts/quality_ruff_first_exact_code_blocking_promotion.md

Goal:
Compare current Ruff config, CI workflow, local repo-check helper, and the #599
dry-run report against the contract. If current-base exact validation passes,
implement the smallest coherent blocking promotion for only these exact codes:
DTZ002, DTZ003, DTZ004, DTZ006, DTZ011, DTZ012, DTZ901.

Recommended implementation shape:
- Add only the selected exact DTZ codes to pyproject.toml alongside E, F, and I.
- Keep GitHub Actions running py -m ruff check src tests tools.
- Update tools/run_repo_checks.ps1 so local lint uses the same src tests tools
  scope as CI.
- Do not create a separate helper unless native Ruff output is proven too
  unclear and Codex B approves that change.

Do not:
- enable broad DTZ or any broad family;
- promote DTZ001, DTZ005, DTZ007, advisory rules, or protected-surface-review rules;
- run Ruff autofix, fix-only, or unsafe-fix;
- rerun all-rules Ruff advisory measurement;
- perform broad cleanup;
- change parser behavior, parser final reconciliation, parser event classes,
  match/game identity, deduplication, fixtures, corpus status, #388/#381
  activation, workbook/webhook/App Script/Sheets, production, analytics, AI, or
  coaching behavior;
- commit raw Ruff JSON, raw logs, generated/private/local artifacts, raw source
  snippets, fix diffs, secrets, credentials, tokens, webhook URLs, spreadsheet
  IDs, or environment values;
- close tracker #567.

Validation:
- git status --short --branch
- py -m ruff check src tests tools --select DTZ002,DTZ003,DTZ004,DTZ006,DTZ011,DTZ012,DTZ901
- py -m ruff check src tests tools
- focused helper/selector tests if those files change
- git diff --check
- py tools/check_agent_docs.py
- path-scoped protected-surface scan on changed files
- path-scoped secret/private-marker scan on changed files

Final handoff must include:
- role performed
- issue/tracker reviewed
- contract used
- implementation decision
- files changed
- exact-code validation result
- existing Ruff validation result
- protected-surface status
- raw-artifact status
- next recommended role
- workflow_handoff block
```

## Workflow Handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/601"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/567"
  project_roadmap: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contract_test_reports/quality_ruff_first_exact_code_dry_run.md"
  contract_artifact: "docs/contracts/quality_ruff_first_exact_code_blocking_promotion.md"
  target_artifact: "docs/implementation_handoffs/quality_ruff_first_exact_code_blocking_promotion_comparison.md"
  risk_tier: "High workflow risk; low runtime risk"
  base_branch: "main"
  target_branch: "main"
  branch: "codex/ruff-first-exact-code-blocking-contract-567"
  readiness_verdict: "ready_for_exact_dtz_blocking_promotion_after_current_base_validation"
  selected_exact_codes:
    - "DTZ002"
    - "DTZ003"
    - "DTZ004"
    - "DTZ006"
    - "DTZ011"
    - "DTZ012"
    - "DTZ901"
  recommended_implementation_shape: "pyproject_single_source_plus_local_ci_scope_parity"
  codex_b_implemented_behavior: false
  validation:
    - "git diff --check -- docs\\contracts\\quality_ruff_first_exact_code_blocking_promotion.md"
    - "py tools\\check_agent_docs.py"
    - "path-scoped protected-surface scan"
    - "path-scoped secret/private-marker scan"
  stop_conditions:
    - "Do not edit pyproject.toml in Codex B."
    - "Do not change CI in Codex B."
    - "Do not promote Ruff to a blocking gate in Codex B."
    - "Do not enable broad Ruff families."
    - "Do not run Ruff autofix or unsafe-fix."
    - "Do not rerun all-rules Ruff advisory measurement."
```
