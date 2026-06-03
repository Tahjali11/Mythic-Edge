# Private Local V1 High-Risk Scanner Findings Triage Contract

## Module

`private_local_v1_high_risk_scanner_findings_triage`

Plain English: this contract defines the first targeted cleanup tranche for the
highest-risk all-repo secret/private-marker scanner findings before Mythic Edge
claims private-local-v1 private artifact safety.

This is a contract-writing artifact only. It does not implement scanner,
fixture, test, docs, Apps Script, parser, analytics, local app, credential, or
production behavior changes.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/260
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/136
- Source issue: https://github.com/Tahjali11/Mythic-Edge/issues/252
- Source PR: https://github.com/Tahjali11/Mythic-Edge/pull/259
- Branch: `codex/analytics-foundation`
- Expected artifact:
  `docs/contracts/private_local_v1_high_risk_scanner_findings_triage.md`

## Source Artifacts

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/project_roadmap.md`
- issue #260
- issue #252 and PR #259
- issue #136
- `docs/contracts/private_local_v1_private_artifact_scanner_env_ignore_posture.md`
- `docs/contract_test_reports/private_local_v1_private_artifact_scanner_env_ignore_posture.md`
- `docs/contracts/repo_wide_secret_private_marker_scanner.md`
- `docs/contracts/validation_matrix_reconciliation.md`
- `docs/contracts/private_local_v1_clean_checkout_install_launch.md`
- `docs/contract_test_reports/private_local_v1_clean_checkout_install_launch.md`
- `docs/contracts/engineering_maturity_index_open_framework.md`
- `docs/contract_test_reports/engineering_maturity_baseline.md`
- `tools/check_secret_patterns.py`
- `tests/test_check_secret_patterns.py`
- `tools/check_local_environment.py`
- `tools/check_protected_surfaces.py`
- `tools/select_validation.py`

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/136

Tracker #136 remains open. This contract does not mark the tracker complete.

## Risk Tier

High.

Reasons:

- selected findings may represent real credentials, live external endpoints,
  or workbook/export leakage;
- unsafe triage could copy sensitive material into docs, reports, tests,
  issues, commits, or PR text;
- weakening scanner rules would reduce the value of the private-local-v1
  readiness gate;
- selected paths include source, tests, tooling, examples, and Apps Script
  source-adjacent surfaces;
- workbook, webhook, Apps Script, and credential policy are protected surfaces.

## Owning Layer

Primary owner: Quality / Governance.

Supporting area: Generated / Local Artifacts.

## Internal Project Area

Quality / Governance.

## Truth Owner

The repo secret/private-marker scanner owns deterministic repository
content-safety classification and redacted scanner reporting.

The #260 triage report owns selected high-risk finding classification for
private-local-v1 readiness.

This contract does not make the scanner or triage report the owner of:

- parser truth;
- analytics truth;
- workbook schema truth;
- webhook payload truth;
- Apps Script deployment truth;
- credential policy;
- issue closure;
- merge or deployment readiness;
- AI/model-provider truth.

## Bridge-Code Status

`shared_support`

Allowed data flow:

```text
tracked repo files + scanner category findings
  -> redacted high-risk finding summary
  -> per-family triage classification
  -> narrow fixes, explicit deferrals, or follow-up issues
  -> contract-test report
```

Forbidden reverse flow:

- triage must not authorize committing secrets, live endpoints, raw logs,
  generated data, workbook exports, runtime files, failed posts, or local-only
  artifacts;
- triage must not weaken scanner coverage merely to lower counts;
- triage must not change parser, analytics, workbook, webhook, Apps Script,
  local app runtime, AI, model-provider, or production behavior.

## Files Owned By This Contract

This contract owns:

- `docs/contracts/private_local_v1_high_risk_scanner_findings_triage.md`

Expected future implementation/comparison artifact:

- `docs/implementation_handoffs/private_local_v1_high_risk_scanner_findings_triage_comparison.md`

Expected future contract-test/review artifact:

- `docs/contract_test_reports/private_local_v1_high_risk_scanner_findings_triage.md`

Future Codex C may touch only if the comparison proves a specific selected
finding family needs it:

- source, example, test, or tool files containing selected high-risk findings;
- `tools/check_secret_patterns.py`;
- `tests/test_check_secret_patterns.py`;
- `tools/check_local_environment.py`;
- `tools/check_protected_surfaces.py`;
- local artifact or scanner policy docs.

Codex C must route back to Codex B before changing scanner category semantics,
path-scoped scanner strictness, all-repo advisory behavior, credential policy,
environment variable contracts, workbook/webhook/App Script behavior, parser
behavior, analytics behavior, local app runtime behavior, CI gates, or
production behavior.

## Observed Current Behavior

### Source Issue State

- Issue #260 is open and owns the first targeted high-risk scanner-debt
  tranche after PR #259.
- Source issue #252 remains open because full private-local-v1 private artifact
  readiness is not claimed.
- PR #259 merged into `codex/analytics-foundation` at
  `6b9afe9446f9283a854d60010fc75f3a2867f4bc`.
- Tracker #136 remains open.
- Path-scoped scanner safety remains strict.
- All-repo scanner remains advisory.

### Refreshed All-Repo Scanner Summary

Observed on `codex/analytics-foundation` during this contract pass:

```text
mode: all-repo-advisory
result: failed
exit_code: 0
scanned_paths: 750
skipped_paths: 0
forbidden: 540
warnings: 901
```

Selected high-risk category counts:

| Category | Total | Forbidden | Warnings |
| --- | ---: | ---: | ---: |
| `credential_value` | 10 | 10 | 0 |
| `live_webhook_url` | 3 | 3 | 0 |
| `workbook_export_marker` | 3 | 3 | 0 |

Selected category path families:

| Category | Path families observed |
| --- | --- |
| `credential_value` | root script, `examples/`, `src/`, `tests/`, `tools/` |
| `live_webhook_url` | `tests/` |
| `workbook_export_marker` | `tests/`, `tools/` |

Selected finding paths observed without raw values or excerpts:

| Category | Path |
| --- | --- |
| `credential_value` | `backfill_game_log_from_match_logs.py` |
| `credential_value` | `examples/live_print_filtered_v10_fixed.py` |
| `credential_value` | `examples/live_print_filtered_v8.py` |
| `credential_value` | `examples/live_print_filtered_v9.py` |
| `credential_value` | `src/mythic_edge_parser/app/card_catalog.py` |
| `credential_value` | `src/mythic_edge_parser/app/config.py` |
| `credential_value` | `src/mythic_edge_parser/app/grp_id_candidates.py` |
| `credential_value` | `src/mythic_edge_parser/parsers/connection_error.py` |
| `credential_value` | `tests/test_sanitize.py` |
| `credential_value` | `tools/auto_launcher/manasight_launcher_auto.py` |
| `live_webhook_url` | `tests/test_evidence_runtime_status.py` |
| `live_webhook_url` | `tests/test_evidence_validation_report_wiring.py` |
| `live_webhook_url` | `tests/test_parser_diagnostics_mode.py` |
| `workbook_export_marker` | `tests/test_check_protected_surfaces.py` |
| `workbook_export_marker` | `tools/check_protected_surfaces.py` |
| `workbook_export_marker` | `tools/google_apps_script/Code.gs` |

This contract intentionally records paths and scanner category IDs only. It
does not record raw matched values, raw excerpts, endpoint IDs, workbook IDs,
credential-looking strings, private paths, or payloads.

## Contract Decision

Issue #260 is a targeted high-risk triage tranche.

Required scope:

- classify all 16 selected findings in the three high-risk categories;
- fix or route each selected finding family;
- preserve path-scoped scanner strictness;
- preserve all-repo scanner as advisory unless a later contract changes that;
- preserve redaction and no-content-leak behavior;
- produce an implementation handoff and a review/contract-test report.

Not required:

- zero all-repo scanner findings;
- fixing all 540 forbidden findings and 901 warnings;
- rewriting broad scanner policy;
- making all-repo scanner a CI gate;
- closing #252 or tracker #136.

Private-local-v1 private artifact readiness may not be claimed while any
selected high-risk finding remains unclassified or unresolved without an
explicit deferral and follow-up route.

## Public Interface

Commands governed by this contract:

```powershell
py tools\check_secret_patterns.py --all
py tools\check_secret_patterns.py --base origin/codex/analytics-foundation
@'
<repo-relative paths>
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
py -m pytest -q tests\test_check_secret_patterns.py tests\test_check_local_environment.py tests\test_check_protected_surfaces.py
git diff --check
py tools\check_agent_docs.py
py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation
```

Required future report artifacts:

- implementation comparison/handoff;
- contract-test or review report;
- optional GitHub issue comments summarizing classification counts without raw
  values.

## Inputs

Allowed inputs:

- tracked repo file paths from `git ls-files`;
- changed repo file paths from `<base>...HEAD`;
- scanner findings with category, severity, repo-relative path, line number,
  and redacted reason/excerpt;
- scanner tests and scanner code;
- policy docs and prior #252 report;
- issue #260 problem representation;
- path-scoped scanner/protected-surface results.

Forbidden inputs:

- raw credential values;
- live endpoint values;
- raw workbook IDs or spreadsheet IDs;
- raw Apps Script deployment IDs;
- raw workbook exports;
- raw Player.log content;
- private JSONL payloads;
- generated SQLite contents;
- runtime payloads;
- failed-post payloads;
- secrets, tokens, API keys, OAuth values, LLM provider keys, environment
  values, or local-only private paths.

## Outputs

Required Codex C output:

- files inspected;
- selected finding count by category and severity;
- selected finding count by path family;
- selected finding classification table;
- exact files changed;
- per-finding-family resolution:
  - removed;
  - replaced with safe placeholder;
  - converted to synthetic/test-only builder;
  - confirmed expected policy text;
  - confirmed scanner false positive with rationale;
  - deferred with follow-up issue;
- validation evidence;
- remaining high-risk findings, if any;
- protected-surface status;
- secret/private-marker status.

Forbidden output:

- raw matched values;
- raw endpoints;
- raw workbook IDs;
- raw secret examples;
- raw private local paths;
- raw Player.log lines;
- private payload excerpts;
- local generated artifact contents.

## Triage Classification Vocabulary

Each selected finding family must be assigned exactly one primary
classification.

### `real_risk_fix_required`

Use when the finding may represent real sensitive material, a live external
endpoint, a workbook/export marker that should not be committed, or a source
file default that could cause unsafe behavior.

Required outcome:

- remove it;
- replace it with a placeholder;
- move it out of tracked source;
- or route to a focused follow-up if removal requires behavior changes outside
  #260.

### `expected_policy_or_contract_text`

Use when policy text intentionally names a scanner category, protected surface,
or forbidden concept.

Allowed only when:

- no raw sensitive value is present;
- wording is needed for policy clarity;
- scanner behavior remains strict for non-policy paths.

### `expected_synthetic_or_sanitized_test`

Use when tests intentionally construct synthetic dangerous-looking values to
prove redaction or detection behavior.

Required safeguards:

- values are built from clearly synthetic fragments;
- assertions prove rendered reports do not contain raw matched values;
- tests do not use copied live endpoints, workbook IDs, or credentials;
- scanner findings are not hidden merely because they are in tests.

### `expected_placeholder_or_example`

Use when examples or docs contain clearly fake, redacted, placeholder, or
sample values.

Required safeguards:

- placeholder context must be explicit near the value;
- example code must not make a real external call by default;
- example code must not encourage storing real credentials in source.

### `scanner_false_positive`

Use only when the scanner category is technically matched but the content is
safe and rewriting would make the repo less clear.

Required rationale:

- path;
- category;
- why it is safe;
- why rewrite is not better;
- test or policy evidence preserving scanner value.

False positives must not be suppressed globally without focused tests.

### `defer_with_reason`

Use when resolution requires a separate issue because it would affect protected
surfaces, legacy tooling, external integrations, Apps Script deployment
assumptions, parser behavior, credential policy, or broader scanner semantics.

Required follow-up:

- issue title or draft issue body;
- category and path family;
- reason not fixed in #260;
- protected surfaces involved;
- validation required before closure.

## Category-Specific Requirements

### `credential_value`

Required inspection:

- determine whether each finding is a real credential-looking default,
  placeholder missing explicit context, synthetic test data, legacy copied
  utility code, or scanner false positive;
- do not print the matched value;
- do not run code paths that could use the value;
- do not replace with another live-looking value.

Preferred fixes:

- remove credential-looking defaults;
- replace with explicit placeholder text;
- construct synthetic test values from fragments inside tests;
- move any real credential requirement to documented local environment setup
  without changing environment variable contracts.

Stop and route back if:

- a source file appears to embed a real credential;
- changing the line would alter runtime credential loading behavior;
- the fix would require credential rotation, environment contract changes, or
  external system changes.

### `live_webhook_url`

Required inspection:

- determine whether each test path uses a synthetic live-looking endpoint only
  to prove scanner/protected behavior;
- verify report redaction tests prevent raw endpoint output;
- do not copy the matched URL into handoffs, reports, commits, or comments.

Preferred fixes:

- build synthetic endpoints from fragments in tests;
- replace full live-looking literals with non-live placeholder values if the
  test does not need scanner detection;
- keep tests focused on redaction and scanner behavior.

Stop and route back if:

- a matched endpoint could be live or copied from production;
- changing it would affect webhook payload shape, Apps Script behavior, Google
  Sheets behavior, or production transport.

### `workbook_export_marker`

Required inspection:

- determine whether each finding is a synthetic scanner/protected-surface test,
  a policy/tooling regex example, an Apps Script placeholder, or a real workbook
  export/spreadsheet marker;
- do not print workbook IDs or export contents;
- treat Apps Script-adjacent findings as protected until proven placeholder.

Preferred fixes:

- convert test values to synthetic builders;
- replace real-looking workbook identifiers with placeholder labels;
- keep scanner/protected-surface tests proving detection without embedding live
  workbook identifiers;
- route Apps Script-related changes through a protected-surface review if a
  behavior change would be required.

Stop and route back if:

- a matched value appears to be a real workbook ID or exported workbook data;
- the fix would alter Apps Script behavior, workbook schema, webhook payload
  shape, or deployment assumptions.

## Required Guarantees

- Selected findings are summarized by count/category/path family before any
  edits.
- No raw matched value is copied into docs, reports, issues, PR text, tests, or
  commit messages.
- Any file edit is tied to a selected finding family.
- Path-scoped scanner forbidden findings remain failing.
- All-repo scanner remains advisory unless a later contract authorizes
  escalation.
- Warnings are not silently treated as proof of safety.
- Suppression, downgrade, or allowlist behavior requires explicit policy
  rationale and tests.
- Scanner redaction tests must remain intact.
- Tests that need dangerous-looking values must construct synthetic values or
  use explicit placeholders.
- No raw local/private/generated artifact is created, copied, sanitized,
  imported, committed, or moved.
- Private-local-v1 readiness language must distinguish:
  - selected high-risk tranche status;
  - remaining all-repo scanner debt;
  - overall #252 readiness;
  - tracker #136 lifecycle.

## Error Behavior

If a selected finding cannot be classified safely:

- do not edit around it blindly;
- mark it `defer_with_reason`;
- propose a follow-up issue;
- keep #252 open;
- do not claim private-local-v1 private artifact readiness.

If scanner output prints unsafe raw values:

- stop;
- do not paste the output;
- route to Codex D/C for scanner redaction fix;
- validate with focused redaction tests before continuing.

If a selected finding appears to be a real secret or live external endpoint:

- do not print it;
- notify the user with only the repo-relative path and scanner category;
- request explicit user direction for rotation/removal if needed;
- do not rotate credentials without explicit approval.

If a fix would touch protected behavior:

- stop and route back to Codex A/B for a separate issue/contract.

## Side Effects

Codex B side effects:

- create this contract only.

Future Codex C side effects allowed by this contract:

- create implementation handoff;
- edit selected source/example/test/tooling/doc files only as needed to resolve
  selected high-risk findings;
- add or update focused scanner tests;
- create a review/contract-test report.

Forbidden side effects:

- read, print, copy, sanitize, import, move, delete, or commit private local
  artifacts;
- create generated SQLite files or app-data artifacts;
- alter parser behavior;
- alter analytics schema, migrations, ingest, or views;
- alter workbook schema;
- alter webhook payload shape;
- alter Apps Script behavior;
- alter Google Sheets behavior;
- alter local app runtime behavior;
- alter production behavior;
- alter OpenAI/model-provider or AI/coaching behavior;
- alter credential or environment variable contracts;
- add CI gates;
- make all-repo scanner a failing gate;
- target `main`;
- close #252 or #136.

## Dependency Order

Future implementation should proceed in this order:

1. Confirm branch and clean state.
2. Re-run all-repo scanner and summarize selected categories only.
3. Re-run changed-file scanner against `origin/codex/analytics-foundation`.
4. Build a selected finding inventory with category, severity, path, line, and
   reason, but no raw excerpt or raw value.
5. Classify each finding family using this contract vocabulary.
6. Fix the lowest-risk selected findings first:
   - synthetic tests;
   - placeholder/example text;
   - policy/tooling text.
7. Treat source and Apps Script-adjacent findings as higher risk and preserve
   behavior unless a safe placeholder change is obvious and tested.
8. Add focused scanner/protected-surface tests when rule behavior, test
   builders, or placeholder policy changes.
9. Run validation.
10. Produce implementation handoff.
11. Route to Codex E for independent review/contract testing.

## Compatibility

Preserve:

- #252 `.env*` ignore posture;
- exact root `.env.example` template allowance;
- path-scoped scanner strictness;
- all-repo scanner advisory mode and exit behavior;
- current scanner redaction guarantees;
- protected-surface gate behavior;
- local environment checker no-private-content-read behavior;
- #253 private-local-v1 install proof state;
- parser, analytics, workbook, Apps Script, local app, production, and AI
  behavior.

## Unknowns

- Whether any selected `credential_value` source findings are real risks,
  placeholder gaps, or scanner false positives is not known until Codex C
  inspects the exact lines without copying values.
- Whether the Apps Script-adjacent `workbook_export_marker` finding is safe
  placeholder text or a real protected value is not known from path/category
  alone.
- Whether selected test findings should be rewritten as synthetic builders or
  kept as documented scanner-test fixtures requires Codex C comparison.
- Whether a small scanner summary helper is needed is unknown. If added, it
  must not output raw excerpts or values.

## Suspected Gaps

- Some scanner tests likely use full dangerous-looking literals where split
  synthetic builders would prove the same behavior with less all-repo debt.
- Some examples or legacy tools may contain credential-looking defaults that
  need explicit placeholder context.
- Source files may include values that are safe but scanner-hostile because
  they lack placeholder labels.
- Tooling and Apps Script-adjacent workbook markers may need clearer placeholder
  vocabulary or test fixtures.
- All-repo scanner has no machine-readable allowlist/baseline policy; #260
  should not invent one broadly.

## Tests Required

Minimum validation for Codex C:

```powershell
py tools\check_secret_patterns.py --all
py tools\check_secret_patterns.py --base origin/codex/analytics-foundation
py -m pytest -q tests\test_check_secret_patterns.py tests\test_check_local_environment.py tests\test_check_protected_surfaces.py
git diff --check
py tools\check_agent_docs.py
py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation
```

If Codex C changes only docs and reports, focused path-scoped protected-surface
and secret/private-marker scans over touched paths are sufficient in addition
to `git diff --check` and agent docs check.

If Codex C changes scanner code or scanner tests, required validation includes:

```powershell
py -m pytest -q tests\test_check_secret_patterns.py
py -m pytest -q tests\test_check_secret_patterns.py tests\test_check_local_environment.py tests\test_check_protected_surfaces.py
py tools\check_secret_patterns.py --all
py tools\check_secret_patterns.py --base origin/codex/analytics-foundation
py -m ruff check tools tests
```

If Codex C touches source/example/tool files outside scanner tooling, run the
focused tests selected by `tools/select_validation.py` or justify why none are
needed.

Validation reports must summarize all-repo scanner output by count/category and
path family only. Do not paste every scanner line.

## Acceptance Criteria

- Contract artifact exists at
  `docs/contracts/private_local_v1_high_risk_scanner_findings_triage.md`.
- Current high-risk scanner counts are recorded without raw values.
- Triage vocabulary is defined.
- Category-specific requirements are defined for `credential_value`,
  `live_webhook_url`, and `workbook_export_marker`.
- Safe inspection and redaction requirements are defined.
- Required guarantees, unknowns, suspected gaps, and protected surfaces are
  defined.
- Validation requirements are defined.
- Codex C handoff is provided.
- No code or behavior changes are made by Codex B.

Future #260 completion requires:

- every selected high-risk finding family classified;
- each selected finding removed, safely rewritten, confirmed synthetic,
  confirmed policy/placeholder, confirmed false positive with rationale, or
  deferred with a concrete follow-up;
- path-scoped scanner strictness preserved;
- all-repo scanner debt not hidden;
- no raw private/sensitive values printed or committed.

## Next Workflow Action

Next recommended role: Codex C / Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison thread for issue #260.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/260

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/136

Source issue:
https://github.com/Tahjali11/Mythic-Edge/issues/252

Source PR:
https://github.com/Tahjali11/Mythic-Edge/pull/259

Branch:
codex/analytics-foundation

Contract:
docs/contracts/private_local_v1_high_risk_scanner_findings_triage.md

Goal:
Compare the current all-repo scanner findings against the #260 contract. Produce docs/implementation_handoffs/private_local_v1_high_risk_scanner_findings_triage_comparison.md and implement only narrow fixes for the selected high-risk categories if they are safe and contract-aligned.

Before editing:
- confirm branch and git status;
- inspect issue #260, issue #252, PR #259, and tracker #136;
- rerun the scanner summary without raw values;
- state what high-risk scanner triage is supposed to do, what the scanner is actually reporting, why the findings matter, and the exact minimal comparison/implementation plan.

In scope:
- selected categories only: credential_value, live_webhook_url, workbook_export_marker;
- classify each selected finding family;
- remove or rewrite unsafe values;
- convert test-only findings to safe synthetic builders where appropriate;
- preserve scanner redaction and path-scoped strictness;
- add/update focused tests only when behavior or fixtures change;
- produce implementation handoff.

Do not:
- print or copy raw matched values, endpoints, workbook IDs, spreadsheet IDs, secrets, tokens, keys, raw logs, private JSONL payloads, generated SQLite contents, failed-post payloads, runtime payloads, or private local paths;
- weaken scanner coverage;
- suppress findings without explicit policy rationale and tests;
- fix all all-repo scanner categories;
- make all-repo scanner a failing gate;
- add CI gates;
- change parser behavior, parser state final reconciliation, parser event classes, match/game identity, deduplication, analytics behavior, SQLite schema/migrations, local app runtime behavior, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets behavior, production behavior, OpenAI/model-provider behavior, AI/coaching behavior, credential policy, or environment variable contracts;
- target main;
- close #252 or tracker #136.

Validation:
- py tools\check_secret_patterns.py --all
- py tools\check_secret_patterns.py --base origin/codex/analytics-foundation
- py -m pytest -q tests\test_check_secret_patterns.py tests\test_check_local_environment.py tests\test_check_protected_surfaces.py
- git diff --check
- py tools\check_agent_docs.py
- py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation
- path-scoped secret/private-marker and protected-surface scans over touched files

Output:
- role performed;
- contract compared;
- files inspected;
- selected high-risk scanner summary;
- classification table;
- files changed;
- validation run;
- remaining high-risk findings;
- protected-surface status;
- next recommended role: Codex E;
- pasteable Codex E prompt;
- workflow_handoff block.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/260"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/136"
  source_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/252"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "GitHub issue #260 problem representation"
  target_artifact: "docs/implementation_handoffs/private_local_v1_high_risk_scanner_findings_triage_comparison.md"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  validation:
    - "git diff --check"
    - "py tools/check_agent_docs.py"
    - "path-scoped protected-surface scan for docs/contracts/private_local_v1_high_risk_scanner_findings_triage.md"
    - "path-scoped secret/private-marker scan for docs/contracts/private_local_v1_high_risk_scanner_findings_triage.md"
  stop_conditions:
    - "Do not implement code in Codex B."
    - "Do not print or copy raw matched values or private artifacts."
    - "Do not weaken scanner coverage or suppress findings without explicit policy rationale and tests."
    - "Do not fix all all-repo scanner categories under #260."
    - "Do not make all-repo scanner a failing gate or add CI gates."
    - "Do not change parser/runtime/analytics/local app/workbook/webhook/App Script/Sheets/OpenAI/AI/production behavior."
    - "Do not change credential policy or environment variable contracts."
    - "Do not target main, close #252, or close tracker #136."
```
