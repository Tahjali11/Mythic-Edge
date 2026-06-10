# CodeQL Code Scanning Alert Triage Contract

## Module

`codeql_code_scanning_alert_triage`

Plain English: this contract defines how Mythic Edge should triage and
remediate the current open GitHub CodeQL/code-scanning alerts without weakening
scanner value, changing unrelated product behavior, or treating alert dismissal
as a substitute for evidence.

This is a Codex B contract-writing artifact only. It does not implement fixes,
dismiss alerts, change CodeQL settings, change CI gates, change parser truth,
or touch secrets/private artifacts.

## Source Issue

- Parent issue: https://github.com/Tahjali11/Mythic-Edge/issues/330
- Child issue: https://github.com/Tahjali11/Mythic-Edge/issues/331
- Current intended branch: `codex/analytics-foundation`
- Contract artifact:
  `docs/contracts/codeql_code_scanning_alert_triage.md`

Required authority and role docs:

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`

## Tracker

Parent security/quality workflow: https://github.com/Tahjali11/Mythic-Edge/issues/330

Parent issue #330 and child issue #331 must remain open after this contract.
Alert closure and issue lifecycle handling route to later reviewed implementation,
review, submitter, and deployer threads.

## Risk Tier

High.

Reasons:

- current open alerts include high-severity path and URL findings;
- fixes may touch local app import behavior, parser/runtime generated status
  files, privacy scanners, and GitHub Actions workflow permissions;
- some flagged files are protected or boundary-sensitive surfaces;
- false-positive dismissal without evidence would weaken future security
  posture;
- broad fixes could accidentally change parser truth, local app UX, analytics
  ingest, generated artifact policy, or CI behavior.

## Owning Layer

Primary owner: Quality / Governance security triage.

Supporting owners:

- Local App / UI for manual JSONL import path handling;
- Parser and Corpus / Provenance for runtime status and gameplay-action status
  file surfaces;
- Quality / Governance for evidence status/report privacy scanners and GitHub
  Actions workflow permission posture;
- External / Collaboration Surface for GitHub CodeQL/code-scanning alert
  evidence.

## Internal Project Area

Quality / Governance.

Adjacent project areas:

- Local App / UI;
- Parser;
- Corpus / Provenance;
- Generated / Local Artifacts;
- External / Collaboration Surface.

## Truth Owner

GitHub CodeQL owns alert detection evidence, not final project truth.

Final classification truth for this issue is the reviewed triage artifact and
implementation/review evidence produced by the Mythic Edge workflow.

Layer truth remains unchanged:

- parser/state owns MTGA event interpretation, match/game identity,
  deduplication, and parser-normalized facts;
- local app import code owns operator-selected file import orchestration;
- runtime/status helpers own generated status artifacts only;
- evidence/privacy helpers own privacy finding summaries only;
- GitHub Actions workflow config owns CI token permission posture;
- CodeQL alerts are security signals that must be reviewed, not blindly
  dismissed and not blindly treated as permission to refactor unrelated code.

## Bridge-Code Status

`shared_support`

Allowed flow:

```text
GitHub CodeQL alert snapshot
  -> Codex B contract and classification policy
  -> Codex C focused comparison/remediation handoff
  -> Codex E contract-test/security review
  -> Codex F/G submission and lifecycle handling
```

Forbidden reverse flow:

- alert triage must not change parser truth ownership;
- alert triage must not move path validation into downstream UI-only logic;
- scanner findings must not authorize committing raw/private/generated
  artifacts;
- CodeQL alert dismissal must not happen without documented reviewer evidence;
- workflow-permission changes must not become broad CI gate changes unless a
  future contract authorizes that expansion.

## Files Owned By This Contract

This contract owns:

- `docs/contracts/codeql_code_scanning_alert_triage.md`

Expected future Codex C artifact:

- `docs/implementation_handoffs/codeql_code_scanning_alert_triage_comparison.md`

Expected future Codex E artifact:

- `docs/contract_test_reports/codeql_code_scanning_alert_triage.md`

Future Codex C may inspect and, if justified by the contract comparison, change:

- `src/mythic_edge_parser/local_app/import_jobs.py`
- `src/mythic_edge_parser/app/runtime_surfaces.py`
- `src/mythic_edge_parser/app/gameplay_actions.py`
- `src/mythic_edge_parser/app/evidence_validation_report_wiring.py`
- `src/mythic_edge_parser/app/evidence_runtime_status.py`
- `.github/workflows/repo-checks.yml`
- focused tests covering the touched behavior

Codex C must route back to Codex B before changing parser event classes,
parser state final reconciliation, match/game identity semantics, analytics
schema/migrations, workbook/webhook/App Script/Sheets behavior, production
behavior, OpenAI/model-provider behavior, secret/credential policy, or broad CI
gate posture.

## Current Alert Inventory

Codex B refreshed the current CodeQL open-alert snapshot with:

```powershell
gh api -H 'Accept: application/vnd.github+json' '/repos/Tahjali11/Mythic-Edge/code-scanning/alerts?state=open&per_page=100'
```

Current open alerts:

| Alert | Rule | Severity | File | Line |
| --- | --- | --- | --- | --- |
| 16 | `py/path-injection` | high | `src/mythic_edge_parser/local_app/import_jobs.py` | 565 |
| 15 | `py/path-injection` | high | `src/mythic_edge_parser/local_app/import_jobs.py` | 556 |
| 14 | `py/path-injection` | high | `src/mythic_edge_parser/local_app/import_jobs.py` | 540 |
| 13 | `py/path-injection` | high | `src/mythic_edge_parser/local_app/import_jobs.py` | 532 |
| 12 | `py/path-injection` | high | `src/mythic_edge_parser/local_app/import_jobs.py` | 466 |
| 11 | `py/path-injection` | high | `src/mythic_edge_parser/local_app/import_jobs.py` | 458 |
| 10 | `py/path-injection` | high | `src/mythic_edge_parser/local_app/import_jobs.py` | 446 |
| 9 | `py/path-injection` | high | `src/mythic_edge_parser/local_app/import_jobs.py` | 440 |
| 8 | `py/path-injection` | high | `src/mythic_edge_parser/app/runtime_surfaces.py` | 239 |
| 7 | `py/path-injection` | high | `src/mythic_edge_parser/app/runtime_surfaces.py` | 237 |
| 6 | `py/path-injection` | high | `src/mythic_edge_parser/app/gameplay_actions.py` | 191 |
| 5 | `py/path-injection` | high | `src/mythic_edge_parser/app/gameplay_actions.py` | 172 |
| 4 | `py/path-injection` | high | `src/mythic_edge_parser/app/gameplay_actions.py` | 121 |
| 3 | `py/incomplete-url-substring-sanitization` | high | `src/mythic_edge_parser/app/evidence_validation_report_wiring.py` | 620 |
| 2 | `py/incomplete-url-substring-sanitization` | high | `src/mythic_edge_parser/app/evidence_runtime_status.py` | 540 |
| 1 | `actions/missing-workflow-permissions` | medium | `.github/workflows/repo-checks.yml` | 9 |

Codex C must refresh the alert inventory before implementation and record any
drift from this table.

## Alert Triage Objective

The triage pass must:

1. verify the current open alert inventory;
2. group alerts by rule family and affected boundary;
3. inspect source-to-sink behavior for each alert group;
4. classify each alert as `fix_required`, `likely_false_positive`,
   `accepted_risk`, or `needs_more_evidence`;
5. implement only focused fixes for `fix_required` alerts;
6. add regression tests for remediated or intentionally preserved behavior;
7. document false-positive or accepted-risk rationale without weakening scanner
   value;
8. leave CodeQL alert dismissal to reviewed follow-up unless explicitly
   authorized.

## Classification And Label Policy

Each alert must receive one classification label in the Codex C handoff and
Codex E report.

### `fix_required`

Use when source inspection shows plausible attacker-controlled or
operator-controlled input can reach a filesystem, URL, workflow-permission, or
privacy-sensitive sink without sufficient normalization, containment, or
authorization.

Required evidence:

- affected alert numbers;
- source input and sink;
- first unsafe value or ambiguity;
- exact code/test change;
- validation command result;
- remaining CodeQL verification status.

### `likely_false_positive`

Use when the code is already safe but CodeQL cannot prove it.

Required evidence:

- affected alert numbers;
- current guards that make the flow safe;
- focused tests that pin the guard, or a documented reason why a test is not
  meaningful;
- explanation of why no code change is safer than churn;
- explicit statement that no CodeQL dismissal was performed by Codex C unless
  separately authorized.

### `accepted_risk`

Use sparingly when a behavior is intentionally allowed for private-local-v1 and
cannot or should not be eliminated now.

Required evidence:

- affected alert numbers;
- why the behavior is necessary;
- who controls the input;
- what harm is bounded;
- what user or repo authority accepted the risk;
- follow-up issue if the risk should be revisited.

Codex C must not create accepted-risk dismissals by itself. Accepted risk
requires explicit user or reviewer approval.

### `needs_more_evidence`

Use when Codex C cannot safely classify or fix the alert under this contract.

Required route:

- stop implementation for that alert family;
- document what evidence is missing;
- route to Codex A/B/E as appropriate.

## Path-Injection Remediation Contract

### Local App Import Paths

Affected alerts:

- #9 through #16 in `src/mythic_edge_parser/local_app/import_jobs.py`

Current behavior already includes useful guardrails:

- URL-like inputs are rejected;
- UNC-like inputs are rejected;
- extension must be `.jsonl`;
- directories and missing paths are rejected;
- source paths are not echoed in job status responses.

Codex C must verify whether those guards are sufficient for CodeQL and for the
local-app threat model.

If fixes are required, they must preserve the intended manual import behavior:

- local operator may select local `.jsonl` files;
- explicit single-file and explicit batch imports remain supported;
- quoted Windows copy-as-path values remain supported when currently tested;
- responses must remain symbolic and must not echo raw private paths;
- malformed JSONL must fail without raw line, raw path, or database creation.

Required safety expectations:

- reject URL, UNC, empty, non-string, directory, non-`.jsonl`, and missing
  inputs before opening files;
- normalize and resolve selected paths before reading;
- keep duplicate detection based on resolved paths;
- avoid using unchecked raw strings directly in filesystem calls;
- decide and document symlink behavior before changing it;
- do not copy selected JSONL files into the repo or app-data unless a later
  contract authorizes retention;
- do not store raw JSONL payloads in SQLite or reports.

Recommended implementation shape:

- add or reuse a small helper that returns a validated local file path plus
  safe display metadata;
- keep all source display labels symbolic;
- add adversarial tests for traversal-looking names, quoted paths, URL-looking
  strings, UNC paths, directories, extension bypass attempts, duplicate
  resolved paths, and raw-path non-echo.

### Parser/Runtime Generated Status File Paths

Affected alerts:

- #7 and #8 in `src/mythic_edge_parser/app/runtime_surfaces.py`
- #4 through #6 in `src/mythic_edge_parser/app/gameplay_actions.py`

Observed pattern:

- parser/runtime match IDs can be interpolated into generated status filenames.

Required safety expectations:

- preserve parser-owned `match_id` values inside payloads and dedup logic;
- derive filesystem path segments from a safe filename/stem helper instead of
  raw match IDs;
- ensure generated paths remain under the intended status/action root;
- reject or encode path separators, drive prefixes, `..`, empty path segments,
  device-like names, and other filesystem control characters;
- keep active/latest status files compatible;
- avoid changing match identity, game identity, deduplication, final
  reconciliation, or parser event payload shapes.

Recommended implementation shape:

- introduce a small local helper for status file names, such as a safe stem or
  stable digest of the raw match ID;
- keep raw match ID in JSON payload fields where parser truth expects it;
- add focused tests showing malicious-looking match IDs cannot escape the
  status root and do not change parser-visible identity.

If the safest fix would change parser identity semantics or public payload
shape, Codex C must stop and route back to Codex B.

## URL Sanitization Remediation Contract

Affected alerts:

- #3 in `src/mythic_edge_parser/app/evidence_validation_report_wiring.py`
- #2 in `src/mythic_edge_parser/app/evidence_runtime_status.py`

Observed pattern:

- privacy classification currently uses substring checks for hosts such as
  `script.google.com` and `hooks.` after a broader forbidden-text regex match.

Required safety expectations:

- no raw URL, webhook, credential, local path, raw Player.log, runtime status,
  failed post, workbook export, generated data, or local-only artifact value may
  be echoed in reports;
- privacy findings may over-report safely, but they must not under-report
  obvious webhook/runtime artifacts;
- domain/host checks must not rely on unsafe substring logic that accepts
  adversarial hostnames as trusted;
- malformed or adversarial URL-like strings must be redacted or classified
  without throwing;
- code should prefer a shared or parallel helper pattern so the two evidence
  modules do not drift.

Recommended implementation shape:

- extract URL-like tokens or reuse a robust regex/URL parser helper;
- classify known runtime/webhook hosts using exact host or approved suffix
  rules rather than raw substring trust;
- preserve existing privacy finding field names unless a contract amendment
  authorizes schema change;
- add tests for true webhook/runtime URLs, adversarial hostnames, URL text in
  query/path positions, malformed URL-like strings, and no raw value echo.

If Codex C finds that both evidence modules should share a new helper in a
separate shared-support module, it may do so only if the helper is tightly
scoped to privacy detection and tests cover both callers. Otherwise, duplicate
small safe logic is acceptable to reduce blast radius.

## GitHub Actions Permissions Contract

Affected alert:

- #1 in `.github/workflows/repo-checks.yml`

Required safety expectations:

- workflow token permissions must be explicit and least-privilege for the repo
  checks workflow;
- expected first posture is read-only repository contents access unless a
  specific workflow step requires more;
- do not add write permissions for tests, lint, protected-surface checks, or
  checkout;
- preserve existing push and pull request triggers;
- preserve checkout, Python setup, package install, pytest, protected-surface,
  and Ruff behavior.

Recommended implementation shape:

```yaml
permissions:
  contents: read
```

Codex C must verify that the workflow does not need additional permissions
before adding anything broader.

## Evidence Required Before Changing Code

Before implementing a fix for each alert family, Codex C must record:

- refreshed alert numbers and locations;
- current source input and sink;
- whether the input is local-operator, parser-produced, GitHub workflow, or
  generated status data;
- why current guards are insufficient or why they are sufficient;
- exact files expected to change;
- tests to add or update;
- protected surfaces touched or avoided.

Do not make speculative refactors just because a file is security-adjacent.

## False Positive, Dismissal, And Accepted-Risk Policy

Codex C may document a likely false positive, but must not dismiss CodeQL
alerts through the GitHub UI/API unless the user explicitly asks for dismissal
after Codex E review.

No alert may be dismissed without:

- alert number and rule;
- exact affected code path;
- source-to-sink explanation;
- current or added tests;
- reviewer agreement;
- reason chosen from the CodeQL dismissal vocabulary, if dismissal is later
  performed;
- issue or PR link preserving the rationale.

Accepted-risk classification requires explicit user approval or a reviewed
governance decision. It is not a Codex C default.

## Protected-Surface Boundaries

This issue may authorize focused security hardening in the named files, but it
does not authorize unrelated behavior changes.

Do not change:

- parser behavior beyond path-safe generated status file naming;
- parser state final reconciliation;
- parser event classes;
- event kind values;
- parser payload shapes;
- match/game identity or deduplication semantics;
- analytics schema or migrations;
- analytics ingest semantics except where tests prove import safety is
  preserved;
- workbook schema;
- webhook payload shape;
- Apps Script behavior;
- Google Sheets behavior;
- production behavior;
- OpenAI/model-provider behavior;
- AI/coaching behavior;
- Line Tracer behavior;
- secret, credential, token, webhook, spreadsheet, or environment-variable
  policy beyond redaction/safety tests;
- broad CI gate posture beyond least-privilege workflow permissions for
  `.github/workflows/repo-checks.yml`.

Do not create, copy, sanitize, commit, print, or expose:

- raw Player.log content;
- private JSONL artifacts;
- generated SQLite databases, WAL, SHM, or journal files;
- runtime status files;
- runtime logs;
- failed posts;
- workbook exports;
- app-data files;
- private paths;
- raw hashes;
- secrets or credentials;
- local-only artifacts.

## Privacy And Secret-Handling Boundaries

Security triage output may name file paths in the repository and CodeQL alert
numbers. It must not paste raw private local paths, raw JSONL bodies, raw
Player.log excerpts, raw webhook URLs, token-like values, spreadsheet IDs, or
environment values.

When demonstrating redaction behavior in tests, use synthetic placeholder
values and assert that raw values are absent from output.

## Validation Requirements

Codex C should run the smallest relevant focused tests first, then broaden only
as needed.

Recommended focused validation by alert family:

```powershell
py -m pytest -q tests\test_analytics_manual_jsonl_import.py
py -m pytest -q tests\test_runtime_surfaces.py tests\test_gameplay_actions.py
py -m pytest -q tests\test_evidence_runtime_status.py tests\test_evidence_validation_report_wiring.py
py -m pytest -q tests\test_check_secret_patterns.py tests\test_check_protected_surfaces.py
py -m ruff check src tests tools
git diff --check
py tools\check_agent_docs.py
```

Required path-scoped scans over changed files:

```powershell
@'
<changed files>
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin

@'
<changed files>
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
```

Required CodeQL verification:

- refresh the CodeQL alert snapshot before implementation;
- after implementation, inspect PR checks or code-scanning alerts when
  available;
- do not claim CodeQL closure until GitHub shows the alert resolved, dismissed
  with approved rationale, or otherwise reviewed;
- if CodeQL does not rerun in the local thread, state that alert closure remains
  unverified.

## Expected Codex C Implementation Scope

Codex C should start by producing a comparison/handoff that maps every alert
number to a classification and implementation decision.

Implementation may proceed in one PR only if the diff remains focused and all
three alert families are covered by tests. If any family expands, split into
follow-up child issues:

1. local-app JSONL import path safety;
2. parser/runtime generated status filename safety;
3. evidence privacy URL classification;
4. GitHub Actions least-privilege permissions.

Codex C must not close #330 or #331. Closing routes to Codex G after reviewed
work is merged and CodeQL status is recorded.

## Expected Codex E Review / Report Requirements

Codex E must produce:

- findings-first review or
  `docs/contract_test_reports/codeql_code_scanning_alert_triage.md`;
- alert-by-alert classification table;
- source-to-sink review for each changed family;
- confirmation that tests cover adversarial path/URL/workflow cases;
- explicit protected-surface status;
- explicit secret/private-artifact status;
- CodeQL status after PR checks when available, or residual risk if not yet
  available;
- recommendation to route to Codex D, F, or back to B/A.

Codex E must not silently dismiss alerts or accept risk without documented
approval.

## Acceptance Criteria

- Contract exists at
  `docs/contracts/codeql_code_scanning_alert_triage.md`.
- Current CodeQL alert snapshot is recorded.
- Alert classification labels and evidence requirements are defined.
- Path-injection remediation boundaries are defined for local-app imports and
  parser/runtime generated status files.
- URL sanitization remediation boundaries are defined.
- GitHub Actions permissions remediation boundaries are defined.
- False-positive, dismissal, and accepted-risk policy is defined.
- Protected-surface and private-artifact boundaries are explicit.
- Codex C and Codex E validation expectations are defined.
- Pasteable Codex C prompt and workflow handoff are included.

## Open Questions / Contract Risks

- CodeQL alert locations can drift after future pushes; Codex C must refresh the
  snapshot before implementation.
- Some path-injection alerts may be false positives around already-restricted
  local paths. Do not churn code without source-to-sink evidence.
- Some path-injection alerts may be real around match IDs becoming filenames.
  Fixes must preserve parser-visible match IDs while making filenames safe.
- URL sanitizer changes could under-detect privacy markers if over-narrowed.
  Tests must cover both true positives and adversarial hostnames.
- Workflow permission changes are likely low-risk, but `.github/workflows/**`
  is still a protected environment/runtime surface and must be scanned/reviewed.

## Next Workflow Action

Next role: Codex C / Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer.

Parent issue:
https://github.com/Tahjali11/Mythic-Edge/issues/330

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/331

Current branch:
codex/analytics-foundation

Contract:
docs/contracts/codeql_code_scanning_alert_triage.md

Target handoff artifact:
docs/implementation_handoffs/codeql_code_scanning_alert_triage_comparison.md

Goal:
Refresh the current CodeQL open-alert snapshot, compare each alert against the
contract, classify every alert, and implement only focused fixes that are
required by evidence.

Before editing:
- Confirm branch and git status.
- Refresh CodeQL alerts with:
  gh api -H 'Accept: application/vnd.github+json' '/repos/Tahjali11/Mythic-Edge/code-scanning/alerts?state=open&per_page=100'
- Read issues #330 and #331, the contract, and the flagged source/test files.
- State the alert-family implementation plan.

Do:
- classify each alert as fix_required, likely_false_positive, accepted_risk, or needs_more_evidence;
- preserve parser truth ownership;
- keep local app import behavior compatible while hardening path handling if required;
- preserve parser-visible match IDs while making generated status filenames safe if required;
- harden URL/runtime-artifact privacy detection without raw value echo;
- add least-privilege permissions to repo-checks workflow if still required;
- add focused regression tests;
- write docs/implementation_handoffs/codeql_code_scanning_alert_triage_comparison.md.

Do not:
- dismiss CodeQL alerts without explicit user approval after review;
- weaken scanner coverage;
- target main;
- change parser state final reconciliation, parser event classes, event kind values, parser payload shapes, match/game identity or deduplication semantics, analytics schema/migrations, workbook schema, webhook payload shape, Apps Script/Sheets behavior, production behavior, OpenAI/model-provider behavior, AI/coaching behavior, or Line Tracer behavior;
- create, copy, sanitize, commit, print, or expose raw Player.log content, private JSONL artifacts, generated SQLite files, runtime files, failed posts, workbook exports, app-data files, private paths, raw hashes, secrets, credentials, environment values, or local-only artifacts;
- close #330 or #331.

Suggested validation:
py -m pytest -q tests\test_analytics_manual_jsonl_import.py
py -m pytest -q tests\test_runtime_surfaces.py tests\test_gameplay_actions.py
py -m pytest -q tests\test_evidence_runtime_status.py tests\test_evidence_validation_report_wiring.py
py -m pytest -q tests\test_check_secret_patterns.py tests\test_check_protected_surfaces.py
py -m ruff check src tests tools
git diff --check
py tools\check_agent_docs.py
Run path-scoped protected-surface and secret/private-marker scans over changed files.

Final output:
- role performed
- issues reviewed
- CodeQL alert snapshot summary
- alert classification table
- files changed
- implementation summary
- validation run and results
- CodeQL rerun/status evidence or residual risk
- protected-surface and secret/private-artifact status
- next recommended role
- pasteable Codex E prompt
- workflow_handoff block
```

```yaml
workflow_handoff:
  parent_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/330"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/331"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "GitHub issue #331 and live CodeQL open-alert snapshot"
  contract_artifact: "docs/contracts/codeql_code_scanning_alert_triage.md"
  target_artifact: "docs/implementation_handoffs/codeql_code_scanning_alert_triage_comparison.md"
  risk_tier: "High"
  branch: "codex/analytics-foundation"
  alert_snapshot:
    total_open: 16
    path_injection_high: 13
    incomplete_url_substring_sanitization_high: 2
    missing_workflow_permissions_medium: 1
  validation:
    - "git diff --check -- docs\\contracts\\codeql_code_scanning_alert_triage.md"
    - "py tools\\check_agent_docs.py"
    - "path-scoped protected-surface scan over contract file"
    - "path-scoped secret/private-marker scan over contract file"
  stop_conditions:
    - "Do not implement code in Codex B."
    - "Do not dismiss CodeQL alerts without documented review evidence and explicit approval."
    - "Do not weaken scanner coverage."
    - "Do not change parser truth ownership, analytics schema, workbook/webhook/App Script/Sheets, OpenAI/AI/coaching, production behavior, or raw/private artifact boundaries."
    - "Do not target main."
```
