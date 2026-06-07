# Private Local V1 Artifact-Path And Ambiguous-Marker Warning Triage Contract

## Module

`private_local_v1_artifact_path_ambiguous_marker_warning_triage`

Plain English: this contract defines the next private-local-v1 all-repo
scanner-debt tranche after the high-risk and raw/private artifact tranches.
It covers warning-only scanner categories that create a large amount of
advisory noise:

- `artifact_path_reference`
- `ambiguous_private_marker`

This is a contract-writing artifact only. It does not implement scanner,
fixture, test, docs, parser, analytics, local app, workbook, webhook, Apps
Script, credential, or production behavior changes.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/264
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/136
- Source issues:
  - https://github.com/Tahjali11/Mythic-Edge/issues/252
  - https://github.com/Tahjali11/Mythic-Edge/issues/260
  - https://github.com/Tahjali11/Mythic-Edge/issues/262
- Source PRs:
  - https://github.com/Tahjali11/Mythic-Edge/pull/259
  - https://github.com/Tahjali11/Mythic-Edge/pull/261
  - https://github.com/Tahjali11/Mythic-Edge/pull/263
- Branch: `codex/analytics-foundation`
- Expected artifact:
  `docs/contracts/private_local_v1_artifact_path_ambiguous_marker_warning_triage.md`

## Source Artifacts

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/project_roadmap.md`
- issue #264
- tracker #136
- issues #252, #260, and #262
- PRs #259, #261, and #263
- `docs/contracts/private_local_v1_private_artifact_scanner_env_ignore_posture.md`
- `docs/contracts/private_local_v1_high_risk_scanner_findings_triage.md`
- `docs/implementation_handoffs/private_local_v1_high_risk_scanner_findings_triage_comparison.md`
- `docs/contract_test_reports/private_local_v1_high_risk_scanner_findings_triage.md`
- `docs/contracts/private_local_v1_raw_private_artifact_scanner_triage.md`
- `docs/implementation_handoffs/private_local_v1_raw_private_artifact_scanner_triage_comparison.md`
- `docs/contract_test_reports/private_local_v1_raw_private_artifact_scanner_triage.md`
- `docs/contracts/repo_wide_secret_private_marker_scanner.md`
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

- warning-only scanner debt is broad enough to hide future real private
  artifact risk if left unclassified;
- selected warnings appear across governance docs, handoffs, reports, tests,
  tooling, fixtures, and source;
- unsafe cleanup could erase useful scanner policy, weaken redaction tests, or
  rewrite historical workflow evidence;
- some ambiguous markers are near parser/evidence Player.log vocabulary and
  must not be "fixed" by changing parser behavior;
- full private-local-v1 private artifact readiness is not claimed.

## Owning Layer

Primary owner: Quality / Governance.

Supporting area: Generated / Local Artifacts.

## Internal Project Area

Quality / Governance.

## Truth Owner

The repo secret/private-marker scanner owns deterministic repository
content-safety classification and redacted scanner reporting.

The #264 triage report owns selected warning-family classification for
private-local-v1 release-readiness planning.

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
tracked repo files + warning-level scanner findings
  -> redacted warning summary
  -> category/family classification
  -> narrow docs/test/tool cleanup candidates, explicit deferrals, or follow-up issues
  -> implementation handoff and review report
```

Forbidden reverse flow:

- warning triage must not authorize committing raw logs, runtime payloads,
  failed-post payloads, generated data dumps, workbook exports, private local
  paths, secrets, credentials, or local-only artifacts;
- warning triage must not weaken scanner coverage merely to reduce counts;
- warning triage must not change parser, analytics, workbook, webhook, Apps
  Script, local app runtime, AI, model-provider, or production behavior.

## Files Owned By This Contract

This contract owns:

- `docs/contracts/private_local_v1_artifact_path_ambiguous_marker_warning_triage.md`

Expected future implementation/comparison artifact:

- `docs/implementation_handoffs/private_local_v1_artifact_path_ambiguous_marker_warning_triage_comparison.md`

Expected future contract-test/review artifact:

- `docs/contract_test_reports/private_local_v1_artifact_path_ambiguous_marker_warning_triage.md`

Future Codex C may touch only if the comparison proves a specific selected
warning family needs it:

- selected docs, handoffs, reports, tests, fixtures, source, example, or tool
  files;
- `tools/check_secret_patterns.py`;
- `tests/test_check_secret_patterns.py`;
- local artifact or scanner policy docs.

Codex C must route back to Codex B before changing scanner category semantics,
path-scoped scanner strictness, all-repo advisory behavior, fixture provenance
policy, parser behavior, runtime behavior, analytics behavior, workbook/webhook
or Apps Script behavior, local app runtime behavior, CI gates, production
behavior, credential policy, or environment variable contracts.

## Observed Current Behavior

### Source Issue State

- Issue #264 is open and owns the artifact-path and ambiguous-marker warning
  triage tranche.
- Issue #252 remains open because full private-local-v1 private artifact
  readiness is not claimed.
- Issue #260 remains open pending lifecycle reconciliation.
- Issue #262 remains open pending lifecycle reconciliation.
- PR #259, PR #261, and PR #263 have been merged into
  `codex/analytics-foundation`.
- Tracker #136 remains open.
- Path-scoped scanner safety remains strict.
- All-repo scanner remains advisory and non-clean.

### Refreshed All-Repo Scanner Summary

Observed on `codex/analytics-foundation` during this contract pass:

```text
mode: all-repo-advisory
result: failed
exit_code: 0
scanned_paths: 756
skipped_paths: 0
forbidden: 540
warnings: 901
```

Selected warning category counts:

| Category | Total | Forbidden | Warnings |
| --- | ---: | ---: | ---: |
| `artifact_path_reference` | 635 | 0 | 635 |
| `ambiguous_private_marker` | 80 | 0 | 80 |

Warning categories intentionally deferred from this issue:

| Category | Total | Forbidden | Warnings |
| --- | ---: | ---: | ---: |
| `sanitized_fixture_marker` | 174 | 0 | 174 |
| `placeholder_secret_reference` | 9 | 0 | 9 |
| `decode_replacement_used` | 3 | 0 | 3 |

### Selected Path-Family Shape

Selected findings by broad path family:

| Category | Path family | Count |
| --- | --- | ---: |
| `artifact_path_reference` | `docs/contracts/` | 221 |
| `artifact_path_reference` | `docs/implementation_handoffs/` | 182 |
| `artifact_path_reference` | `docs/contract_test_reports/` | 172 |
| `artifact_path_reference` | `tests/` | 42 |
| `artifact_path_reference` | `docs/` | 8 |
| `artifact_path_reference` | `tools/` | 5 |
| `artifact_path_reference` | `tests/fixtures/` | 4 |
| `artifact_path_reference` | `src/` | 1 |
| `ambiguous_private_marker` | `docs/contracts/` | 73 |
| `ambiguous_private_marker` | `docs/implementation_handoffs/` | 4 |
| `ambiguous_private_marker` | `tests/` | 2 |
| `ambiguous_private_marker` | `docs/contract_test_reports/` | 1 |

Highest-count selected paths observed without raw values or excerpts:

| Category | Count | Path |
| --- | ---: | --- |
| `artifact_path_reference` | 24 | `docs/contracts/player_log_evidence_ledger_runtime_status_exposure.md` |
| `artifact_path_reference` | 18 | `docs/contract_test_reports/player_log_evidence_ledger_schema_snapshot_builder.md` |
| `artifact_path_reference` | 9 | `docs/contract_test_reports/code_hardening_golden_fixture_policy.md` |
| `artifact_path_reference` | 8 | `docs/contract_test_reports/player_log_evidence_ledger_runtime_status_exposure.md` |
| `artifact_path_reference` | 8 | `docs/contracts/parser_diagnostics_mode.md` |
| `artifact_path_reference` | 8 | `tests/test_runtime_field_evidence.py` |
| `ambiguous_private_marker` | 10 | `docs/contracts/parser_gre_game_state.md` |
| `ambiguous_private_marker` | 9 | `docs/contracts/parser_gre_connect_resp.md` |
| `ambiguous_private_marker` | 7 | `docs/contracts/player_log_evidence_ledger_tier3_mulligans.md` |
| `ambiguous_private_marker` | 7 | `docs/contracts/player_log_evidence_ledger_tier3_play_draw.md` |
| `ambiguous_private_marker` | 6 | `docs/contracts/player_log_evidence_ledger.md` |
| `ambiguous_private_marker` | 5 | `docs/contracts/parser_event_lifecycle.md` |

This contract intentionally records category IDs, counts, and repo-relative
paths only. It does not record raw matched values, raw excerpts, raw log-like
lines, raw payload text, private paths, local user names, generated data
contents, workbook contents, endpoint values, credential values, or environment
values.

## Contract Decision

Issue #264 is a targeted warning-only scanner triage tranche.

Required scope:

- classify selected warning families in:
  - `artifact_path_reference`;
  - `ambiguous_private_marker`;
- preserve path-scoped scanner strictness;
- preserve all-repo scanner as advisory unless a later contract changes that;
- preserve redaction and no-content-leak behavior;
- separate expected policy/test/handoff text from concrete cleanup targets;
- route broad or protected-surface cleanup to follow-up issues;
- produce an implementation handoff and a review/contract-test report.

Not required:

- zero all-repo scanner findings;
- fixing all 540 forbidden findings and 901 warnings;
- handling `sanitized_fixture_marker`, `placeholder_secret_reference`, or
  `decode_replacement_used` except as background context;
- rewriting broad scanner policy;
- adding an allowlist/baseline system;
- making all-repo scanner a CI gate;
- closing #252, #260, #262, or tracker #136.

Private-local-v1 private artifact readiness may not be claimed from this
warning-only pass.

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
- policy docs and prior #252/#260/#262 reports;
- issue #264 problem representation;
- path-scoped scanner/protected-surface results.

Forbidden inputs:

- raw local artifact paths;
- local user names;
- raw log-like lines;
- raw runtime payloads;
- raw failed-post payloads;
- generated data dumps;
- private JSONL payloads;
- generated SQLite contents;
- raw workbook exports;
- secrets, credentials, endpoint URLs, tokens, keys, OAuth values, provider
  keys, spreadsheet IDs, or environment values.

## Outputs

Required Codex C output:

- files inspected;
- selected warning count by category and severity;
- selected warning count by path family;
- classification matrix by category/path family;
- docs/policy warning families;
- handoff/report warning families;
- test/fixture warning families;
- concrete cleanup candidates, if any;
- scanner false positives, if any;
- explicit deferrals and follow-up issue routes;
- exact files changed, if any;
- validation evidence;
- remaining selected warnings;
- protected-surface status;
- secret/private-marker status.

Forbidden output:

- raw local artifact paths;
- local user names;
- raw log-like lines;
- raw runtime payloads;
- raw failed-post payloads;
- generated data contents;
- private payload excerpts;
- endpoint values;
- workbook IDs;
- secrets, tokens, keys, credentials, or environment values.

## Triage Classification Vocabulary

Each selected warning family must be assigned exactly one primary
classification.

### `expected_policy_or_contract_text`

Use when docs or contracts intentionally discuss protected surfaces, ignored
artifact families, parser evidence boundaries, runtime status boundaries,
Player.log provenance, or scanner category behavior.

Allowed only when:

- no raw private content is present;
- wording is necessary for policy clarity;
- scanner behavior remains strict for non-policy paths.

### `expected_handoff_or_review_text`

Use when implementation handoffs or contract-test reports preserve prior
workflow evidence, validation commands, scanner summaries, or issue lifecycle
context.

Allowed only when:

- the text is repo-relative or symbolic;
- no raw private value is present;
- the report is useful as durable workflow history.

Preferred outcome:

- keep useful historical evidence visible;
- route bulk normalization to a focused docs-cleanup issue if release-readiness
  requires count reduction.

### `expected_synthetic_or_sanitized_fixture`

Use when tests or fixtures intentionally include synthetic or sanitized marker
shapes to prove parser, scanner, sanitizer, evidence-ledger, diagnostics, or
path-redaction behavior.

Required safeguards:

- no real private value is present;
- fixture/test purpose is explicit;
- synthetic data is built or labeled clearly enough for review;
- scanner redaction behavior remains tested;
- future fixture changes follow golden fixture policy when applicable.

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

### `concrete_cleanup_required`

Use when a warning is safe in severity but should still be cleaned up because
it exposes unnecessary local-path shape, confusing historical wording,
scanner-hostile examples, or unclear placeholder context.

Required outcome:

- rewrite to symbolic placeholder text;
- replace with clearer policy wording;
- convert to fragment-built synthetic test input;
- or route to a focused follow-up if cleanup is broad or behavior-adjacent.

### `defer_with_reason`

Use when resolution requires a separate issue because it would affect protected
surfaces, parser behavior, runtime behavior, evidence-ledger semantics,
diagnostics behavior, fixture policy, generated-data policy, local artifact
policy, historical workflow evidence, or broad scanner semantics.

Required follow-up:

- issue title or draft issue body;
- category and path family;
- reason not fixed in #264;
- protected surfaces involved;
- validation required before closure.

## Category-Specific Requirements

### `artifact_path_reference`

Meaning:

This warning identifies references to ignored or local artifact paths in docs,
tests, policies, comments, handoffs, or reports. These references may be
expected, but the warning volume makes it hard to see whether any path wording
should be normalized before private-local-v1 readiness.

Required inspection:

- separate governance/policy docs, historical handoffs/reports, tests,
  fixtures, tooling, and source references;
- do not copy matched path text into durable artifacts;
- determine whether the reference is symbolic, repo-relative, placeholder,
  test-owned, historical workflow evidence, or machine-local/private;
- identify whether old reports/handoffs should be normalized now or deferred.

Preferred outcomes:

- classify durable policy text as expected when it intentionally names local
  artifact boundaries;
- classify tests as synthetic/sanitized only when the test proves redaction or
  path handling;
- mark historical docs cleanup as deferred unless the warning blocks a current
  release-readiness claim;
- use symbolic placeholders for any new docs created under #264.

Stop and route back if:

- a warning appears to expose a real machine-local path or user name;
- cleanup would alter sanitizer behavior, local app path semantics, runner
  behavior, diagnostics behavior, or protected-surface policy.

### `ambiguous_private_marker`

Meaning:

This warning identifies a token, marker, URL-like string, path-like string, or
log-like marker that is relevant to private artifact safety but is not clearly
live/private from scanner context alone.

Required inspection:

- separate parser/player-log vocabulary, policy discussion, historical reports,
  tests, and scanner-source examples;
- do not copy matched marker text into durable artifacts;
- decide whether the warning is expected parser/policy vocabulary, expected
  test data, a scanner false positive, a concrete cleanup candidate, or a
  deferred parser/evidence cleanup;
- preserve parser and evidence-ledger meaning.

Preferred outcomes:

- classify parser contract vocabulary as expected policy text when it is
  describing evidence boundaries;
- classify parser/source constants as false positives only when no private
  artifact content is present;
- route parser/evidence vocabulary cleanup separately if reducing all-repo
  warnings would require changing source or contract wording broadly.

Stop and route back if:

- a warning appears to contain copied raw Player.log content;
- a fix would change parser interpretation, parser state final reconciliation,
  parser event classes, match/game identity, deduplication, evidence-ledger
  semantics, or fixture provenance rules.

## Required Guarantees

- Selected warnings are summarized by count/category/path family before any
  edits.
- No raw matched value is copied into docs, reports, issues, PR text, tests, or
  commit messages.
- Any file edit is tied to a selected warning family.
- Path-scoped scanner forbidden findings remain failing.
- All-repo scanner remains advisory unless a later contract authorizes
  escalation.
- Warning-only findings are not silently treated as proof of safety.
- Suppression, downgrade, or allowlist behavior requires explicit policy
  rationale and tests.
- Scanner redaction tests must remain intact.
- Parser, diagnostics, evidence-ledger, sanitizer, generated-data, and
  protected-surface tests must not be weakened to reduce warning counts.
- Tests that need path-like or marker-like values should use synthetic
  builders, approved sanitized fixtures, or explicit placeholders.
- No raw local/private/generated artifact is created, copied, sanitized,
  imported, committed, or moved.
- Private-local-v1 readiness language must distinguish:
  - selected #264 warning-triage status;
  - remaining all-repo scanner debt;
  - broader #252 readiness;
  - issue #260 and #262 lifecycle;
  - tracker #136 lifecycle.

## Error Behavior

If a selected warning cannot be classified safely:

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

If a selected warning appears to be real private artifact content:

- do not print it;
- notify the user with only repo-relative path and scanner category;
- request explicit user direction if removal could require data handling or
  external cleanup;
- do not delete or mutate local/private artifacts without explicit approval.

If cleanup would touch protected behavior:

- stop and route back to Codex A/B for a separate issue/contract.

## Side Effects

Codex B side effects:

- create this contract only.

Future Codex C side effects allowed by this contract:

- create implementation handoff;
- edit selected docs/test/tooling/source files only as needed to classify or
  safely resolve selected warning findings;
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
- alter evidence-ledger semantics;
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
- close #252, #260, #262, or #136.

## Dependency Order

Future implementation should proceed in this order:

1. Confirm branch and clean state.
2. Inspect issue #264, #262, #260, #252, PR #263, PR #261, PR #259, and
   tracker #136.
3. Re-run all-repo scanner and summarize selected warning categories only.
4. Re-run changed-file scanner against `origin/codex/analytics-foundation`.
5. Build a selected warning inventory with category, severity, path, line, and
   reason, but no raw excerpt or raw value.
6. Group warnings by category and path family.
7. Classify path families using this contract vocabulary.
8. Identify small safe docs/test/tooling edits, if any.
9. Route broad historical-doc cleanup, parser/evidence vocabulary cleanup,
   fixture cleanup, or scanner semantic changes into follow-up issues.
10. Run validation.
11. Produce implementation handoff.
12. Route to Codex E for independent review/contract testing.

## Compatibility

Preserve:

- #252 `.env*` ignore posture;
- #260 high-risk scanner triage package;
- #262 raw/private artifact scanner triage package;
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

- Whether any selected warning is a real private artifact exposure is unknown
  until Codex C inspects exact lines without copying values.
- Whether historical handoffs/reports should be normalized before
  private-local-v1 readiness is a governance decision, not a scanner decision.
- Whether parser/evidence contracts should keep all marker vocabulary as policy
  text or migrate some examples to fixture references requires follow-up
  judgment.
- Whether all-repo scanner warning counts should eventually have a baseline,
  allowlist, or release-readiness threshold remains deferred.
- Whether the lone source `artifact_path_reference` warning needs source-code
  cleanup or is an expected path-handling reference is unknown.

## Suspected Gaps

- Historical reports and handoffs probably preserve useful context but may
  also contain old local-path examples that should be normalized before a
  polished release-readiness claim.
- Parser and Player.log evidence contracts likely use log-marker vocabulary
  that the scanner cannot distinguish from ambiguous private markers without
  policy context.
- Some tests may use inline path-like or marker-like strings where fragment
  builders would reduce advisory noise while preserving test meaning.
- The all-repo scanner has no stable warning baseline or machine-readable
  allowlist policy; #264 should not invent one broadly.
- Warning-only scanner debt may remain large even after this classification
  pass because sanitized fixtures and placeholder warnings are deferred.

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
  `docs/contracts/private_local_v1_artifact_path_ambiguous_marker_warning_triage.md`.
- Current selected warning scanner counts are recorded without raw values.
- Triage vocabulary is defined.
- Category-specific requirements are defined for `artifact_path_reference` and
  `ambiguous_private_marker`.
- Deferred warning categories are explicitly out of scope.
- Safe inspection and redaction requirements are defined.
- Required guarantees, unknowns, suspected gaps, and protected surfaces are
  defined.
- Validation requirements are defined.
- Codex C handoff is provided.
- No code or behavior changes are made by Codex B.

Future #264 completion requires:

- selected warning findings summarized and classified by family;
- each selected family marked expected policy/contract text, expected
  handoff/review text, expected synthetic/sanitized fixture, expected
  placeholder/example, scanner false positive, concrete cleanup required, or
  deferred with a follow-up route;
- path-scoped scanner strictness preserved;
- all-repo scanner debt not hidden;
- no raw private/sensitive values printed or committed.

## Next Workflow Action

Next recommended role: Codex C / Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison thread for issue #264.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/264

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/136

Source issues:
- https://github.com/Tahjali11/Mythic-Edge/issues/252
- https://github.com/Tahjali11/Mythic-Edge/issues/260
- https://github.com/Tahjali11/Mythic-Edge/issues/262

Source PRs:
- https://github.com/Tahjali11/Mythic-Edge/pull/259
- https://github.com/Tahjali11/Mythic-Edge/pull/261
- https://github.com/Tahjali11/Mythic-Edge/pull/263

Branch:
codex/analytics-foundation

Contract:
docs/contracts/private_local_v1_artifact_path_ambiguous_marker_warning_triage.md

Goal:
Compare the current all-repo scanner warnings against the #264 contract. Produce docs/implementation_handoffs/private_local_v1_artifact_path_ambiguous_marker_warning_triage_comparison.md and implement only narrow fixes for artifact-path or ambiguous-marker warning families if they are safe and contract-aligned.

Before editing:
- confirm branch and git status;
- inspect issue #264, issue #262, issue #260, issue #252, PR #263, PR #261, PR #259, and tracker #136;
- rerun the scanner summary without raw values;
- state what warning triage is supposed to do, what the scanner is actually reporting, why the warning volume matters, and the exact minimal comparison/implementation plan.

In scope:
- selected warning categories only:
  artifact_path_reference and ambiguous_private_marker;
- classify selected warning families;
- identify concrete cleanup candidates;
- convert obvious docs/test examples to symbolic placeholders or synthetic builders only when low risk;
- preserve parser/test meaning and scanner strictness;
- add/update focused tests only when behavior or fixtures change;
- produce implementation handoff.

Do not:
- print or copy raw matched values, raw local paths, local user names, raw log-like lines, runtime payloads, failed-post payloads, generated data contents, private JSONL payloads, generated SQLite contents, workbook exports, secrets, tokens, keys, endpoints, spreadsheet IDs, provider keys, environment values, or local-only artifacts;
- weaken scanner coverage;
- suppress findings without explicit policy rationale and tests;
- handle sanitized_fixture_marker, placeholder_secret_reference, or decode_replacement_used except as context;
- fix all all-repo scanner categories;
- make all-repo scanner a failing gate;
- add CI gates;
- change parser behavior, parser state final reconciliation, parser event classes, match/game identity, deduplication, evidence-ledger semantics, analytics behavior, SQLite schema/migrations, local app runtime behavior, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets behavior, production behavior, OpenAI/model-provider behavior, AI/coaching behavior, credential policy, or environment variable contracts;
- target main;
- close #252, #260, #262, or #136.

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
- selected warning scanner summary;
- classification matrix;
- files changed;
- validation run;
- remaining selected warnings;
- protected-surface status;
- next recommended role: Codex E;
- pasteable Codex E prompt;
- workflow_handoff block.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/264"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/136"
  source_issues:
    - "https://github.com/Tahjali11/Mythic-Edge/issues/252"
    - "https://github.com/Tahjali11/Mythic-Edge/issues/260"
    - "https://github.com/Tahjali11/Mythic-Edge/issues/262"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "GitHub issue #264 problem representation"
  target_artifact: "docs/implementation_handoffs/private_local_v1_artifact_path_ambiguous_marker_warning_triage_comparison.md"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  validation:
    - "git diff --check"
    - "py tools/check_agent_docs.py"
    - "path-scoped protected-surface scan for docs/contracts/private_local_v1_artifact_path_ambiguous_marker_warning_triage.md"
    - "path-scoped secret/private-marker scan for docs/contracts/private_local_v1_artifact_path_ambiguous_marker_warning_triage.md"
  stop_conditions:
    - "Do not implement code in Codex B."
    - "Do not print or copy raw matched values or private artifacts."
    - "Do not weaken scanner coverage or suppress findings without explicit policy rationale and tests."
    - "Do not handle deferred warning categories except as context."
    - "Do not fix all all-repo scanner categories under #264."
    - "Do not make all-repo scanner a failing gate or add CI gates."
    - "Do not change parser/runtime/analytics/local app/workbook/webhook/App Script/Sheets/OpenAI/AI/production behavior."
    - "Do not change credential policy or environment variable contracts."
    - "Do not target main, close #252, close #260, close #262, or close tracker #136."
```
