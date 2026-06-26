# Quality Coverage Baseline And Ratchet Design Contract

## Module

`quality_coverage_baseline_ratchet_design`

Plain English: this contract defines the safe Phase 0 plan for measuring the
current Python coverage baseline and designing later coverage ratchets. A
coverage ratchet is a threshold that should move upward over time after the
repo has evidence that the threshold is fair and useful. Phase 0 is only
measurement and design. It is not CI enforcement.

Coverage is an execution signal: it shows which code paths ran during tests.
Coverage does not prove parser truth, fixture validity, corpus readiness,
security assurance, privacy assurance, release readiness, deploy readiness, or
production behavior.

This contract artifact authorizes only the docs-only design boundary. It does
not implement code, change CI, activate coverage enforcement, run or commit
coverage reports, change parser behavior, promote fixtures, update corpus
metadata, close issues, merge pull requests, or activate tracker #388. Draft PR
submission belongs only to Codex F after review and does not itself authorize
merge, CI enforcement, or runtime behavior.

## Source Issue

- Repository: `Tahjali11/Mythic-Edge`
- Repository URL: `https://github.com/Tahjali11/Mythic-Edge`
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/569
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/566
- Project roadmap: https://github.com/Tahjali11/Mythic-Edge/issues/568
- Active parser evidence tracker:
  https://github.com/Tahjali11/Mythic-Edge/issues/388
- Target artifact:
  `docs/contracts/quality_coverage_baseline_ratchet_design.md`
- Risk tier: High

Observed during contract drafting:

- The primary Mythic Edge checkout was on a gone branch and had unrelated
  governance/doc WIP.
- To preserve unrelated work, this contract was written in a clean sibling
  worktree:
  `codex/quality-coverage-baseline-ratchet-design-569`.
- The sibling worktree was created from `origin/main`.
- `origin/main` was verified at
  `1ad427447c595550c4d9679941e01b371577dab9`.
- Issue #569 was open.
- Tracker #566 was open.
- Project roadmap #568 was open.
- Active parser evidence tracker #388 was open.
- The target contract did not exist before this pass.

Current authorization facts to preserve:

```yaml
implementation_authorized: false
ci_change_authorized: false
coverage_measurement_execution_authorized: false
coverage_report_commit_authorized: false
coverage_enforcement_authorized: false
parser_behavior_change_authorized: false
parser_behavior_ready: false
pipeline_activation_ready_for_issue_388: false
fixture_promotion_authorized: false
corpus_status_change_authorized: false
security_assurance_claim_authorized: false
privacy_assurance_claim_authorized: false
release_readiness_claim_authorized: false
```

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/566

Tracker #566 owns the long-term coverage ratchet and quality-threshold
enforcement roadmap. This contract is the Phase 0 child that defines how to
measure and design safely before any later enforcement work.

## Related Roadmap And Active Lane

- Project roadmap #568 permits read-only measurement and planning before #388
  closes only when it does not mutate repo source, change CI, open broad
  implementation lanes, or interfere with the active WIP slot.
- Active parser evidence tracker #388 remains open and separate. This contract
  does not activate #388, run private harvest, promote fixtures, update corpus
  metadata, or claim parser behavior readiness.

## Source Artifacts Inspected

- GitHub issue #569
- GitHub tracker #566
- GitHub project roadmap #568
- GitHub active parser evidence tracker #388
- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/internal_project_map.md`
- `pyproject.toml`
- `.github/workflows/repo-checks.yml`
- `tools/run_repo_checks.ps1`
- current `tools/` validation-helper inventory
- `.gitignore`

No private `Player.log`, `UTC_Log`, app-data, local runtime artifacts, workbook
exports, SQLite files, secrets, credentials, tokens, API keys, webhook URLs, or
coverage report files were read or imported.

## Owning Layer

Primary owning layer: Quality / Governance.

Coverage measurement and ratchet policy are governance and validation
surfaces. They may observe which code paths test execution touches. They do not
own parser truth, corpus truth, fixture validity, security assurance, privacy
assurance, release readiness, deploy readiness, or production readiness.

## Internal Project Area

Quality / Governance.

This contract reads parser and quality tooling context, but it does not modify
Parser, Corpus / Provenance, Local App / UI, Workbook / Transport, Analytics,
or Future AI Integration behavior.

## Truth Owner

Truth owner for this contract: repo quality governance.

Coverage tools own only coverage measurements for a specific test command,
branch, commit, environment, and configuration. The Python parser/state layer
continues to own parser behavior and parser-owned facts. Corpus / Provenance
continues to own fixture and corpus evidence. Coverage must never be presented
as proof that those upstream truths are correct.

## Bridge-Code Status

`shared_support`

Coverage tooling is shared support for repo quality. It reads test execution
metadata and may later inform CI gates. It must not create a reverse-flow where
coverage results authorize parser behavior changes, fixture promotion, corpus
status changes, or readiness claims.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/quality_coverage_baseline_ratchet_design.md`

Future child issues may separately authorize changes to:

- `pyproject.toml`
- `.github/workflows/repo-checks.yml`
- `tools/run_repo_checks.ps1`
- a future path-group coverage checker under `tools/`
- focused tests for that future checker
- workflow docs or PR templates that describe coverage exceptions

This contract does not authorize changing those files.

## Current Coverage And CI Observations

Current Python coverage configuration in `pyproject.toml`:

- `pytest-cov` is listed in dev dependencies.
- coverage runs with branch coverage enabled.
- coverage source is `src/mythic_edge_parser`.
- coverage report config shows missing lines and skips covered files.

Current GitHub Actions behavior in `.github/workflows/repo-checks.yml`:

- installs the package with dev dependencies;
- runs `py -m pytest -q tests`;
- runs `py tools/check_protected_surfaces.py --base origin/${{ github.base_ref }}`
  for pull requests;
- runs `py -m ruff check src tests tools`;
- does not currently run coverage or enforce a coverage floor.

Current local helper behavior in `tools/run_repo_checks.ps1`:

- default mode runs `py -m pytest -q tests`;
- `-Coverage` mode runs
  `py -m pytest --cov=src/mythic_edge_parser --cov-report=term-missing tests`;
- the helper does not enforce `--cov-fail-under`.

Current `.gitignore` behavior:

- `_review_/` is ignored and is appropriate for local review artifacts;
- `frontend/coverage/` is ignored;
- root `.coverage`, `coverage.xml`, and HTML coverage output are not
  explicitly ignored by name.

## Scope Decision

Phase 0 scope is Python-only coverage measurement design.

Reasons:

- `pyproject.toml` already contains Python coverage configuration.
- repo checks currently run Python tests.
- `tools/run_repo_checks.ps1` already has a non-enforcing Python coverage mode.
- frontend coverage is a separate local-app/UI quality topic and should be
  handled by a later issue if needed.

Phase 0 may define read-only commands and safe output handling. This
docs-only contract package must not run coverage, commit reports, change CI,
add thresholds, or activate enforcement.

## Measurement, Advisory Baseline, And Enforcement Boundary

### Measurement

Measurement means running coverage commands in a clean, known checkout to
observe current values. Measurement may produce local `.coverage`, XML, HTML,
JSON, or terminal output artifacts. These artifacts may contain local paths,
source path details, and command-environment details.

Measurement is allowed only in a later execution issue or by explicit user
approval. This docs-only contract, review, and submission path does not run
measurement.

Measurement must not:

- set `--cov-fail-under`;
- change CI;
- write committed reports;
- infer parser correctness;
- promote fixtures;
- update corpus metadata;
- close #388 or #566;
- claim readiness or assurance.

### Advisory Baseline

Advisory baseline means a later reviewed artifact records sanitized aggregate
coverage values from an approved measurement run. It is guidance, not a gate.

Allowed advisory baseline fields:

- repository and commit;
- branch or source ref;
- command ID;
- test command shape;
- Python version or CI image label if known;
- total coverage percent;
- branch coverage presence;
- file-count summary;
- protected-surface group coverage summaries, if a later checker exists;
- degraded/missing/malformed report status;
- sanitized notes and non-claims.

Forbidden advisory baseline fields:

- raw XML/HTML/JSON report contents;
- raw `.coverage` database;
- local absolute paths;
- user names or home directories;
- raw logs;
- workbook exports;
- secrets or environment values;
- private local artifact paths;
- line-by-line missing coverage copied wholesale from local reports.

Advisory baseline must not fail CI and must not be treated as enforcement.

### Enforcement

Enforcement means CI or local required checks fail when coverage falls below an
accepted threshold. Enforcement is out of scope for Phase 0.

Enforcement requires a later issue, contract, implementation, review,
submitter, and deployer path. It must name:

- exact threshold;
- branch/base used for the accepted baseline;
- command used by local validation and CI;
- exception vocabulary;
- failure behavior;
- rollback or freeze policy;
- protected-surface threshold behavior, if any.

## Safe Measurement Command Design

The commands below are contract design only. Do not run them in Codex B.

All commands must write coverage outputs under ignored `_review_/` or an
external temporary directory. Do not write root `coverage.xml`, root `.coverage`,
or checked-in report directories.

Recommended local macOS/Linux measurement shape:

```bash
RUN_ID="<public-safe-run-id>"
mkdir -p "_review_/quality_coverage_baseline/${RUN_ID}"
COVERAGE_FILE="_review_/quality_coverage_baseline/${RUN_ID}/.coverage" \
  python3 -m pytest -q tests \
    --cov=src/mythic_edge_parser \
    --cov-report=term-missing \
    --cov-report="xml:_review_/quality_coverage_baseline/${RUN_ID}/coverage.xml"
```

Recommended local Windows measurement shape:

```powershell
$RunId = "<public-safe-run-id>"
New-Item -ItemType Directory -Force "_review_/quality_coverage_baseline/$RunId" | Out-Null
$env:COVERAGE_FILE = "_review_/quality_coverage_baseline/$RunId/.coverage"
py -m pytest -q tests `
  --cov=src/mythic_edge_parser `
  --cov-report=term-missing `
  --cov-report="xml:_review_/quality_coverage_baseline/$RunId/coverage.xml"
Remove-Item Env:\COVERAGE_FILE
```

Recommended CI-like measurement design for a later issue:

```powershell
py -m pytest -q tests `
  --cov=src/mythic_edge_parser `
  --cov-report=term-missing `
  --cov-report=xml
```

CI-like measurement must remain advisory until a later enforcement issue adds
an accepted `--cov-fail-under` threshold or protected-surface checker.

## Safe Coverage Output Handling

Coverage output is local/generated until a later contract approves a sanitized
summary.

Allowed local output locations:

- `_review_/quality_coverage_baseline/<public-safe-run-id>/`
- an operating-system temporary directory outside the repo
- CI job artifacts in a later advisory CI workflow, if that workflow is
  explicitly authorized

Forbidden committed output:

- `.coverage`
- `coverage.xml`
- coverage JSON files
- coverage HTML directories
- raw terminal logs from coverage runs
- unredacted file-by-file missing-line reports
- local absolute path lists
- private or generated local artifacts

Allowed public-safe summary content:

- aggregate total coverage;
- branch coverage enabled/disabled label;
- command ID;
- commit SHA;
- sanitized environment label, such as `windows-latest` or `local-macos`;
- repo-relative path group names;
- protected-surface group aggregate percentages, after a later checker exists;
- explicit non-claims.

Coverage summaries must strip or avoid:

- local absolute paths;
- user home directories;
- raw log names;
- secret-like values;
- environment variables;
- private deck names;
- workbook export names;
- generated artifact names.

## Global Floor Ratchet Design

The first enforcement layer is a global coverage floor.

Later global-floor issue requirements:

- measure the baseline on the approved source branch;
- record the measured total coverage in a public-safe advisory artifact;
- propose an initial floor based on measured data, not a guessed vanity number;
- start below or at a conservative accepted value to avoid immediate churn;
- fail closed only after Codex E review and Codex G-approved CI integration;
- require written justification to lower the floor;
- ratchet upward only after cleanup or sustained baseline evidence proves the
  new floor is stable.

Global-floor commands may later use:

```powershell
py -m pytest -q tests --cov=src/mythic_edge_parser --cov-report=term-missing --cov-report=xml --cov-fail-under=<accepted-global-floor>
```

This contract does not set `<accepted-global-floor>`.

## Protected-Surface Ratchet Design

The second enforcement layer is protected-surface coverage.

Candidate protected groups for later design:

- parser truth and state interpretation:
  `src/mythic_edge_parser/app/state.py`,
  `src/mythic_edge_parser/app/models.py`,
  `src/mythic_edge_parser/app/extractors.py`,
  `src/mythic_edge_parser/app/event_identity.py`,
  `src/mythic_edge_parser/router.py`,
  `src/mythic_edge_parser/parsers/`
- evidence ledger and provenance:
  evidence-ledger, golden replay, corpus metadata, drift, and fixture-promotion
  support modules
- EventBus and delivery accounting:
  `src/mythic_edge_parser/event_bus.py` and related delivery/pressure modules
- local API, upload, import, and request guards:
  local-app backend and upload/import safety modules
- privacy redaction and artifact exclusion:
  sanitizers, secret/private-marker scanners, protected-surface checks, local
  environment checks, and report redaction helpers

Later protected-surface checker requirements:

- consume coverage XML or JSON from an approved local/CI measurement command;
- fail closed on missing coverage report;
- fail closed on malformed coverage report;
- fail closed when a configured protected path is absent unexpectedly;
- report only repo-relative paths or symbolic group names;
- keep thresholds versioned and reviewable;
- allow docs-only/generated/fixture/report-only exceptions only through an
  explicit exception vocabulary;
- never treat protected-surface coverage as parser truth, security assurance,
  privacy assurance, or release readiness.

This contract does not implement the checker or set group thresholds.

## New-Code Coverage Expectation Design

The third enforcement layer is a future new-code expectation.

Later new-code policy should require:

- focused tests for new or materially changed protected-surface behavior;
- explicit exception text for untested new code;
- review of whether generated files, docs-only changes, fixtures, deliberate
  report-only lanes, and parked/deferred lanes should be exempt;
- no automatic rejection of legitimate contract-only or docs-only changes;
- no meaningless tests added only to satisfy a number.

The new-code policy must remain subordinate to current issue and contract
scope. It must not force parser behavior changes, fixture promotion, corpus
status changes, or unrelated refactors.

## Exception Vocabulary

Allowed future exception categories:

- `docs_only`
- `contract_only`
- `generated_file`
- `fixture_metadata_only`
- `report_only_boundary`
- `private_evidence_blocked`
- `external_boundary_blocked`
- `deferred_lane`
- `parked_lane`
- `legacy_bridge_pending_contract`
- `tooling_bootstrap`
- `human_approved_temporary_exception`

Exception rules:

- Every exception must name the issue or PR that approved it.
- Every exception must name its expiration condition.
- Every exception must explain whether it affects global floor,
  protected-surface floor, new-code expectation, or all three.
- Exceptions must not hide raw/private artifacts, secrets, parser truth gaps,
  or readiness claims.

## Error Behavior

Future coverage measurement or enforcement tooling must fail closed when:

- coverage output is missing;
- coverage output is malformed;
- coverage output was produced from the wrong branch or commit;
- report paths include local absolute paths in a public artifact;
- a configured protected-surface group has no matched files unexpectedly;
- a threshold is missing in enforcement mode;
- a threshold is non-numeric or out of range;
- an exception has no issue/PR reference or expiration condition;
- a report contains raw logs, workbook exports, secrets, private paths, or
  generated private artifacts.

In Phase 0, failure behavior is advisory only: record the reason and stop. Do
not patch CI, lower gates, or infer readiness.

## Side Effects

This contract-writing scope may write:

- `docs/contracts/quality_coverage_baseline_ratchet_design.md`

This contract-writing and review scope must not:

- run coverage;
- write coverage output;
- commit coverage reports;
- change CI;
- change `pyproject.toml`;
- change `tools/run_repo_checks.ps1`;
- create custom coverage checkers;
- close issues or trackers;
- change parser behavior;
- change fixture or corpus metadata;
- update GitHub Actions.

Draft PR submission is allowed only in the Codex F submitter role after review
has no blocking findings. A draft PR does not authorize merge, issue closure,
tracker completion, CI changes, coverage enforcement, or any runtime behavior.

Future measurement passes may write local ignored artifacts under `_review_/`
only when explicitly authorized.

## Dependency Order For Later Work

1. Phase 0: contract-only design in this artifact.
2. Phase 1: explicit read-only measurement issue; run coverage locally or in an
   advisory environment; keep raw reports local; record sanitized aggregate
   baseline only.
3. Phase 2: global-floor contract; choose first accepted floor from measured
   baseline; define exceptions.
4. Phase 3: global-floor implementation; update local validation and CI only
   after review.
5. Phase 4: protected-surface group contract; define path groups and
   thresholds.
6. Phase 5: protected-surface checker implementation and tests.
7. Phase 6: new-code coverage expectation policy.
8. Phase 7: ratchet raise/freeze/lower policy after enough evidence exists.

## Compatibility

Existing behavior must remain valid:

- `py -m pytest -q tests` remains the current CI test command until a later
  issue changes CI.
- `py -m ruff check src tests tools` remains the current CI lint command.
- `tools/run_repo_checks.ps1 -Coverage` remains a non-enforcing local helper.
- `pyproject.toml` coverage config remains advisory configuration until a
  later issue changes enforcement.

## Tests And Validation Required

This docs-only contract package requires validation:

```bash
printf '%s\n' docs/contracts/quality_coverage_baseline_ratchet_design.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' docs/contracts/quality_coverage_baseline_ratchet_design.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
git diff --check
```

Because this is a new untracked file, also validate whitespace with:

```bash
git diff --check --no-index /dev/null docs/contracts/quality_coverage_baseline_ratchet_design.md
```

Do not run coverage for this docs-only contract, review, or submission package.

Later measurement validation should include:

- clean checkout or clean sibling worktree status;
- exact commit SHA;
- exact command line;
- confirmation raw reports stayed local/ignored;
- sanitized aggregate summary only;
- secret/private-marker scan for any public artifact.

Later enforcement implementation validation should include:

- focused tests for any new checker;
- passing and failing global-floor cases;
- passing and failing protected-surface group cases;
- missing coverage report;
- malformed coverage report;
- docs-only/contract-only exception behavior;
- generated/fixture/report-only exception behavior;
- `git diff --check`;
- protected-surface and secret/private-marker scans.

## Acceptance Criteria

- The contract distinguishes measurement, advisory baseline, and enforcement.
- The contract explains why Phase 0 permits read-only planning but not CI
  changes.
- The contract defines safe local coverage output handling.
- The contract keeps raw coverage reports out of Git.
- The contract selects Python-only Phase 0 scope and defers frontend coverage.
- The contract defines later global-floor ratchet design.
- The contract defines later protected-surface ratchet design.
- The contract defines later new-code expectation design.
- The contract preserves #388 as active and separate.
- The contract makes no parser truth, fixture-promotion, corpus-readiness,
  release-readiness, security-assurance, or privacy-assurance claims.

## Non-Claims

This contract does not claim:

- parser truth;
- parser behavior readiness;
- tracker #388 activation readiness;
- fixture promotion readiness;
- corpus readiness;
- private smoke success;
- security assurance;
- privacy assurance;
- release readiness;
- deploy readiness;
- production readiness;
- analytics truth;
- AI truth;
- coaching truth.

## Remaining Risks

- The actual baseline is not measured in this docs-only contract package.
- The first accepted global floor is not selected in this contract.
- Protected-surface path groups are proposed but not finalized.
- Frontend coverage remains out of scope.
- CI remains unchanged.
- Existing local helper coverage mode remains non-enforcing.

## Next Workflow Action

Recommended next role: Codex E, Module Reviewer / Contract Tester.

Pasteable prompt:

```text
Use the Mythic Edge workflow rules.

Act as Codex E: Module Reviewer for issue #569.

Repository:
Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/569

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/566

Project roadmap:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Active parser evidence tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/388

Contract artifact:
docs/contracts/quality_coverage_baseline_ratchet_design.md

Review goal:
Review the Phase 0 coverage baseline measurement and ratchet design contract.
Lead with findings. Verify that it distinguishes measurement, advisory
baseline, and enforcement; keeps coverage output public-safe; designs later
global-floor and protected-surface ratchets; and does not authorize code,
CI changes, coverage enforcement, coverage report commits, parser behavior
changes, fixture promotion, corpus readiness, release readiness, security
assurance, or privacy assurance.

Expected output:
- Findings first, ordered by severity.
- Validation reviewed.
- Verdict: ready for Codex F, route back to Codex B, or route to Codex A if
  scope is wrong.
- workflow_handoff block.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/569"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/566"
  project_roadmap: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  active_parser_evidence_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  completed_thread: "B"
  next_thread: "E"
  verdict: "quality_coverage_baseline_ratchet_design_contract_ready_for_review"
  risk_tier: "High"
  base_branch: "main"
  target_branch: "main"
  branch: "codex/quality-coverage-baseline-ratchet-design-569"
  source_artifact: "GitHub issue #569"
  target_artifact: "docs/contracts/quality_coverage_baseline_ratchet_design.md"
  implementation_authorized: false
  ci_change_authorized: false
  coverage_measurement_execution_authorized: false
  coverage_report_commit_authorized: false
  coverage_enforcement_authorized: false
  parser_behavior_change_authorized: false
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  validation:
    - "printf '%s\\n' docs/contracts/quality_coverage_baseline_ratchet_design.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin"
    - "printf '%s\\n' docs/contracts/quality_coverage_baseline_ratchet_design.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin"
    - "git diff --check"
    - "git diff --check --no-index /dev/null docs/contracts/quality_coverage_baseline_ratchet_design.md"
  stop_conditions:
    - "Do not implement code."
    - "Do not open a PR before review has no blocking findings."
    - "Do not change CI."
    - "Do not activate coverage enforcement."
    - "Do not run or commit coverage reports."
    - "Do not change parser behavior."
    - "Do not claim parser truth, fixture promotion, corpus readiness, release readiness, security assurance, or privacy assurance."
```
