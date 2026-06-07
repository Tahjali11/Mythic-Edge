# Private Local V1 Raw/Private Artifact Scanner Triage Contract

## Module

`private_local_v1_raw_private_artifact_scanner_triage`

Plain English: this contract defines the next private-local-v1 all-repo scanner
triage tranche after the credential, live endpoint, and workbook-marker tranche.
It covers raw/private artifact categories that may indicate tracked
Player.log-like content, runtime status payloads, generated data dumps,
failed-post payloads, or private local paths.

This is a contract-writing artifact only. It does not implement scanner,
fixture, test, docs, parser, analytics, local app, workbook, webhook, Apps
Script, credential, or production behavior changes.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/262
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/136
- Source issues:
  - https://github.com/Tahjali11/Mythic-Edge/issues/252
  - https://github.com/Tahjali11/Mythic-Edge/issues/260
- Source PRs:
  - https://github.com/Tahjali11/Mythic-Edge/pull/259
  - https://github.com/Tahjali11/Mythic-Edge/pull/261
- Branch: `codex/analytics-foundation`
- Expected artifact:
  `docs/contracts/private_local_v1_raw_private_artifact_scanner_triage.md`

## Source Artifacts

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/project_roadmap.md`
- issue #262
- issue #260 and PR #261
- issue #252 and PR #259
- tracker #136
- `docs/contracts/private_local_v1_high_risk_scanner_findings_triage.md`
- `docs/implementation_handoffs/private_local_v1_high_risk_scanner_findings_triage_comparison.md`
- `docs/contract_test_reports/private_local_v1_high_risk_scanner_findings_triage.md`
- `docs/contracts/private_local_v1_private_artifact_scanner_env_ignore_posture.md`
- `docs/contract_test_reports/private_local_v1_private_artifact_scanner_env_ignore_posture.md`
- `docs/contracts/repo_wide_secret_private_marker_scanner.md`
- `docs/contracts/validation_matrix_reconciliation.md`
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

- the selected scope contains 524 forbidden all-repo findings;
- selected findings may indicate raw log-like content, runtime status payloads,
  generated data, failed-post payloads, or private machine-local paths;
- unsafe triage could copy private content into docs, reports, tests, issues,
  commits, or PR text;
- selected findings span tests, parser/source modules, tooling, docs, and
  historical workflow artifacts;
- large-scale rewrites could accidentally change parser, diagnostics, runtime,
  scanner, or protected-surface behavior.

## Owning Layer

Primary owner: Quality / Governance.

Supporting area: Generated / Local Artifacts.

## Internal Project Area

Quality / Governance.

## Truth Owner

The repo secret/private-marker scanner owns deterministic repository
content-safety classification and redacted scanner reporting.

The #262 triage report owns selected raw/private artifact finding
classification for private-local-v1 readiness.

This contract does not make the scanner or triage report the owner of:

- parser truth;
- analytics truth;
- workbook schema truth;
- webhook payload truth;
- Apps Script truth;
- runtime status truth;
- fixture provenance truth;
- credential policy;
- merge, deploy, issue, or tracker readiness;
- AI/model-provider truth.

## Bridge-Code Status

`shared_support`

Allowed data flow:

```text
tracked repo files + scanner category findings
  -> redacted raw/private artifact summary
  -> category/family classification
  -> scoped fix candidates, explicit deferrals, or follow-up issues
  -> implementation handoff and review report
```

Forbidden reverse flow:

- triage must not authorize committing raw logs, runtime payloads, failed-post
  payloads, generated data dumps, workbook exports, private local paths,
  secrets, credentials, or local-only artifacts;
- triage must not weaken scanner coverage merely to reduce counts;
- triage must not change parser, analytics, workbook, webhook, Apps Script,
  local app runtime, AI, model-provider, or production behavior.

## Files Owned By This Contract

This contract owns:

- `docs/contracts/private_local_v1_raw_private_artifact_scanner_triage.md`

Expected future implementation/comparison artifact:

- `docs/implementation_handoffs/private_local_v1_raw_private_artifact_scanner_triage_comparison.md`

Expected future contract-test/review artifact:

- `docs/contract_test_reports/private_local_v1_raw_private_artifact_scanner_triage.md`

Future Codex C may touch only if the comparison proves a specific selected
finding family needs it:

- selected test, fixture, docs, source, example, or tool files;
- `tools/check_secret_patterns.py`;
- `tests/test_check_secret_patterns.py`;
- `tools/check_local_environment.py`;
- `tools/check_protected_surfaces.py`;
- local artifact or scanner policy docs.

Codex C must route back to Codex B before changing scanner category semantics,
path-scoped scanner strictness, all-repo advisory behavior, fixture provenance
policy, parser behavior, runtime behavior, analytics behavior, workbook/webhook
or Apps Script behavior, local app runtime behavior, CI gates, production
behavior, credential policy, or environment variable contracts.

## Observed Current Behavior

### Source Issue State

- Issue #262 is open and owns the raw/private artifact scanner-debt tranche.
- Issue #260 / PR #261 merged the selected high-risk scanner triage package
  for credential, live endpoint, and workbook marker categories.
- Issue #252 remains open because full private-local-v1 private artifact
  readiness is not claimed.
- Tracker #136 remains open.
- Path-scoped scanner safety remains strict.
- All-repo scanner remains advisory and non-clean.

### Refreshed All-Repo Scanner Summary

Observed on `codex/analytics-foundation` during this contract pass:

```text
mode: all-repo-advisory
result: failed
exit_code: 0
scanned_paths: 753
skipped_paths: 0
forbidden: 540
warnings: 901
```

Selected raw/private artifact category counts:

| Category | Total | Forbidden | Warnings |
| --- | ---: | ---: | ---: |
| `raw_player_log_content` | 335 | 335 | 0 |
| `runtime_status_payload` | 85 | 85 | 0 |
| `generated_data_dump` | 38 | 38 | 0 |
| failed-post payload category | 9 | 9 | 0 |
| `private_local_path` | 57 | 57 | 0 |

The failed-post payload category is written in scanner-safe prose in this
contract so the contract does not create warning-only self-findings. Codex C
must use the exact category ID reported by `tools/check_secret_patterns.py` and
issue #262 when building the implementation inventory.

Warning-only categories deferred from this issue:

| Category | Total | Forbidden | Warnings |
| --- | ---: | ---: | ---: |
| `artifact_path_reference` | 635 | 0 | 635 |
| `sanitized_fixture_marker` | 174 | 0 | 174 |
| `ambiguous_private_marker` | 80 | 0 | 80 |
| `placeholder_secret_reference` | 9 | 0 | 9 |
| `decode_replacement_used` | 3 | 0 | 3 |

### Selected Path-Family Shape

Selected findings by broad path family:

| Category | Path families observed |
| --- | --- |
| `raw_player_log_content` | `tests/`, `src/`, `docs/problem_representations/` |
| `runtime_status_payload` | `tests/`, `src/`, `tools/`, `tests/fixtures/` |
| `generated_data_dump` | `tests/`, `src/`, `tools/`, `docs/` |
| failed-post payload category | `src/`, `tools/`, `docs/problem_representations/` |
| `private_local_path` | `docs/contract_test_reports/`, `docs/implementation_handoffs/`, `src/`, `tests/`, `docs/contracts/`, `examples/`, `tools/` |

Highest-count selected paths observed without raw values or excerpts:

| Category | Count | Path |
| --- | ---: | --- |
| `raw_player_log_content` | 88 | `src/mythic_edge_parser/app/evidence_ledger.py` |
| `raw_player_log_content` | 35 | `tests/test_parsers.py` |
| `raw_player_log_content` | 21 | `tests/test_parser_small_modules.py` |
| `raw_player_log_content` | 18 | `tests/test_connection_parsers.py` |
| `runtime_status_payload` | 19 | `src/mythic_edge_parser/app/parser_diagnostics.py` |
| `runtime_status_payload` | 15 | `tests/test_gameplay_actions.py` |
| `runtime_status_payload` | 14 | `tests/test_sheet_exports.py` |
| `generated_data_dump` | 13 | `tests/test_card_catalog.py` |
| `generated_data_dump` | 7 | `src/mythic_edge_parser/app/card_catalog.py` |
| failed-post payload category | 4 | `src/mythic_edge_parser/app/parser_diagnostics.py` |
| `private_local_path` | 6 | `docs/implementation_handoffs/player_log_evidence_ledger_schema_snapshot_builder_comparison.md` |
| `private_local_path` | 4 | `tests/test_sanitize.py` |

This contract intentionally records category IDs, counts, and repo-relative
paths only. It does not record raw matched values, raw excerpts, raw log-like
lines, raw payload text, private paths, local user names, generated data
contents, workbook contents, endpoint values, credential values, or environment
values.

## Contract Decision

Issue #262 is a targeted raw/private artifact triage tranche.

Required scope:

- classify selected finding families in these categories:
  - `raw_player_log_content`;
  - `runtime_status_payload`;
  - `generated_data_dump`;
  - failed-post payload category;
  - `private_local_path`;
- preserve path-scoped scanner strictness;
- preserve all-repo scanner as advisory unless a later contract changes that;
- preserve redaction and no-content-leak behavior;
- separate report-only classification from concrete remediation;
- route broad or protected-surface remediation to follow-up issues;
- produce an implementation handoff and a review/contract-test report.

Not required:

- zero all-repo scanner findings;
- fixing all 540 forbidden findings and 901 warnings;
- handling warning-only categories except as background context;
- rewriting broad scanner policy;
- making all-repo scanner a CI gate;
- closing #252, #260, or tracker #136.

Private-local-v1 private artifact readiness may not be claimed while any
selected raw/private artifact family remains unclassified or unresolved without
an explicit deferral and follow-up route.

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
  and reason;
- scanner redacted excerpts only when needed for local inspection, not copied
  into durable reports;
- scanner tests and scanner code;
- policy docs and prior #252/#260 reports;
- issue #262 problem representation;
- path-scoped scanner/protected-surface results.

Forbidden inputs:

- raw log-like lines;
- raw runtime payloads;
- raw failed-post payloads;
- generated data dumps;
- private local paths or local user names;
- private JSONL payloads;
- generated SQLite contents;
- raw workbook exports;
- secrets, credentials, endpoint URLs, tokens, keys, OAuth values, provider
  keys, spreadsheet IDs, or environment values.

## Outputs

Required Codex C output:

- files inspected;
- selected finding count by category and severity;
- selected finding count by path family;
- classification matrix by category/path family;
- high-risk concrete fix candidates;
- expected synthetic/test fixture families;
- expected policy/docs families;
- scanner false positives, if any;
- explicit deferrals and follow-up issue routes;
- exact files changed, if any;
- validation evidence;
- remaining selected findings;
- protected-surface status;
- secret/private-marker status.

Forbidden output:

- raw log-like lines;
- raw runtime payloads;
- raw failed-post payloads;
- generated data contents;
- private local paths;
- local user names;
- private payload excerpts;
- endpoint values;
- workbook IDs;
- secrets, tokens, keys, credentials, or environment values.

## Triage Classification Vocabulary

Each selected finding family must be assigned exactly one primary
classification.

### `real_artifact_leakage_fix_required`

Use when the finding may represent committed raw/private artifact content,
private machine-local state, generated data, runtime payloads, failed-post
payloads, or data copied from a live/private environment.

Required outcome:

- remove it;
- replace it with placeholder or synthetic text;
- move it out of tracked source;
- or route to a focused follow-up if removal requires protected behavior
  changes.

### `expected_synthetic_or_sanitized_fixture`

Use when tests or fixtures intentionally include synthetic or sanitized marker
shapes to prove parser, scanner, sanitizer, evidence-ledger, or diagnostics
behavior.

Required safeguards:

- no real private value is present;
- fixture/test purpose is explicit;
- synthetic data is built or labeled clearly enough for review;
- scanner redaction behavior remains tested;
- future fixture changes follow golden fixture policy when applicable.

### `expected_policy_or_contract_text`

Use when docs, contracts, handoffs, or reports intentionally discuss protected
surfaces, path families, scanner categories, or historical workflow findings.

Allowed only when:

- no raw private content is present;
- wording is necessary for policy clarity;
- scanner behavior remains strict for non-policy paths.

### `expected_placeholder_or_example`

Use when examples or docs contain clearly fake, placeholder, sample, redacted,
or configured values.

Required safeguards:

- placeholder context must be explicit near the value;
- example code must not read or write private artifacts by default;
- example code must not encourage committing local/generated/private state.

### `scanner_false_positive`

Use only when the scanner category is technically matched but the text is safe
and rewriting would reduce clarity or scanner value.

Required rationale:

- path or path family;
- category;
- why it is safe;
- why rewrite is not better;
- test or policy evidence preserving scanner value.

False positives must not be suppressed globally without focused tests.

### `defer_with_reason`

Use when resolution requires a separate issue because it would affect protected
surfaces, parser behavior, runtime behavior, evidence-ledger semantics,
diagnostics behavior, fixture policy, generated-data policy, local artifact
policy, or broad scanner semantics.

Required follow-up:

- issue title or draft issue body;
- category and path family;
- reason not fixed in #262;
- protected surfaces involved;
- validation required before closure.

## Category-Specific Requirements

### `raw_player_log_content`

Required inspection:

- separate parser test literals, evidence-ledger examples, parser source
  comments, docs/problem-representation text, and actual raw log-like content;
- do not copy line text into durable artifacts;
- identify whether tests can use fragment builders or sanctioned fixture files
  instead of inline raw-looking markers;
- preserve parser behavior and parser regression coverage.

Preferred outcomes:

- classify parser tests as expected synthetic/sanitized only when that is
  accurate;
- route broad parser-test fixture refactors separately if needed;
- avoid editing parser source unless the matched text is clearly comment/doc
  wording or an obvious placeholder gap.

Stop and route back if:

- a finding appears to contain real local log content;
- a fix would alter parser interpretation, parser state final reconciliation,
  parser event classes, match/game identity, or deduplication.

### `runtime_status_payload`

Required inspection:

- separate runtime diagnostics constants, status API tests, sheet/export tests,
  evidence schema snapshots, Apps Script-adjacent tooling, and actual runtime
  artifacts;
- do not copy payload text into durable artifacts;
- distinguish field-name references from payload dumps.

Preferred outcomes:

- preserve diagnostic/status field coverage;
- classify field-name tests and schema snapshots separately from payload-like
  content;
- route runtime status schema or diagnostics behavior changes separately.

Stop and route back if:

- a finding appears to contain a real runtime status file or payload;
- a fix would change diagnostics behavior, status API shape, workbook-facing
  output, or Apps Script assumptions.

### `generated_data_dump`

Required inspection:

- separate card catalog tests, card catalog source constants, Scryfall/support
  tooling docs, generated-data policy text, and actual generated dumps;
- do not copy generated data contents into durable artifacts;
- preserve approved card-data source behavior and generated-data ignore policy.

Preferred outcomes:

- classify tests that intentionally exercise generated-data fields;
- route broad card-catalog fixture or generated-data policy cleanup separately;
- keep generated data files out of Git unless a separate contract explicitly
  authorizes a sanitized fixture or snapshot.

Stop and route back if:

- a finding appears to contain real generated data dump content;
- a fix would alter card catalog behavior, card identity behavior, analytics
  schema, generated-data refresh behavior, or approved data-source policy.

### Failed-Post Payload Category

Required inspection:

- separate failed-post field-name references from committed failed-post payload
  content;
- treat diagnostics and protected-surface tooling carefully;
- do not copy queue/payload text into durable artifacts.

Preferred outcomes:

- classify source/tooling references when they are field names or policy text;
- route any actual failed-post payload content to immediate fix/follow-up;
- preserve webhook retry/diagnostics behavior unless separately contracted.

Stop and route back if:

- a finding appears to contain a real failed-post payload or queued transport
  artifact;
- a fix would alter webhook payload shape, output transport, retry behavior, or
  diagnostics semantics.

### `private_local_path`

Required inspection:

- separate old reports/handoffs, examples, sanitizer tests, golden replay
  source code, parser diagnostics, and tooling;
- do not copy full paths, usernames, home directories, or machine-specific
  fragments into durable artifacts;
- verify whether the path is placeholder, redacted, historical report text,
  synthetic test input, or real local machine state.

Preferred outcomes:

- replace durable docs paths with symbolic placeholders where feasible;
- keep sanitizer tests proving redaction, but prefer fragment builders;
- route broad historical report cleanup separately if needed.

Stop and route back if:

- a finding appears to expose a real user path;
- a fix would alter sanitizer behavior, golden replay path handling,
  diagnostics behavior, or local app path semantics.

## Required Guarantees

- Selected findings are summarized by count/category/path family before any
  edits.
- No raw matched value is copied into docs, reports, issues, PR text, tests, or
  commit messages.
- Any file edit is tied to a selected finding family.
- Path-scoped scanner forbidden findings remain failing.
- All-repo scanner remains advisory unless a later contract authorizes
  escalation.
- Warning-only categories remain out of scope except as background context.
- Suppression, downgrade, or allowlist behavior requires explicit policy
  rationale and tests.
- Scanner redaction tests must remain intact.
- Parser, diagnostics, evidence-ledger, sanitizer, generated-data, and
  protected-surface tests must not be weakened to reduce scanner counts.
- Tests that need dangerous-looking values should use synthetic builders,
  approved sanitized fixtures, or explicit placeholders.
- No raw local/private/generated artifact is created, copied, sanitized,
  imported, committed, or moved.
- Private-local-v1 readiness language must distinguish:
  - selected #262 tranche status;
  - remaining all-repo scanner debt;
  - broader #252 readiness;
  - issue #260 lifecycle;
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

If a selected finding appears to be real private artifact content:

- do not print it;
- notify the user with only repo-relative path and scanner category;
- request explicit user direction if removal could require data handling or
  external cleanup;
- do not delete or mutate local/private artifacts without explicit approval.

If a fix would touch protected behavior:

- stop and route back to Codex A/B for a separate issue/contract.

## Side Effects

Codex B side effects:

- create this contract only.

Future Codex C side effects allowed by this contract:

- create implementation handoff;
- edit selected docs/test/tooling/source files only as needed to classify or
  safely resolve selected raw/private artifact findings;
- add or update focused scanner/sanitizer/protected-surface tests when behavior
  or fixtures change;
- create a review/contract-test report.

Forbidden side effects:

- read, print, copy, sanitize, import, move, delete, or commit private local
  artifacts;
- create generated SQLite files or app-data artifacts;
- alter parser behavior;
- alter parser state final reconciliation;
- alter parser event classes;
- alter match/game identity or deduplication;
- alter diagnostics/status API behavior;
- alter analytics schema, migrations, ingest, or views;
- alter workbook schema;
- alter webhook payload shape or output transport;
- alter Apps Script behavior;
- alter Google Sheets behavior;
- alter local app runtime behavior;
- alter production behavior;
- alter OpenAI/model-provider or AI/coaching behavior;
- alter credential or environment variable contracts;
- add CI gates;
- make all-repo scanner a failing gate;
- target `main`;
- close #252, #260, or #136.

## Dependency Order

Future implementation should proceed in this order:

1. Confirm branch and clean state.
2. Inspect issue #262, #260, #252, PR #261, PR #259, and tracker #136.
3. Re-run all-repo scanner and summarize selected categories only.
4. Re-run changed-file scanner against `origin/codex/analytics-foundation`.
5. Build a selected inventory with category, severity, path, line, and reason,
   but no raw excerpt or raw value.
6. Group findings by category and path family.
7. Classify path families using this contract vocabulary.
8. Identify small safe edits, if any.
9. Route broad parser-test, diagnostics, generated-data, failed-post, or
   historical-doc cleanup into follow-up issues when needed.
10. Run validation.
11. Produce implementation handoff.
12. Route to Codex E for independent review/contract testing.

## Compatibility

Preserve:

- #252 `.env*` ignore posture;
- #260 high-risk scanner triage package;
- path-scoped scanner strictness;
- all-repo scanner advisory mode and exit behavior;
- current scanner redaction guarantees;
- protected-surface gate behavior;
- local environment checker no-private-content-read behavior;
- parser/evidence/sanitizer regression coverage;
- generated-data ignore policy;
- parser, analytics, workbook, Apps Script, local app, production, and AI
  behavior.

## Unknowns

- Whether any selected finding represents real private artifact leakage is not
  known until Codex C inspects exact lines without copying values.
- Whether broad parser tests should be rewritten with fixture builders or kept
  as accepted synthetic test coverage is not known.
- Whether evidence-ledger source findings are comments, test data, or
  behavior-adjacent literals requires careful comparison.
- Whether generated-data scanner findings are true dumps, field-name
  references, or scanner false positives requires source-line inspection.
- Whether private path findings in old reports should be rewritten or accepted
  as historical artifacts requires a docs-governance judgment.
- Whether a machine-readable all-repo scanner baseline is needed remains
  deferred.

## Suspected Gaps

- Many parser tests probably use inline raw-looking snippets where synthetic
  builders or dedicated sanitized fixtures could reduce all-repo debt.
- Evidence-ledger and diagnostics modules may contain raw-looking examples or
  field-name constants that need better scanner-aware labeling.
- Some generated-data findings are likely card-catalog test/source terms rather
  than actual generated dumps, but the scanner cannot currently distinguish all
  cases.
- Historical reports and handoffs may contain private-looking path examples
  that should be normalized to symbolic placeholders before release-readiness
  claims.
- All-repo scanner has no stable baseline/allowlist policy; #262 should not
  invent one broadly.

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

If Codex C changes only docs and reports, focused path-scoped
protected-surface and secret/private-marker scans over touched paths are
sufficient in addition to `git diff --check` and agent docs check.

If Codex C changes scanner code or scanner tests:

```powershell
py -m pytest -q tests\test_check_secret_patterns.py
py -m pytest -q tests\test_check_secret_patterns.py tests\test_check_local_environment.py tests\test_check_protected_surfaces.py
py tools\check_secret_patterns.py --all
py tools\check_secret_patterns.py --base origin/codex/analytics-foundation
py -m ruff check tools tests
```

If Codex C touches parser, evidence, diagnostics, generated-data, sanitizer, or
runtime source/tests, run focused tests selected by `tools/select_validation.py`
or justify why none are needed.

Validation reports must summarize all-repo scanner output by count/category and
path family only. Do not paste every scanner line.

## Acceptance Criteria

- Contract artifact exists at
  `docs/contracts/private_local_v1_raw_private_artifact_scanner_triage.md`.
- Current selected raw/private artifact scanner counts are recorded without raw
  values.
- Triage vocabulary is defined.
- Category-specific requirements are defined for `raw_player_log_content`,
  `runtime_status_payload`, `generated_data_dump`, the failed-post payload
  category, and `private_local_path`.
- Warning-only categories are explicitly deferred.
- Safe inspection and redaction requirements are defined.
- Required guarantees, unknowns, suspected gaps, and protected surfaces are
  defined.
- Validation requirements are defined.
- Codex C handoff is provided.
- No code or behavior changes are made by Codex B.

Future #262 completion requires:

- selected raw/private artifact findings summarized and classified by family;
- each selected family marked expected synthetic/sanitized, expected policy,
  expected placeholder/example, scanner false positive, concrete fix required,
  or deferred with a follow-up route;
- path-scoped scanner strictness preserved;
- all-repo scanner debt not hidden;
- no raw private/sensitive values printed or committed.

## Next Workflow Action

Next recommended role: Codex C / Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison thread for issue #262.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/262

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/136

Source issues:
- https://github.com/Tahjali11/Mythic-Edge/issues/252
- https://github.com/Tahjali11/Mythic-Edge/issues/260

Source PRs:
- https://github.com/Tahjali11/Mythic-Edge/pull/259
- https://github.com/Tahjali11/Mythic-Edge/pull/261

Branch:
codex/analytics-foundation

Contract:
docs/contracts/private_local_v1_raw_private_artifact_scanner_triage.md

Goal:
Compare the current all-repo scanner findings against the #262 contract. Produce docs/implementation_handoffs/private_local_v1_raw_private_artifact_scanner_triage_comparison.md and implement only narrow fixes for raw/private artifact categories if they are safe and contract-aligned.

Before editing:
- confirm branch and git status;
- inspect issue #262, issue #260, issue #252, PR #261, PR #259, and tracker #136;
- rerun the scanner summary without raw values;
- state what raw/private artifact scanner triage is supposed to do, what the scanner is actually reporting, why the findings matter, and the exact minimal comparison/implementation plan.

In scope:
- selected categories only:
  raw_player_log_content, runtime_status_payload, generated_data_dump,
  failed-post payload category, private_local_path;
- classify selected finding families;
- identify concrete fix candidates;
- convert obvious test-only findings to safe synthetic builders only when low risk;
- preserve parser/test meaning and scanner strictness;
- add/update focused tests only when behavior or fixtures change;
- produce implementation handoff.

Do not:
- print or copy raw matched values, raw log-like lines, runtime payloads, failed-post payloads, generated data contents, private local paths, private JSONL payloads, generated SQLite contents, workbook exports, secrets, tokens, keys, endpoints, spreadsheet IDs, provider keys, or environment values;
- weaken scanner coverage;
- suppress findings without explicit policy rationale and tests;
- handle warning-only categories except as context;
- fix all all-repo scanner categories;
- make all-repo scanner a failing gate;
- add CI gates;
- change parser behavior, parser state final reconciliation, parser event classes, match/game identity, deduplication, analytics behavior, SQLite schema/migrations, local app runtime behavior, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets behavior, production behavior, OpenAI/model-provider behavior, AI/coaching behavior, credential policy, or environment variable contracts;
- target main;
- close #252, #260, or #136.

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
- selected raw/private scanner summary;
- classification matrix;
- files changed;
- validation run;
- remaining selected findings;
- protected-surface status;
- next recommended role: Codex E;
- pasteable Codex E prompt;
- workflow_handoff block.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/262"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/136"
  source_issues:
    - "https://github.com/Tahjali11/Mythic-Edge/issues/252"
    - "https://github.com/Tahjali11/Mythic-Edge/issues/260"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "GitHub issue #262 problem representation"
  target_artifact: "docs/implementation_handoffs/private_local_v1_raw_private_artifact_scanner_triage_comparison.md"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  validation:
    - "git diff --check"
    - "py tools/check_agent_docs.py"
    - "path-scoped protected-surface scan for docs/contracts/private_local_v1_raw_private_artifact_scanner_triage.md"
    - "path-scoped secret/private-marker scan for docs/contracts/private_local_v1_raw_private_artifact_scanner_triage.md"
  stop_conditions:
    - "Do not implement code in Codex B."
    - "Do not print or copy raw matched values or private artifacts."
    - "Do not weaken scanner coverage or suppress findings without explicit policy rationale and tests."
    - "Do not handle warning-only categories except as context."
    - "Do not fix all all-repo scanner categories under #262."
    - "Do not make all-repo scanner a failing gate or add CI gates."
    - "Do not change parser/runtime/analytics/local app/workbook/webhook/App Script/Sheets/OpenAI/AI/production behavior."
    - "Do not change credential policy or environment variable contracts."
    - "Do not target main, close #252, close #260, or close tracker #136."
```
