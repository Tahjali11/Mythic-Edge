# Quality Ruff Current Advisory Remeasurement After Second Tranche

## Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/613
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/567
- Project roadmap: https://github.com/Tahjali11/Mythic-Edge/issues/568
- Source contract:
  `docs/contracts/quality_ruff_current_advisory_measurement_report.md`

## Role Performed

Codex C: approval-gated Ruff advisory measurement executor.

## Approval Scope Used

```yaml
ruff_measurement_execution_authorized: true
report_artifact_creation_authorized: true
measured_ref: "origin/main"
measured_commit: "62bc9c2a61b414d5e168148cb078a44842fc42bc"
raw_ruff_json_commit_authorized: false
raw_ruff_json_local_only: true
blocking_promotion_authorized: false
autofix_authorized: false
unsafe_fix_authorized: false
```

## Measurement Base

- Repository: `Tahjali11/Mythic-Edge`
- Working branch: `codex/ruff-remeasurement-after-second-tranche-567`
- Target ref: `origin/main`
- Approved target commit:
  `62bc9c2a61b414d5e168148cb078a44842fc42bc`
- Measured checkout commit:
  `62bc9c2a61b414d5e168148cb078a44842fc42bc`
- Ruff version: `ruff 0.15.12`

The worktree was clean before measurement and was exactly on the approved
commit. No CI, Ruff config, source, parser, corpus, workbook, webhook, Apps
Script, analytics, AI, coaching, release, deploy, or production behavior was
changed.

## Commands

The all-rules Ruff advisory measurement was run with `--exit-zero` and wrote
raw JSON only under ignored local evidence storage:

```text
py -m ruff check src tests tools --select ALL --exit-zero --output-format json --output-file <local-only-raw-json>
```

The exact Ruff rule catalog was captured locally with:

```text
py -m ruff rule --all --output-format json
```

The sanitized report was generated with:

```text
py tools/generate_ruff_advisory_report.py --input <local-only-raw-json> --rule-codes-file <local-only-rule-codes-json> --branch-or-ref origin/main --commit 62bc9c2a61b414d5e168148cb078a44842fc42bc --ruff-version "ruff 0.15.12" --scan-scope src tests tools --command "py -m ruff check src tests tools --select ALL --exit-zero --output-format json --output-file <local-only-raw-json>" --measured-checkout-root <clean-measured-checkout-root>
```

The raw all-rules Ruff JSON, raw Ruff rule catalog, and temporary exact
rule-code list remain local-only and uncommitted.

## Report Produced

Created sanitized report artifact:

- `docs/quality_reports/ruff_advisory/2026-07-01-62bc9c2-ruff-advisory-report.json`

Summary:

```yaml
schema_version: "quality_ruff_advisory_report.v1"
commit: "62bc9c2a61b414d5e168148cb078a44842fc42bc"
ruff_version: "ruff 0.15.12"
findings: 17984
triggered_rule_codes: 116
rule_summaries: 956
zero_baseline_candidates: 840
dispositions:
  advisory: 35
  protected_surface_review_required: 81
  zero_baseline_candidate: 840
```

The previous committed report at commit `51d5d8352c10204663d904765a8820bb464a52ac`
recorded `17665` findings, `115` triggered rule codes, and `841`
zero-baseline candidates. This new report is the fresher post-#608/#611
measurement evidence for future Ruff tranche selection.

## Files Changed

- `docs/quality_reports/ruff_advisory/2026-07-01-62bc9c2-ruff-advisory-report.json`
- `docs/implementation_handoffs/quality_ruff_current_advisory_remeasurement_after_second_tranche.md`

## Boundaries Preserved

- no raw Ruff JSON committed;
- no raw Ruff rule catalog committed;
- no local absolute paths, raw terminal logs, raw diagnostics, source patches,
  autofix diffs, private logs, generated SQLite files, runtime files, failed
  posts, workbook exports, secrets, credentials, tokens, private paths, or
  local-only artifacts committed;
- no CI change;
- no `pyproject.toml` Ruff rule-selection change;
- no blocking Ruff promotion;
- no Ruff autofix or unsafe fix;
- no parser behavior, corpus, workbook, webhook, Apps Script, analytics, AI,
  coaching, release, deploy, or production behavior change.

## Validation

Passed:

- `py -m json.tool docs\quality_reports\ruff_advisory\2026-07-01-62bc9c2-ruff-advisory-report.json`
- `PYTHONDONTWRITEBYTECODE=1 py -m pytest -q tests\test_ruff_advisory_report.py`
  - `41 passed`
- `py -m ruff check src tests tools`
  - `All checks passed!`
- `git diff --check`
- `py tools\check_agent_docs.py`
  - `errors: 0`, `warnings: 0`
- `py tools\check_protected_surfaces.py --base origin/main --paths-from-stdin`
  - `forbidden: 0`, `warnings: 0`
- `py tools\check_secret_patterns.py --base origin/main --paths-from-stdin`
  - `forbidden: 0`, `warnings: 0`

## Still Out Of Scope

- additional Ruff rule promotion;
- broad Ruff family enablement;
- Ruff preview mode;
- Ruff autofix or unsafe fix;
- CI changes;
- tracker #567 closure;
- parser correctness, security assurance, privacy assurance, release readiness,
  deploy readiness, production readiness, analytics truth, AI truth, or
  coaching truth claims.

## Recommended Next Role

Codex E: review the sanitized report and this handoff against issue #613 and
the source contract, then route to Codex F only if the measurement package is
safe to publish.

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/613"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/567"
  project_roadmap: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/quality_ruff_current_advisory_measurement_report.md"
  produced_artifacts:
    - "docs/quality_reports/ruff_advisory/2026-07-01-62bc9c2-ruff-advisory-report.json"
    - "docs/implementation_handoffs/quality_ruff_current_advisory_remeasurement_after_second_tranche.md"
  measured_ref: "origin/main"
  measured_commit: "62bc9c2a61b414d5e168148cb078a44842fc42bc"
  ruff_version: "ruff 0.15.12"
  findings: 17984
  triggered_rule_codes: 116
  rule_summaries: 956
  zero_baseline_candidates: 840
  raw_ruff_json_committed: false
  raw_ruff_json_local_only: true
  blocking_promotion_authorized: false
  autofix_authorized: false
  unsafe_fix_authorized: false
  ci_changed: false
  parser_behavior_change_authorized: false
  validation:
    - "sanitized report JSON validated"
    - "focused Ruff advisory report tests passed: 41 passed"
    - "current Ruff gate passed"
    - "git diff --check passed"
    - "agent docs check passed"
    - "changed-file protected-surface scan passed: forbidden 0, warnings 0"
    - "changed-file secret/private-marker scan passed: forbidden 0, warnings 0"
  validation_status: "passed"
```
