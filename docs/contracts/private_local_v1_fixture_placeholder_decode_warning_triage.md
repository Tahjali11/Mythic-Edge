# Private Local V1 Fixture, Placeholder, And Decode Warning Triage Contract

## Module

`private_local_v1_fixture_placeholder_decode_warning_triage`

Plain English: this contract defines the next private-local-v1 scanner-debt
tranche after the high-risk, raw/private artifact, artifact-path, and
ambiguous-marker triage work. It covers the remaining focused warning-only
categories:

- `sanitized_fixture_marker`
- `placeholder_secret_reference`
- `decode_replacement_used`

This is a contract-writing artifact only. It does not implement scanner,
fixture, test, docs, parser, analytics, local app, workbook, webhook, Apps
Script, credential, or production behavior changes.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/266
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/136
- Source issues:
  - https://github.com/Tahjali11/Mythic-Edge/issues/252
  - https://github.com/Tahjali11/Mythic-Edge/issues/260
  - https://github.com/Tahjali11/Mythic-Edge/issues/262
  - https://github.com/Tahjali11/Mythic-Edge/issues/264
- Source PRs:
  - https://github.com/Tahjali11/Mythic-Edge/pull/259
  - https://github.com/Tahjali11/Mythic-Edge/pull/261
  - https://github.com/Tahjali11/Mythic-Edge/pull/263
  - https://github.com/Tahjali11/Mythic-Edge/pull/265
- Branch: `codex/analytics-foundation`
- Expected artifact:
  `docs/contracts/private_local_v1_fixture_placeholder_decode_warning_triage.md`

## Source Artifacts

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- issue #266
- tracker #136
- issues #252, #260, #262, and #264
- PRs #259, #261, #263, and #265
- `docs/contracts/private_local_v1_private_artifact_scanner_env_ignore_posture.md`
- `docs/contracts/private_local_v1_high_risk_scanner_findings_triage.md`
- `docs/contracts/private_local_v1_raw_private_artifact_scanner_triage.md`
- `docs/contracts/private_local_v1_artifact_path_ambiguous_marker_warning_triage.md`
- associated implementation handoffs and contract-test reports for #260,
  #262, and #264
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

Medium.

Reasons:

- selected categories are warning-only in current scanner behavior;
- fixture and placeholder warnings can be expected and useful when documented;
- decode warnings may signal readability or scanner-confidence debt, but they
  are not direct evidence of leaked private content;
- unsafe cleanup could still weaken fixture provenance, scanner redaction
  tests, or historical docs;
- full private-local-v1 private artifact readiness is not claimed.

## Owning Layer

Primary owner: Quality / Governance.

Supporting area: Generated / Local Artifacts.

## Internal Project Area

Quality / Governance.

## Truth Owner

The repo secret/private-marker scanner owns deterministic repository
content-safety classification and redacted scanner reporting.

The #266 triage report owns selected warning-family classification for
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
  -> redacted fixture/placeholder/decode summary
  -> category/family classification
  -> narrow docs/test/fixture cleanup candidates, explicit deferrals, or follow-up issues
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

- `docs/contracts/private_local_v1_fixture_placeholder_decode_warning_triage.md`

Expected future implementation/comparison artifact:

- `docs/implementation_handoffs/private_local_v1_fixture_placeholder_decode_warning_triage_comparison.md`

Expected future contract-test/review artifact:

- `docs/contract_test_reports/private_local_v1_fixture_placeholder_decode_warning_triage.md`

Future Codex C may touch only if the comparison proves a specific selected
warning family needs it:

- selected fixture metadata, tests, docs, source comments, or tooling docs;
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

- Issue #266 is open and owns the sanitized-fixture, placeholder, and decode
  warning triage tranche.
- Issue #252 remains open because full private-local-v1 private artifact
  readiness is not claimed.
- Issues #260, #262, and #264 remain open pending lifecycle reconciliation.
- PRs #259, #261, #263, and #265 have been merged into
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
scanned_paths: 759
skipped_paths: 0
forbidden: 540
warnings: 901
```

Selected warning category counts:

| Category | Total | Forbidden | Warnings |
| --- | ---: | ---: | ---: |
| `sanitized_fixture_marker` | 174 | 0 | 174 |
| `placeholder_secret_reference` | 9 | 0 | 9 |
| `decode_replacement_used` | 3 | 0 | 3 |

Selected findings by broad path family:

| Category | Path family | Count |
| --- | --- | ---: |
| `sanitized_fixture_marker` | `tests/fixtures/` | 174 |
| `placeholder_secret_reference` | `tests/` | 7 |
| `placeholder_secret_reference` | `docs/contracts/` | 1 |
| `placeholder_secret_reference` | `src/` | 1 |
| `decode_replacement_used` | `docs/` | 3 |

Highest-count selected paths observed without raw values or excerpts:

| Category | Count | Path |
| --- | ---: | --- |
| `sanitized_fixture_marker` | 140 | `tests/fixtures/evidence_schema_snapshots/player_log_evidence_ledger_schema_snapshot.v1.json` |
| `sanitized_fixture_marker` | 12 | `tests/fixtures/parser_regression_bo3_slice.log` |
| `sanitized_fixture_marker` | 7 | `tests/fixtures/flush_timing_corpus_slice.log` |
| `sanitized_fixture_marker` | 7 | `tests/fixtures/parser_regression_match_slice.log` |
| `sanitized_fixture_marker` | 5 | `tests/fixtures/draft_parser_family_slice.log` |
| `sanitized_fixture_marker` | 3 | `tests/fixtures/router_smoke_slice.log` |
| `placeholder_secret_reference` | 3 | `tests/test_check_secret_patterns.py` |
| `placeholder_secret_reference` | 2 | `tests/test_app_outputs.py` |
| `decode_replacement_used` | 1 | `docs/Mythic_Edge_Deep_Dive_Guide.pdf` |
| `decode_replacement_used` | 1 | `docs/Mythic_Edge_Learning_Guide.pdf` |
| `decode_replacement_used` | 1 | `docs/Tailer_py_Deep_Dive.pdf` |

This contract intentionally records category IDs, counts, and repo-relative
paths only. It does not record raw matched values, raw excerpts, raw log-like
lines, raw payload text, private paths, local user names, generated data
contents, workbook contents, endpoint values, credential values, or environment
values.

## Contract Decision

Issue #266 is a targeted warning-only scanner triage tranche.

Required scope:

- classify selected warning families in:
  - `sanitized_fixture_marker`;
  - `placeholder_secret_reference`;
  - `decode_replacement_used`;
- preserve path-scoped scanner strictness;
- preserve all-repo scanner as advisory unless a later contract changes that;
- preserve redaction and no-content-leak behavior;
- distinguish expected sanitized evidence from fixture hygiene debt;
- distinguish clear placeholders from confusing placeholder-secret drift;
- distinguish harmless decode warnings from docs readability/scanner-confidence
  cleanup candidates;
- route broad or protected-surface cleanup to follow-up issues;
- produce an implementation handoff and a review/contract-test report.

Not required:

- zero all-repo scanner findings;
- fixing all 540 forbidden findings and 901 warnings;
- handling high-risk, raw/private artifact, artifact-path, or ambiguous-marker
  categories except as background context;
- rewriting broad scanner policy;
- adding an allowlist/baseline system;
- making all-repo scanner a CI gate;
- closing #252, #260, #262, #264, or tracker #136.

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
- fixture metadata and fixture paths, without raw private payload dumps;
- issue #266 problem representation;
- path-scoped scanner/protected-surface results.

Forbidden inputs:

- raw local artifact paths;
- local user names;
- raw log-like lines copied from private Player.log files;
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
- expected sanitized fixture families;
- placeholder/reference warning families;
- decode warning families;
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

### `expected_sanitized_fixture_evidence`

Use when the warning appears inside an approved or clearly documented sanitized
fixture that intentionally preserves parser-observable marker shape without
private content.

Required safeguards:

- fixture is under an approved fixture path;
- no real private value is present;
- fixture purpose is test/provenance evidence;
- scanner redaction and parser regression value are preserved;
- fixture policy remains visible.

### `fixture_hygiene_cleanup_required`

Use when a sanitized fixture is likely safe but has unclear provenance,
overly broad marker repetition, missing metadata, unclear labels, or avoidable
inline marker noise.

Required outcome:

- add or improve fixture metadata;
- route to a focused fixture cleanup issue;
- or rewrite with a synthetic fixture builder only when parser test meaning is
  preserved.

### `expected_placeholder_or_example`

Use when docs, tests, or source intentionally use explicit placeholder,
redacted, fake, sample, or configured values.

Required safeguards:

- placeholder context must be explicit near the value;
- value must not look live enough to confuse reviewers;
- test or docs purpose must remain clear;
- example code must not encourage committing local/generated/private state.

### `placeholder_cleanup_required`

Use when a placeholder warning is not secret leakage but should be rewritten
because the placeholder is unclear, too live-looking, source-adjacent, or
likely to confuse a future reviewer.

Required outcome:

- rewrite to symbolic placeholder text;
- split synthetic test values into builders;
- or route to a focused follow-up if cleanup would touch behavior-adjacent
  code.

### `decode_readability_warning`

Use when a file required replacement decoding during scanning, but the warning
is most likely a binary/PDF or encoded documentation artifact rather than
private content.

Required safeguards:

- do not paste decoded replacement output;
- do not infer private content from unreadable bytes;
- record repo-relative path and category only;
- route any repair through docs/readability or generated-doc policy.

### `scanner_false_positive`

Use only when the scanner category is technically matched but the text or file
shape is safe and rewriting would reduce clarity or scanner value.

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
policy, historical workflow evidence, binary/docs generation policy, or broad
scanner semantics.

Required follow-up:

- issue title or draft issue body;
- category and path family;
- reason not fixed in #266;
- protected surfaces involved;
- validation required before closure.

## Category-Specific Requirements

### `sanitized_fixture_marker`

Meaning:

This warning identifies Player.log-like marker shapes inside files the scanner
believes are sanitized fixtures. The warning is valuable: it tells reviewers
that the fixture preserves parser-relevant shape while still requiring
sanitization/provenance awareness.

Required inspection:

- verify each path family is under an approved fixture location;
- identify whether fixture purpose is parser regression, schema snapshot,
  flush timing, draft parser family, or router smoke coverage;
- do not copy fixture payload text into durable artifacts;
- decide whether the high count is expected evidence or fixture hygiene debt.

Preferred outcomes:

- classify clearly documented fixtures as expected sanitized fixture evidence;
- route metadata/provenance gaps through a fixture cleanup issue;
- preserve parser and evidence regression value;
- avoid rewriting fixture payloads under #266 unless the cleanup is obviously
  docs/metadata-only and test-safe.

Stop and route back if:

- a fixture appears to contain real private log content;
- a fix would alter parser interpretation, parser state final reconciliation,
  parser event classes, match/game identity, deduplication, or fixture oracle
  semantics.

### `placeholder_secret_reference`

Meaning:

This warning identifies placeholder or redacted secret-like text. It is
usually allowed, but it still needs classification because unclear placeholders
can train future contributors toward unsafe examples.

Required inspection:

- separate scanner tests, app output tests, drift/golden replay tests, contract
  policy text, and source redaction vocabulary;
- do not copy placeholder values into durable artifacts when they are
  secret-shaped;
- determine whether the placeholder is clear, test-owned, policy-owned,
  source-owned, or confusing enough to rewrite.

Preferred outcomes:

- keep scanner tests that prove placeholder handling and redaction;
- classify explicit docs/policy placeholders as expected;
- route source-adjacent placeholder rewrites separately if behavior semantics
  could change;
- prefer symbolic placeholder wording in any new docs created under #266.

Stop and route back if:

- a placeholder appears to be copied from a real secret, endpoint, environment
  value, workbook ID, or credential;
- a fix would alter credential policy, environment variable contracts,
  sanitizer behavior, parser outputs, or app output shape.

### `decode_replacement_used`

Meaning:

This warning identifies files that could not be decoded cleanly as UTF-8 and
were scanned with replacement characters. In the current #266 evidence, these
are documentation PDF files.

Required inspection:

- record only repo-relative file paths and category counts;
- do not paste decoded output or replacement-text excerpts;
- decide whether the warning is acceptable binary/documentation behavior,
  docs readability debt, or scanner file-type handling debt;
- do not regenerate, rewrite, or delete PDFs in Codex B.

Preferred outcomes:

- classify PDF decode warnings as decode readability/scanner-confidence
  warnings unless evidence suggests private content;
- route generated-document repair or source-doc regeneration separately;
- preserve scanner behavior that reports replacement decoding.

Stop and route back if:

- a decoded file appears to contain private data;
- cleanup would require deleting, regenerating, or replacing documentation
  artifacts without a docs-generation contract;
- scanner behavior would need a file-type skip policy change.

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
- Sanitized fixtures must preserve parser-regression value unless a fixture
  cleanup contract explicitly authorizes a change.
- PDFs or other non-text docs must not be decoded, pasted, regenerated, or
  deleted merely to reduce warning counts.
- No raw local/private/generated artifact is created, copied, sanitized,
  imported, committed, or moved.
- Private-local-v1 readiness language must distinguish:
  - selected #266 warning-triage status;
  - remaining all-repo scanner debt;
  - broader #252 readiness;
  - issue #260, #262, and #264 lifecycle;
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
- edit selected docs/test/fixture metadata/source comment files only as needed
  to classify or safely resolve selected warning findings;
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
- close #252, #260, #262, #264, or #136.

## Dependency Order

Future implementation should proceed in this order:

1. Confirm branch and clean state.
2. Inspect issue #266, #264, #262, #260, #252, PR #265, PR #263, PR #261,
   PR #259, and tracker #136.
3. Re-run all-repo scanner and summarize selected warning categories only.
4. Re-run changed-file scanner against `origin/codex/analytics-foundation`.
5. Build a selected warning inventory with category, severity, path, line, and
   reason, but no raw excerpt or raw value.
6. Group warnings by category and path family.
7. Classify path families using this contract vocabulary.
8. Identify small safe docs/test/fixture metadata edits, if any.
9. Route broad fixture cleanup, placeholder cleanup, PDF/docs regeneration, or
   scanner semantic changes into follow-up issues.
10. Run validation.
11. Produce implementation handoff.
12. Route to Codex E for independent review/contract testing.

## Compatibility

Preserve:

- #252 `.env*` ignore posture;
- #260 high-risk scanner triage package;
- #262 raw/private artifact scanner triage package;
- #264 artifact-path and ambiguous-marker warning triage package;
- path-scoped scanner strictness;
- all-repo scanner advisory mode and exit behavior;
- current scanner redaction guarantees;
- protected-surface gate behavior;
- local environment checker no-private-content-read behavior;
- parser/evidence/sanitizer regression coverage;
- fixture and golden evidence policy;
- generated-data ignore policy;
- parser, analytics, workbook, Apps Script, local app, production, and AI
  behavior.

## Unknowns

- Whether any selected sanitized fixture lacks sufficient provenance metadata
  is unknown until Codex C inspects the fixture family without copying payloads.
- Whether the source `placeholder_secret_reference` warning is pure redaction
  vocabulary or needs source-comment cleanup is unknown.
- Whether the PDF decode warnings should be accepted, regenerated, or routed
  into docs maintenance is unknown.
- Whether all-repo scanner warning counts should eventually have a baseline,
  allowlist, or release-readiness threshold remains deferred.
- Whether this tranche is sufficient to close #252 is unknown and must not be
  claimed by Codex B.

## Suspected Gaps

- The large schema snapshot fixture warning count may be expected evidence but
  could need clearer fixture provenance if future release readiness requires
  lower ambiguity.
- Some placeholder tests may be intentionally proving scanner/redaction logic
  but could use clearer builders or labels.
- PDF decode warnings may be harmless binary/doc behavior, but the scanner has
  no explicit PDF skip/readability policy beyond reporting replacement decode.
- The all-repo scanner has no stable warning baseline or machine-readable
  allowlist policy; #266 should not invent one broadly.

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

If Codex C touches fixtures, parser, evidence, diagnostics, generated-data,
sanitizer, or runtime source/tests, run focused tests selected by
`tools/select_validation.py` or justify why none are needed.

If Codex C touches PDF documentation or generated docs, route to a docs/PDF
contract or run a visual/readability validation appropriate for that artifact.

Validation reports must summarize all-repo scanner output by count/category and
path family only. Do not paste every scanner line.

## Acceptance Criteria

- Contract artifact exists at
  `docs/contracts/private_local_v1_fixture_placeholder_decode_warning_triage.md`.
- Current selected warning scanner counts are recorded without raw values.
- Triage vocabulary is defined.
- Category-specific requirements are defined for `sanitized_fixture_marker`,
  `placeholder_secret_reference`, and `decode_replacement_used`.
- Safe inspection and redaction requirements are defined.
- Required guarantees, unknowns, suspected gaps, and protected surfaces are
  defined.
- Validation requirements are defined.
- Codex C handoff is provided.
- No code or behavior changes are made by Codex B.

Future #266 completion requires:

- selected warning findings summarized and classified by family;
- each selected family marked expected sanitized fixture evidence, fixture
  hygiene cleanup required, expected placeholder/example, placeholder cleanup
  required, decode readability warning, scanner false positive, or deferred
  with a follow-up route;
- path-scoped scanner strictness preserved;
- all-repo scanner debt not hidden;
- no raw private/sensitive values printed or committed.

## Next Workflow Action

Next recommended role: Codex C / Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison thread for issue #266.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/266

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/136

Source issues:
- https://github.com/Tahjali11/Mythic-Edge/issues/252
- https://github.com/Tahjali11/Mythic-Edge/issues/260
- https://github.com/Tahjali11/Mythic-Edge/issues/262
- https://github.com/Tahjali11/Mythic-Edge/issues/264

Source PRs:
- https://github.com/Tahjali11/Mythic-Edge/pull/259
- https://github.com/Tahjali11/Mythic-Edge/pull/261
- https://github.com/Tahjali11/Mythic-Edge/pull/263
- https://github.com/Tahjali11/Mythic-Edge/pull/265

Branch:
codex/analytics-foundation

Contract:
docs/contracts/private_local_v1_fixture_placeholder_decode_warning_triage.md

Goal:
Compare the current all-repo scanner warnings against the #266 contract. Produce docs/implementation_handoffs/private_local_v1_fixture_placeholder_decode_warning_triage_comparison.md and implement only narrow fixes for sanitized-fixture, placeholder, or decode warning families if they are safe and contract-aligned.

Before editing:
- confirm branch and git status;
- inspect issue #266, #264, #262, #260, #252, PR #265, PR #263, PR #261, PR #259, and tracker #136;
- rerun the scanner summary without raw values;
- state what fixture/placeholder/decode warning triage is supposed to do, what the scanner is actually reporting, why the warning families matter, and the exact minimal comparison/implementation plan.

In scope:
- selected warning categories only:
  sanitized_fixture_marker, placeholder_secret_reference, decode_replacement_used;
- classify selected warning families;
- identify concrete cleanup candidates;
- improve docs/test/fixture metadata only when low risk and contract-aligned;
- preserve parser/test meaning and scanner strictness;
- add/update focused tests only when behavior or fixtures change;
- produce implementation handoff.

Do not:
- print or copy raw matched values, raw local paths, local user names, raw log-like lines, runtime payloads, failed-post payloads, generated data contents, private JSONL payloads, generated SQLite contents, workbook exports, secrets, tokens, keys, endpoints, spreadsheet IDs, provider keys, environment values, or local-only artifacts;
- weaken scanner coverage;
- suppress findings without explicit policy rationale and tests;
- fix all all-repo scanner categories;
- make all-repo scanner a failing gate;
- add CI gates;
- change parser behavior, parser state final reconciliation, parser event classes, match/game identity, deduplication, evidence-ledger semantics, analytics behavior, SQLite schema/migrations, local app runtime behavior, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets behavior, production behavior, OpenAI/model-provider behavior, AI/coaching behavior, credential policy, or environment variable contracts;
- regenerate, delete, or replace PDF docs without a focused docs/PDF contract;
- target main;
- close #252, #260, #262, #264, or #136.

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
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/266"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/136"
  source_issues:
    - "https://github.com/Tahjali11/Mythic-Edge/issues/252"
    - "https://github.com/Tahjali11/Mythic-Edge/issues/260"
    - "https://github.com/Tahjali11/Mythic-Edge/issues/262"
    - "https://github.com/Tahjali11/Mythic-Edge/issues/264"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "GitHub issue #266 problem representation"
  target_artifact: "docs/implementation_handoffs/private_local_v1_fixture_placeholder_decode_warning_triage_comparison.md"
  risk_tier: "Medium"
  branch: "codex/analytics-foundation"
  validation:
    - "git diff --check"
    - "py tools/check_agent_docs.py"
    - "path-scoped protected-surface scan for docs/contracts/private_local_v1_fixture_placeholder_decode_warning_triage.md"
    - "path-scoped secret/private-marker scan for docs/contracts/private_local_v1_fixture_placeholder_decode_warning_triage.md"
  stop_conditions:
    - "Do not implement code in Codex B."
    - "Do not print or copy raw matched values or private artifacts."
    - "Do not weaken scanner coverage or suppress findings without explicit policy rationale and tests."
    - "Do not fix all all-repo scanner categories under #266."
    - "Do not make all-repo scanner a failing gate or add CI gates."
    - "Do not regenerate, delete, or replace PDF docs without a focused docs/PDF contract."
    - "Do not change parser/runtime/analytics/local app/workbook/webhook/App Script/Sheets/OpenAI/AI/production behavior."
    - "Do not change credential policy or environment variable contracts."
    - "Do not target main, close #252, close #260, close #262, close #264, or close tracker #136."
```
