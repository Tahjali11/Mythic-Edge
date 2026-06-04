# Private Local V1 Scanner Readiness Reconciliation Contract

## Module

`private_local_v1_scanner_readiness_reconciliation`

Plain English: this contract defines how Mythic Edge should reconcile the
completed private-local-v1 scanner-debt triage tranches into a release-readiness
posture.

This is a contract-writing artifact only. It does not implement scanner,
fixture, docs, parser, analytics, local app, workbook, webhook, Apps Script,
credential, CI, or production behavior changes.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/268
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/136
- Source issues:
  - https://github.com/Tahjali11/Mythic-Edge/issues/252
  - https://github.com/Tahjali11/Mythic-Edge/issues/260
  - https://github.com/Tahjali11/Mythic-Edge/issues/262
  - https://github.com/Tahjali11/Mythic-Edge/issues/264
  - https://github.com/Tahjali11/Mythic-Edge/issues/266
- Source PRs:
  - https://github.com/Tahjali11/Mythic-Edge/pull/259
  - https://github.com/Tahjali11/Mythic-Edge/pull/261
  - https://github.com/Tahjali11/Mythic-Edge/pull/263
  - https://github.com/Tahjali11/Mythic-Edge/pull/265
  - https://github.com/Tahjali11/Mythic-Edge/pull/267
- Branch: `codex/analytics-foundation`
- Expected artifact:
  `docs/contracts/private_local_v1_scanner_readiness_reconciliation.md`

## Source Artifacts

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- issue #268 and tracker #136
- issues #252, #260, #262, #264, and #266
- `docs/contracts/private_local_v1_private_artifact_scanner_env_ignore_posture.md`
- `docs/contracts/private_local_v1_high_risk_scanner_findings_triage.md`
- `docs/contracts/private_local_v1_raw_private_artifact_scanner_triage.md`
- `docs/contracts/private_local_v1_artifact_path_ambiguous_marker_warning_triage.md`
- `docs/contracts/private_local_v1_fixture_placeholder_decode_warning_triage.md`
- associated implementation handoffs and contract-test reports for completed
  scanner-debt tranches, where present
- `docs/contracts/repo_wide_secret_private_marker_scanner.md`
- `docs/contracts/engineering_maturity_index_open_framework.md`
- `tools/check_secret_patterns.py`
- `tests/test_check_secret_patterns.py`
- `tools/check_local_environment.py`
- `tools/check_protected_surfaces.py`
- `tools/select_validation.py`
- `.gitignore`

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/136

Tracker #136 remains open. This contract does not mark the tracker complete.

## Risk Tier

Medium-High.

Reasons:

- the decision affects private-local-v1 release-readiness language;
- all-repo scanner output remains non-clean and includes forbidden-category
  findings;
- unsafe reconciliation could hide real private-artifact risk or weaken future
  scanner expectations;
- this pass may recommend source-issue closure, but must not close issues
  directly;
- parser, analytics, workbook, webhook, Apps Script, credential, local app, and
  production behavior are protected surfaces.

## Owning Layer

Primary owner: Quality / Governance.

Supporting area: Generated / Local Artifacts.

## Internal Project Area

Quality / Governance.

## Truth Owner

The repo secret/private-marker scanner owns deterministic repository
content-safety classification and redacted scanner reporting.

The #268 reconciliation report owns the private-local-v1 scanner-readiness
posture and source-issue lifecycle recommendations.

This contract does not make the scanner or reconciliation report the owner of:

- parser truth;
- analytics truth;
- workbook schema truth;
- webhook payload truth;
- Apps Script truth;
- local app runtime truth;
- credential policy;
- merge, deployment, or production readiness;
- tracker #136 completion;
- AI/model-provider truth.

## Bridge-Code Status

`shared_support`

Allowed data flow:

```text
completed scanner triage contracts + redacted scanner counts
  -> blocker/non-blocker classification
  -> private-local-v1 scanner-readiness posture
  -> source-issue closure or follow-up routing recommendation
```

Forbidden reverse flow:

- reconciliation must not authorize committing raw logs, runtime payloads,
  failed-post payloads, generated data dumps, workbook exports, private local
  paths, secrets, credentials, endpoints, or local-only artifacts;
- reconciliation must not weaken scanner coverage merely to reduce counts;
- reconciliation must not make the all-repo advisory scanner a required CI
  gate;
- reconciliation must not change parser, analytics, workbook, webhook, Apps
  Script, local app runtime, AI, model-provider, or production behavior.

## Files Owned By This Contract

This contract owns:

- `docs/contracts/private_local_v1_scanner_readiness_reconciliation.md`

Expected future comparison artifact:

- `docs/implementation_handoffs/private_local_v1_scanner_readiness_reconciliation_comparison.md`

Expected future review or contract-test artifact:

- `docs/contract_test_reports/private_local_v1_scanner_readiness_reconciliation.md`

Future Codex C may produce a report-only comparison and may recommend issue
lifecycle changes. Codex C must route back to Codex B before changing scanner
category semantics, scanner strictness, all-repo advisory behavior, CI gates,
environment-file policy, protected-surface rules, parser behavior, analytics
behavior, local app behavior, workbook/webhook or Apps Script behavior,
credential policy, or production behavior.

## Observed Current Behavior

### Source Issue State

- Issue #268 is open and owns the scanner-readiness reconciliation pass.
- Issues #252, #260, #262, #264, and #266 supplied the source tranche
  classifications.
- PRs #259, #261, #263, #265, and #267 are reported by issue #268 as merged
  into `codex/analytics-foundation`.
- Tracker #136 remains open.
- Path-scoped changed-file scanner safety remains strict.
- The all-repo scanner remains advisory and non-clean.

### Current Scanner Shape

Issue #268 records this current scanner shape:

```text
mode: all-repo-advisory
result: failed
exit_code: 0
scanned_paths: 762
forbidden: 540
warnings: 901
```

Category-only count summary from issue #268:

| Category | Total | Forbidden | Warnings |
| --- | ---: | ---: | ---: |
| `artifact_path_reference` | 635 | 0 | 635 |
| `raw_player_log_content` | 335 | 335 | 0 |
| `sanitized_fixture_marker` | 174 | 0 | 174 |
| `runtime_status_payload` | 85 | 85 | 0 |
| `ambiguous_private_marker` | 80 | 0 | 80 |
| `private_local_path` | 57 | 57 | 0 |
| `generated_data_dump` | 38 | 38 | 0 |
| `credential_value` | 10 | 10 | 0 |
| failed-post payload category | 9 | 9 | 0 |
| `placeholder_secret_reference` | 9 | 0 | 9 |
| `workbook_export_marker` | 3 | 3 | 0 |
| `live_webhook_url` | 3 | 3 | 0 |
| `decode_replacement_used` | 3 | 0 | 3 |

The failed-post payload category is written in scanner-safe prose in this
contract so the contract does not create warning-only self-findings. Later
reports may use the exact scanner category ID if they do not copy raw payload
content or raw scanner excerpts.

Issue #268 also records that the changed-file scanner currently passes against
`origin/codex/analytics-foundation` with forbidden 0 and warnings 0.

## Contract Decision

Private-local-v1 scanner readiness is not the same as a zero-finding all-repo
scanner.

For the `private_local_v1` release profile, Mythic Edge may be considered
scanner-ready only when all of the following are true:

1. changed-file and path-scoped scanner runs remain strict and pass for the
   release candidate;
2. every all-repo scanner category reported in issue #268 has a durable
   classification from #252, #260, #262, #264, #266, or the #268
   reconciliation report;
3. no selected source tranche leaves an unclassified release-blocking finding;
4. remaining all-repo findings are redacted, non-leaking, expected, historical,
   fixture/governance evidence, or explicitly routed follow-up debt;
5. real `.env*` files, secrets, endpoint values, local logs, generated
   databases, failed-post payloads, workbook exports, and local-only artifacts
   remain uncommitted;
6. no scanner rule, scanner severity, ignore policy, allowlist, or validation
   command is weakened to achieve readiness;
7. readiness language clearly says the all-repo scanner remains advisory and
   non-clean.

The all-repo scanner may remain advisory and non-clean for private-local-v1
only if the reconciliation report explicitly classifies the remaining debt as
non-blocking for the private-local-v1 release profile.

## Classification Vocabulary

Codex C and Codex E must use these labels.

| Label | Meaning |
| --- | --- |
| `release_blocking_cleanup_required` | A finding or family must be fixed or re-routed before private-local-v1 scanner readiness can be claimed. |
| `non_blocking_classified_debt` | A finding or family may remain because it is classified, non-leaking, redacted, and safe for private-local-v1. |
| `optional_polish_followup` | Cleanup may improve readability, scanner confidence, or docs hygiene but does not block private-local-v1. |
| `completed_tranche_ready_to_close` | A source issue can be recommended for Codex G closure because its scoped classification and validation are complete. |
| `deferred_future_release_profile` | A concern is real but belongs to a later release profile, public release hardening, or a separate governance issue. |

## Source-Tranche Reconciliation Requirements

### Issue #252

Codex C must reconcile the `.env*` ignore posture and scanner policy baseline.

Required classification:

- exact root `.env.example` is allowed only as a tracked public template;
- real local `.env*` files must remain ignored or blocked from commits;
- scanner policy must remain strict for changed files;
- all-repo scanner may remain advisory.

Issue #252 may be recommended as `completed_tranche_ready_to_close` only if
the reconciliation report finds no unresolved `.env*` or scanner-policy blocker
for private-local-v1.

### Issue #260

Codex C must reconcile the high-risk scanner categories:

- `credential_value`;
- `live_webhook_url`;
- `workbook_export_marker`.

Required classification:

- no live secret, endpoint, workbook export, or deployment-facing value may be
  accepted as private-local-v1 clean;
- test placeholders, scanner examples, protected-surface vocabulary, and
  intentionally redacted fixtures may be non-blocking only when the #260
  report classified them without raw-value leakage;
- any unresolved real-value risk is `release_blocking_cleanup_required`.

Issue #260 may be recommended as `completed_tranche_ready_to_close` only if no
selected high-risk family remains unclassified or blocking.

### Issue #262

Codex C must reconcile the raw/private artifact categories:

- `raw_player_log_content`;
- `runtime_status_payload`;
- `generated_data_dump`;
- failed-post payload category;
- `private_local_path`.

Required classification:

- committed raw private artifacts are blockers;
- parser/test vocabulary, sanitized evidence fixtures, historical governance
  reports, and redacted scanner tests may be non-blocking only when classified;
- local path references must remain non-sensitive or redacted enough for repo
  use;
- generated-data, runtime-status, and failed-post vocabulary must not authorize
  committing generated runtime artifacts.

Issue #262 may be recommended as `completed_tranche_ready_to_close` only if no
selected raw/private category remains unclassified or blocking.

### Issue #264

Codex C must reconcile warning categories:

- `artifact_path_reference`;
- `ambiguous_private_marker`.

Required classification:

- broad docs/handoff/report references may remain when they are route markers,
  policy descriptions, or historical workflow evidence;
- ambiguous parser/evidence vocabulary must not be "fixed" by changing parser
  behavior;
- any cleanup must be optional docs/tooling polish unless a concrete private
  artifact leak is found.

Issue #264 may be recommended as `completed_tranche_ready_to_close` only if no
selected warning family blocks private-local-v1.

### Issue #266

Codex C must reconcile warning categories:

- `sanitized_fixture_marker`;
- `placeholder_secret_reference`;
- `decode_replacement_used`.

Required classification:

- sanitized fixture markers may remain when they are expected sanitized
  evidence and covered by fixture provenance rules;
- placeholder-looking values may remain when they are scanner, sanitizer, or
  redaction-test vocabulary;
- decode warnings may remain as docs readability or scanner-confidence debt
  only if they do not expose private content;
- PDF regeneration or file-type policy changes require a later focused issue.

Issue #266 may be recommended as `completed_tranche_ready_to_close` only if no
selected warning family blocks private-local-v1.

## Release-Blocking Criteria

Any of these conditions blocks private-local-v1 scanner-readiness claims:

- changed-file or path-scoped scanner reports any forbidden finding;
- a changed-file warning is unexplained or unclassified;
- a source tranche lacks a durable comparison/report or equivalent evidence;
- an all-repo category from issue #268 remains unclassified;
- a report copies raw matched values, raw scanner excerpts, raw log-like lines,
  private paths, raw payloads, endpoint values, spreadsheet IDs, credentials,
  or generated artifact contents;
- a real secret, credential, endpoint, environment value, raw private artifact,
  generated database, runtime file, failed post, workbook export, or local-only
  artifact is tracked or staged;
- scanner coverage, severity, redaction, or changed-file strictness is weakened
  without a separate approved contract;
- root `.env.example` policy no longer preserves real `.env*` safety;
- protected-surface cleanup is required before the release profile but lacks a
  scoped follow-up issue.

## Non-Blocking Classified Debt Criteria

All-repo scanner findings may be classified as non-blocking only when they are:

- already classified by the source tranche and accepted by review;
- limited to synthetic, sanitized, placeholder, governance, documentation,
  historical, or test-vocabulary contexts;
- summarized by category, count, and repo-relative path family only;
- not copied as raw values or raw excerpts into reports;
- not evidence of a committed private local artifact;
- paired with a follow-up route when cleanup would be useful but unnecessary
  for `private_local_v1`.

## Operator-Facing Readiness Language

Codex C and Codex E must avoid claiming:

- "the all-repo scanner is clean";
- "all private-artifact debt is gone";
- "the repo is public-release clean";
- "tracker #136 is complete";
- "production or external integration readiness is proven".

Approved wording pattern after validation:

```text
Private-local-v1 scanner readiness is conditionally release-clean for the
private_local_v1 profile: changed-file/path-scoped scanner strictness is clean,
the known all-repo scanner debt is classified and non-blocking for this release
profile, and remaining cleanup is optional or deferred. The all-repo scanner
remains advisory and non-clean.
```

If any blocker remains, the report must instead say:

```text
Private-local-v1 scanner readiness is not yet release-clean. The blocking
items are: <category/family summaries only>.
```

## Public Interface

Commands and surfaces governed by this contract:

```powershell
py tools\check_secret_patterns.py --all
py tools\check_secret_patterns.py --base origin/codex/analytics-foundation
@'
docs/contracts/private_local_v1_scanner_readiness_reconciliation.md
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
py tools\check_local_environment.py --profile clean_clone --format json
py tools\check_local_environment.py --profile clean_install_transition_audit --format json
py -m pytest -q tests\test_check_secret_patterns.py tests\test_check_local_environment.py tests\test_check_protected_surfaces.py
```

The scanner may print redacted summaries. Reconciliation reports must not copy
raw scanner lines when the same point can be made with category, count, and
repo-relative path-family summaries.

## Inputs

Allowed inputs:

- tracked repo files;
- issue #268 category-count summary;
- scanner category IDs, severity, and counts;
- source contracts, handoffs, and contract-test reports from #252, #260, #262,
  #264, and #266;
- redacted scanner output;
- Git status, branch, and changed-file lists;
- `.gitignore` and local artifact policy docs;
- validation command outputs.

Forbidden inputs:

- raw Player.log contents;
- raw private JSONL payloads;
- raw runtime status payloads;
- raw failed-post payloads;
- raw generated database or generated data contents;
- raw workbook export contents;
- raw secret, token, credential, endpoint, spreadsheet ID, or environment
  values;
- private local path contents or private local artifact contents.

## Outputs

Required future reconciliation output:

- issue, tracker, branch, and source-tranche summary;
- source-tranche lifecycle recommendation table;
- blocker/non-blocker classification table;
- current changed-file scanner result;
- current all-repo advisory scanner category summary;
- readiness verdict for the `private_local_v1` profile;
- optional follow-up recommendations;
- explicit statement that all-repo scanner remains advisory and non-clean, if
  still true;
- protected-surface and raw-value redaction status;
- validation commands and results;
- next recommended workflow role.

Forbidden output:

- raw matched values;
- raw scanner excerpts;
- raw private paths;
- raw log-like lines;
- fixture payload excerpts;
- PDF decode text;
- endpoint, spreadsheet, credential, token, key, or environment values;
- generated database contents;
- runtime payload contents;
- failed-post payload contents;
- workbook export contents.

## Issue Lifecycle Policy

Codex C may recommend closure for source issues only when the source issue's
scoped tranche is complete and non-blocking for private-local-v1.

Codex E must independently verify the recommendation before Codex F/G routing.

Codex G owns actual issue closure and tracker updates. This contract does not
authorize Codex B, C, or E to close #252, #260, #262, #264, #266, #268, or
tracker #136.

Tracker #136 must remain open unless a separate tracker reconciliation proves
the broader private-local-v1 maturity work is complete.

## Validation Requirements

Codex C must run or explain why it could not run:

```powershell
git status --short --branch --untracked-files=all
py tools\check_secret_patterns.py --all
py tools\check_secret_patterns.py --base origin/codex/analytics-foundation
py -m pytest -q tests\test_check_secret_patterns.py tests\test_check_local_environment.py tests\test_check_protected_surfaces.py
git diff --check
py tools\check_agent_docs.py
py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation
@'
docs/contracts/private_local_v1_scanner_readiness_reconciliation.md
docs/implementation_handoffs/private_local_v1_scanner_readiness_reconciliation_comparison.md
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
@'
docs/contracts/private_local_v1_scanner_readiness_reconciliation.md
docs/implementation_handoffs/private_local_v1_scanner_readiness_reconciliation_comparison.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
```

Codex E must verify:

- no raw values or raw excerpts were copied;
- no scanner weakening occurred;
- no protected surfaces were changed;
- source-tranche closure recommendations are supported by evidence;
- readiness wording does not overclaim beyond `private_local_v1`.

## Acceptance Criteria

The #268 reconciliation package is acceptable when:

- this contract exists and is cited by the comparison/report;
- #252, #260, #262, #264, and #266 are reconciled explicitly;
- every issue #268 category is classified as blocking, non-blocking,
  optional, completed, or deferred;
- changed-file/path-scoped scanner strictness is preserved;
- all-repo advisory/non-clean status is reported honestly;
- private-local-v1 readiness language is explicit and limited;
- source-issue closure recommendations are separated from actual closure;
- no raw private content or sensitive value is copied into artifacts;
- validation evidence is recorded;
- protected surfaces remain untouched.

## Suspected Gaps

- The all-repo scanner count is intentionally non-clean; future readers may
  confuse "classified" with "removed" unless reports use precise language.
- Some historical docs and reports may remain noisy for public-release
  readiness even if non-blocking for private-local-v1.
- PDF decode warnings may still reduce scanner confidence for docs maintenance.
- Source issue lifecycle may lag behind merged PR evidence until Codex G closes
  issues explicitly.

## Unknowns

- Whether later public-release profiles will require a clean all-repo scanner.
- Whether future fixture-governance work will reduce sanitized fixture warning
  counts or preserve them as expected evidence.
- Whether the all-repo scanner should eventually emit a machine-readable
  baseline report for classified debt.
- Whether tracker #136 has additional private-local-v1 blockers unrelated to
  scanner readiness.

## Protected Surfaces

This contract does not authorize changes to:

- parser behavior;
- parser state final reconciliation;
- parser event classes;
- match identity;
- game identity;
- deduplication;
- analytics schema, migrations, or ingest semantics;
- local app/UI behavior;
- workbook schema;
- webhook payload shape;
- Apps Script behavior;
- Google Sheets behavior;
- output transport;
- production behavior;
- OpenAI/model-provider behavior;
- AI/coaching behavior;
- Line Tracer behavior;
- CI gates;
- Pyright gate behavior;
- scanner category semantics or severity;
- secrets, credentials, tokens, API keys, endpoint values, spreadsheet IDs, or
  environment values;
- raw logs, private JSONL artifacts, generated SQLite databases, runtime files,
  failed posts, workbook exports, app-data files, generated data, or local-only
  artifacts.

## Codex C Implementation Scope

Codex C should perform a report-only reconciliation:

1. verify current branch and git status;
2. inspect issue #268, tracker #136, and source issue/PR states;
3. inspect the five source contracts, handoffs, and reports;
4. refresh scanner summaries without copying raw matched values;
5. classify each source tranche and each remaining scanner family;
6. produce
   `docs/implementation_handoffs/private_local_v1_scanner_readiness_reconciliation_comparison.md`;
7. recommend whether #252, #260, #262, #264, #266, and #268 can route to Codex
   E/F/G;
8. preserve all protected surfaces and scanner behavior.

Codex C must not implement cleanup unless a later prompt explicitly authorizes
it under a scoped contract.

## Pasteable Codex C Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison thread for issue #268.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/268

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/136

Branch:
codex/analytics-foundation

Contract:
docs/contracts/private_local_v1_scanner_readiness_reconciliation.md

Goal:
Produce docs/implementation_handoffs/private_local_v1_scanner_readiness_reconciliation_comparison.md as a report-only reconciliation of private-local-v1 scanner readiness after #252, #260, #262, #264, and #266.

Before editing:
- Confirm branch and git status.
- Inspect issue #268, tracker #136, source issues #252/#260/#262/#264/#266, and PRs #259/#261/#263/#265/#267.
- State what private-local-v1 scanner readiness is supposed to prove, what current scanner output shows, why all-repo advisory debt can or cannot remain, and the exact minimal report-only plan.

Do:
- Compare current repo state and source tranche reports against the contract.
- Refresh scanner summaries using category/count/path-family summaries only.
- Do not paste raw scanner excerpts, private paths, raw logs, payloads, workbook exports, endpoints, secrets, credentials, tokens, spreadsheet IDs, environment values, generated database contents, or local-only artifact contents.
- Classify each source tranche as release-blocking, non-blocking classified debt, optional polish, completed tranche ready to close, or deferred future release profile.
- Recommend which source issues can route to Codex G for closure and which follow-ups remain.
- Preserve changed-file/path-scoped scanner strictness and all-repo advisory semantics.

Do not:
- Implement cleanup unless explicitly authorized by a later prompt.
- Change scanner rules, scanner severities, ignore policy, CI gates, or Pyright
  gate behavior.
- Change parser, analytics, local app/UI, workbook, webhook, Apps Script,
  Google Sheets, production, OpenAI/model-provider, AI/coaching, or Line
  Tracer behavior.
- Touch secrets, credentials, raw logs, generated data, runtime files, failed
  posts, workbook exports, generated SQLite files, app-data files, or
  local-only artifacts.
- Target main.
- Close #252, #260, #262, #264, #266, #268, or tracker #136.
- Stage, commit, push, or open a PR.

Validation:
git status --short --branch --untracked-files=all
py tools\check_secret_patterns.py --all
py tools\check_secret_patterns.py --base origin/codex/analytics-foundation
py -m pytest -q tests\test_check_secret_patterns.py tests\test_check_local_environment.py tests\test_check_protected_surfaces.py
git diff --check
py tools\check_agent_docs.py
@'
docs/contracts/private_local_v1_scanner_readiness_reconciliation.md
docs/implementation_handoffs/private_local_v1_scanner_readiness_reconciliation_comparison.md
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
@'
docs/contracts/private_local_v1_scanner_readiness_reconciliation.md
docs/implementation_handoffs/private_local_v1_scanner_readiness_reconciliation_comparison.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin

Final handoff must include:
- role performed
- issue/tracker reviewed
- contract used
- artifact produced
- source tranches reconciled
- readiness verdict
- source issue closure recommendations
- validation results
- protected surfaces status
- remaining risks
- next recommended role
- pasteable Codex E prompt
- workflow_handoff block
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/268"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/136"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "GitHub issue #268 and completed scanner-debt tranche contracts/reports"
  target_artifact: "docs/implementation_handoffs/private_local_v1_scanner_readiness_reconciliation_comparison.md"
  contract_artifact: "docs/contracts/private_local_v1_scanner_readiness_reconciliation.md"
  risk_tier: "Medium-High"
  branch: "codex/analytics-foundation"
  stop_conditions:
    - "Do not implement cleanup in the reconciliation comparison unless explicitly authorized."
    - "Do not weaken scanner coverage, scanner severity, redaction, or path-scoped strictness."
    - "Do not claim all-repo scanner cleanliness while all-repo scanner remains advisory/non-clean."
    - "Do not close #252, #260, #262, #264, #266, #268, or tracker #136 outside Codex G lifecycle handling."
    - "Do not change parser/runtime/analytics/local app/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
    - "Do not create or commit generated/private/runtime/local artifacts or secrets."
```
