# Engineering Maturity Baseline Audit

## Findings

### P1: `private_local_v1` is not ready until clean-install/local-run proof is completed

The repo has strong source, tests, launcher, frontend, and local-artifact
evidence, but the active release profile requires proof that the project can be
installed and run from a clean checkout without relying on this working
machine's accumulated state. Current evidence shows `clean_clone` and
`clean_install_transition_audit` reports with warnings, including untracked
worktree state and `.env*` ignore-coverage uncertainty. The roadmap also places
live Player.log mode and professional polish after the current local-app and
analytics foundation work.

This blocks a private-local-v1 readiness decision, not continued feature work.

### P1: All-repo secret/private-marker debt prevents claiming release-grade private artifact safety

Path-scoped checks for current reviewed work are routinely clean, but the
all-repo advisory scan currently reports `forbidden: 540` and `warnings: 898`.
That does not prove this audit introduced leakage; it does mean the maturity
baseline cannot score private artifact safety as "hard to break quietly" until
the repo-wide findings are triaged, suppressed with policy, or fixed.

This is a private-local-v1 blocker because the selected profile emphasizes safe
local use with raw logs, generated outputs, local app state, and credentials
kept out of source control.

### P2: Pyright remains correctly advisory, but type discipline is not mature

`tools/run_pyright_advisory_report.py --format json` returned
`status: advisory_findings`, `gate_behavior: advisory_non_blocking`, and
`type_findings: 253`. That is contract-compliant because Pyright is not a
required gate, but it keeps type safety below release-proven maturity.

This is not a private-local-v1 blocker by itself.

### P2: Documentation and onboarding lag behind the current local-app workflow

`README.md` still describes the older parser/Google Sheets oriented pipeline and
mentions a four-thread Codex workflow, while current authority docs use the A-G
workflow and the roadmap now centers local app, manual import, analytics views,
Match Journal, and live-mode readiness. The project has many durable artifacts,
but a human setup/readiness path still depends on knowing where to look.

This is not necessarily a private-local-v1 blocker for the current user, but it
blocks shared-with-developer readiness and contributes to clean-install risk.

### P3: Authorized blocker remediation issues were created after baseline rerun

After explicit user authorization, the audit created GitHub remediation issues
only for under-5 rows where `should_create_now: yes` and
`release_profile_blocker: private_local_v1`.

Created issues:

- #251: `[release] Prove private-local-v1 local app startup and status smoke`
- #252: `[quality] Triage private-local-v1 private artifact scanner and env ignore posture`
- #253: `[release] Prove private-local-v1 clean checkout install and launch path`

Deferred and non-blocking under-5 rows remain drafted in this report only.

## Role Performed

Codex E: Governance Reviewer / Baseline Auditor.

## Issue / Tracker / Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/249
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/136
- Source issue: https://github.com/Tahjali11/Mythic-Edge/issues/248

## Selected Release Profile

`private_local_v1`

## Contract Reviewed

`docs/contracts/engineering_maturity_index_open_framework.md`

Contract status: present and tracked on the current branch.

## Files, Docs, And Issues Reviewed

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/templates/contract_test_report.md`
- `docs/contracts/engineering_maturity_index_open_framework.md`
- `docs/project_roadmap.md`
- `docs/internal_project_map.md`
- `docs/local_artifacts_manifest.json`
- `README.md`
- `pyproject.toml`
- `.github/workflows/repo-checks.yml`
- `frontend/package.json`
- `tools/select_validation.py`
- `tools/run_repo_checks.ps1`
- `tools/check_local_environment.py`
- `tools/check_protected_surfaces.py`
- `tools/check_secret_patterns.py`
- `tools/run_pyright_advisory_report.py`
- accepted ADRs under `docs/decisions/ADR-*.md`
- contract, handoff, and report inventories under `docs/contracts/`,
  `docs/implementation_handoffs/`, and `docs/contract_test_reports/`
- focused parser, evidence, analytics, local app, governance, and hardening
  test file inventory under `tests/`
- GitHub issues #136, #248, #249
- Current open PR list

## Baseline Summary

No composite score is used. The primary output is category score, confidence,
private-local-v1 blocker status, and path-to-5 plan.

| # | Category | Status | Score | Confidence | Private Local V1 Blocker |
| --- | --- | --- | --- | --- | --- |
| 1 | Architecture and truth ownership | scored | 4 | high | no |
| 2 | Parser correctness and evidence | scored | 4 | high | no |
| 3 | Test and corpus coverage | scored | 4 | high | no |
| 4 | Local app runtime and usability | scored | 3 | medium | yes |
| 5 | Security and private artifact safety | scored | 3 | medium | yes |
| 6 | Delivery workflow and release readiness | scored | 4 | high | no |
| 7 | Installability and operational portability | scored | 3 | medium | yes |
| 8 | Supply-chain and repo hygiene | scored | 3 | medium | no |
| 9 | Documentation and onboarding | scored | 3 | medium | no |
| 10 | Analytics readiness | scored | 4 | medium | no |
| 11 | Future AI integration readiness | intentionally_deferred | N/A | high | deferred |

## Baseline Rows

### 1. Architecture And Truth Ownership

- category: Architecture and truth ownership
- status: `scored`
- score: `4`
- score_confidence: `high`
- scored_measures:
  - `Parser truth remains upstream of workbook, analytics, UI, and AI (arc42/Q42; CHAOSS)`
  - `Internal project ownership is documented without forcing premature repo splits (arc42/Q42; CHAOSS)`
  - `Protected surfaces require explicit issue and contract authorization (arc42/Q42; CHAOSS)`
- open_public_reference_inspiration: arc42/Q42, CHAOSS.
- objective_evidence:
  - `AGENTS.md`, `docs/agent_rules.yml`, and
    `docs/agent_constitution.md` define authority order, truth ownership, and
    protected surfaces.
  - ADR-0001 through ADR-0006 are accepted.
  - `docs/internal_project_map.md` documents internal project ownership and
    bridge-code classifications.
  - Protected-surface tooling exists and passed for current tracked diff:
    `forbidden: 0`, `warnings: 0`.
- subjective_rationale: For `private_local_v1`, architecture is unusually clear
  for a personal repo. The remaining risk is not conceptual truth ownership; it
  is enforcement and stale-doc alignment.
- why_not_higher: The map intentionally preserves a flat source layout and
  still marks some support modules as ambiguous or provisional. Boundary rules
  are workflow/tooling backed but not release-proven over a completed v1 cycle.
- v1_0_blocker: `no`
- release_profile_relevance: High for `private_local_v1`.
- next_action:
  - Keep ADR-0006 and `docs/internal_project_map.md` cited in future
    cross-boundary work.
  - Resolve or deliberately defer ambiguous shared-support modules before
    public or shared-developer release.
  - Link architecture map from onboarding docs after review.
- related_issues_contracts_tests: issues #215, #217, #218; ADR-0001, ADR-0004,
  ADR-0006; `docs/internal_project_map.md`; `tools/check_protected_surfaces.py`.
- remediation_plan:
  - current_score: `4`
  - target_score_for_active_release_profile: `4`
  - path_to_5: complete one private-local-v1 readiness cycle without boundary
    drift, then add an architecture index or README pointer that lets a fresh
    thread find the map without chat context.
  - recommended_issue_count: `1`
  - proposed_issue_titles:
    - `[quality] Link internal project map from onboarding and release-readiness docs`
  - proposed_issue_bodies_or_acceptance_criteria:
    - Add a docs-only pointer to `docs/internal_project_map.md`.
    - Do not move files, rename packages, or enforce import rules.
    - Validate with `git diff --check`, `py tools/check_agent_docs.py`, and
      path-scoped protected/secret scans.
  - internal_project_area: Quality / Governance
  - priority: medium
  - release_profile_blocker: `no`
  - should_create_now: `deferred`
  - deferral_reason: Not required before private-local-v1 if current workflow
    prompts continue to cite the map.
  - related_contracts_tests_tools_or_issues: `docs/internal_project_map.md`,
    ADR-0006, issue #218.

### 2. Parser Correctness And Evidence

- category: Parser correctness and evidence
- status: `scored`
- score: `4`
- score_confidence: `high`
- scored_measures:
  - `Parser-managed match/game facts are verified at the parser/state layer (arc42/Q42; DORA)`
  - `Player.log drift and degraded evidence are surfaced without guessing (arc42/Q42)`
  - `Evidence provenance remains downstream support, not a second parser (arc42/Q42; CHAOSS)`
- open_public_reference_inspiration: arc42/Q42, DORA.
- objective_evidence:
  - Parser contracts and reports exist for state, models, outputs, runner,
    event identity, GRE parsers, draft parsers, diagnostics, and golden replay.
  - Evidence-ledger contracts and reports cover tiers, runtime status, field
    evidence, schema snapshots, drift reports, and validation wiring.
  - Current full Python suite passed: `1653 passed, 1 skipped, 1 warning`.
  - Related parser/evidence tests exist, including `test_state.py`,
    `test_app_models.py`, `test_event_schema_snapshots.py`,
    `test_parser_regressions.py`, `test_golden_replay_harness.py`,
    `test_log_drift_sensor.py`, and evidence-ledger tests.
- subjective_rationale: For `private_local_v1`, parser correctness evidence is
  strong enough to keep analytics and local app work downstream. Remaining
  uncertainty is mainly live-log and corpus breadth, not absence of parser
  ownership.
- why_not_higher: Live Player.log behavior, broader corpus coverage, and real
  private-log drift scenarios are not release-proven in this baseline.
- v1_0_blocker: `no`
- release_profile_relevance: Critical for `private_local_v1`.
- next_action:
  - Keep parser/evidence regressions in the private-local-v1 readiness packet.
  - Preserve live-mode stop conditions around raw Player.log access.
  - Expand corpus only through sanitized or approved fixture policy.
- related_issues_contracts_tests: parser contracts/reports, Player.log evidence
  ledger contracts/reports, `tests/test_parser_regressions.py`,
  `tests/test_event_schema_snapshots.py`, `tests/test_golden_replay_harness.py`.
- remediation_plan:
  - current_score: `4`
  - target_score_for_active_release_profile: `4`
  - path_to_5: prove parser/evidence behavior through a completed live or
    release-profile validation cycle with no silent drift and with documented
    recovery from degraded evidence.
  - recommended_issue_count: `1`
  - proposed_issue_titles:
    - `[parser] Prove private-local-v1 parser/evidence readiness packet`
  - proposed_issue_bodies_or_acceptance_criteria:
    - Run focused parser, evidence, golden replay, drift, and schema snapshot
      suites.
    - Record remaining corpus gaps and non-live assumptions.
    - Do not change parser behavior in the readiness packet.
  - internal_project_area: Parser / Corpus / Provenance
  - priority: medium
  - release_profile_blocker: `no`
  - should_create_now: `deferred`
  - deferral_reason: Existing tests pass; bundle into the final v1 readiness
    packet rather than creating a standalone fix issue now.
  - related_contracts_tests_tools_or_issues: parser reports, evidence-ledger
    reports, `tools/select_validation.py`.

### 3. Test And Corpus Coverage

- category: Test and corpus coverage
- status: `scored`
- score: `4`
- score_confidence: `high`
- scored_measures:
  - `Critical parser and analytics behaviors have focused regression coverage (arc42/Q42; CHAOSS)`
  - `Golden fixture and corpus gaps are explicit rather than invisible (CHAOSS; arc42/Q42)`
  - `Schema and snapshot tests protect important row and payload shapes (arc42/Q42; DORA)`
- open_public_reference_inspiration: arc42/Q42, CHAOSS.
- objective_evidence:
  - Inventory found 106 Python test files and 21 fixture files.
  - Full Python suite passed with 1653 passing tests.
  - Frontend Vitest suite passed with 68 tests.
  - Schema snapshot, golden replay, drift sensor, parser regression, analytics,
    local app, Match Journal, and validation-tool tests are present.
  - Golden fixture, drift baseline, parser feature-equity, and validation
    selector contract reports exist.
- subjective_rationale: Coverage breadth is a major strength. The project has
  a meaningful mix of unit, contract, schema, snapshot, replay, fixture, and
  tool tests.
- why_not_higher: Coverage still depends on selected sanitized fixtures and
  focused corpora. Real live Player.log and broad property/fuzz coverage are
  not release-proven.
- v1_0_blocker: `no`
- release_profile_relevance: High for `private_local_v1`.
- next_action:
  - Keep full suite plus focused suites in release-readiness evidence.
  - Track fixture/corpus gaps as follow-ups, not hidden risks.
  - Avoid auto-updating snapshots without contract authority.
- related_issues_contracts_tests: `tests/`, `tests/fixtures/`,
  `docs/contracts/code_hardening_golden_fixture_policy.md`,
  `docs/contracts/parser_feature_equity_corpus_ratchet.md`,
  `docs/contracts/repo_wide_workbook_webhook_schema_snapshots.md`.
- remediation_plan:
  - current_score: `4`
  - target_score_for_active_release_profile: `4`
  - path_to_5: complete a release-profile corpus packet that proves fixture
    relevance, live-mode diagnostic coverage, and no silent schema drift.
  - recommended_issue_count: `1`
  - proposed_issue_titles:
    - `[quality] Define private-local-v1 corpus and fixture readiness packet`
  - proposed_issue_bodies_or_acceptance_criteria:
    - List required parser, golden, drift, schema, and analytics fixtures.
    - Identify intentionally deferred live/private fixture gaps.
    - Validate with focused tests and snapshot checks.
  - internal_project_area: Corpus / Provenance
  - priority: medium
  - release_profile_blocker: `no`
  - should_create_now: `deferred`
  - deferral_reason: Existing coverage passes; release packet can group this
    with parser readiness.
  - related_contracts_tests_tools_or_issues: fixture policy and corpus ratchet
    contracts.

### 4. Local App Runtime And Usability

- category: Local app runtime and usability
- status: `scored`
- score: `3`
- score_confidence: `medium`
- scored_measures:
  - `Local app launch and setup status are reproducible enough for the active release profile (arc42/Q42; DORA)`
  - `Operator-facing diagnostics reduce guesswork without exposing private artifacts (arc42/Q42; SPACE)`
  - `Local app UI remains an access surface, not parser or analytics truth (arc42/Q42; SPACE)`
- open_public_reference_inspiration: arc42/Q42, SPACE, DORA.
- objective_evidence:
  - Local app backend, config, setup-status, manual import, upload, analytics
    views, Match Journal, live status, watcher process, diagnostics, and live
    SQLite capture contracts/reports exist.
  - Frontend tests passed: 68 tests.
  - Frontend typecheck passed.
  - Frontend build passed; generated `frontend/dist` was removed afterward.
  - Local app and frontend packages are present in repo-owned source.
- subjective_rationale: The app is clearly beyond prototype, but still has
  active live-mode and real-app-data readiness work. For `private_local_v1`,
  the user needs the app to start and explain status reliably in the actual
  local context, not just in synthetic tests.
- why_not_higher: Live Player.log mode is still being built, real local app
  operation against the actual app-data root is not proven in this audit, and
  browser/live smoke evidence is not yet a final readiness packet.
- v1_0_blocker: `yes`
- release_profile_relevance: Critical for `private_local_v1`.
- next_action:
  - Complete a private-local-v1 local-app readiness smoke packet.
  - Include backend health, frontend render, setup status, import path,
    analytics views, Match Journal status, and live watcher metadata status.
  - Keep destructive controls and raw/private display out of scope.
- related_issues_contracts_tests: issues #204 and #207, local app contracts and
  reports, `tests/test_analytics_local_app_backend.py`,
  `frontend/src/*.test.tsx`.
- remediation_plan:
  - current_score: `3`
  - target_score_for_active_release_profile: `4`
  - path_to_5: first prove deterministic local startup and safe status display
    in a private-local-v1 smoke packet; later prove repeated real use without
    silent regressions.
  - recommended_issue_count: `1`
  - proposed_issue_titles:
    - `[release] Prove private-local-v1 local app startup and status smoke`
  - proposed_issue_bodies_or_acceptance_criteria:
    - Start backend/frontend through approved launcher or documented commands.
    - Verify setup/status, import status, analytics views, Match Journal status,
      and live watcher readiness without reading raw private logs.
    - Confirm no generated artifacts are committed.
  - internal_project_area: Local App / UI
  - priority: high
  - release_profile_blocker: `private_local_v1`
  - should_create_now: `yes`
  - deferral_reason: `N/A`
  - related_contracts_tests_tools_or_issues: issues #204, #207, live-app and
    analytics local-app reports.

### 5. Security And Private Artifact Safety

- category: Security and private artifact safety
- status: `scored`
- score: `3`
- score_confidence: `medium`
- scored_measures:
  - `Secret/private artifact scanning exists and is routinely used (OWASP SAMM; NIST SSDF; OpenSSF Scorecard)`
  - `Raw Player.log, private JSONL, generated SQLite, runtime artifact, and secret boundaries are documented (OWASP SAMM; NIST SSDF)`
  - `Local app responses avoid private path, raw payload, raw hash, SQL, stack trace, and secret exposure (arc42/Q42; OWASP SAMM; NIST SSDF)`
- open_public_reference_inspiration: OWASP SAMM, NIST SSDF, OpenSSF Scorecard,
  arc42/Q42.
- objective_evidence:
  - `tools/check_secret_patterns.py`, `tools/check_protected_surfaces.py`, and
    related tests exist.
  - `docs/local_artifacts_manifest.json` defines clean-clone, local developer
    app, analytics, live parser, historical import, and clean-install
    transition profiles.
  - Path-scoped scans are routinely used and current tracked diff protected
    surface check passed.
  - All-repo advisory secret/private-marker scan currently reports
    `forbidden: 540`, `warnings: 898`.
  - Clean-clone local environment report status is `warning`, with `.env*`
    ignore-coverage uncertainty.
- subjective_rationale: The safety process is strong, but private-local-v1
  cannot claim release-grade safety while all-repo scanner debt and env ignore
  uncertainty remain unresolved.
- why_not_higher: The scanner tooling exists, but the repo-wide result is not
  clean or fully triaged; `.env*` coverage is not confirmed; and live/private
  local behavior has not completed the release-profile packet.
- v1_0_blocker: `yes`
- release_profile_relevance: Critical for `private_local_v1`.
- next_action:
  - Triage all-repo scanner findings into policy text, expected fixture
    markers, or concrete fixes.
  - Resolve `.env*` ignore-coverage uncertainty.
  - Define required private-local-v1 secret/protected-surface checks.
- related_issues_contracts_tests: `docs/contracts/local_artifact_manifest_environment_profiles.md`,
  `docs/contracts/pre_v1_clean_install_transition.md`,
  `tools/check_secret_patterns.py`, `tools/check_protected_surfaces.py`,
  `tests/test_check_secret_patterns.py`, `tests/test_check_local_environment.py`.
- remediation_plan:
  - current_score: `3`
  - target_score_for_active_release_profile: `4`
  - path_to_5: get private-local-v1 scanner posture to "path-scoped clean plus
    all-repo findings triaged", then prove repeated release use with no
    private artifact regressions.
  - recommended_issue_count: `2`
  - proposed_issue_titles:
    - `[quality] Triage all-repo secret/private-marker scanner findings for private-local-v1`
    - `[quality] Resolve .env ignore-coverage uncertainty in local artifact checks`
  - proposed_issue_bodies_or_acceptance_criteria:
    - Classify existing all-repo findings as expected policy/fixture markers,
      suppressible scanner false positives, or real fixes.
    - Do not weaken scanner coverage.
    - Confirm `.env*` behavior without printing secret values.
  - internal_project_area: Quality / Governance / Generated / Local Artifacts
  - priority: high
  - release_profile_blocker: `private_local_v1`
  - should_create_now: `yes`
  - deferral_reason: `N/A`
  - related_contracts_tests_tools_or_issues: local artifact and secret scanner
    contracts/reports.

### 6. Delivery Workflow And Release Readiness

- category: Delivery workflow and release readiness
- status: `scored`
- score: `4`
- score_confidence: `high`
- scored_measures:
  - `Release recovery clarity is visible in issues, handoffs, and validation reports (DORA; SPACE)`
  - `Validation routing is deterministic without becoming a second authority (DORA; CHAOSS)`
  - `A-G workflow artifacts preserve review and submitter boundaries (SPACE; CHAOSS)`
- open_public_reference_inspiration: DORA, SPACE, CHAOSS.
- objective_evidence:
  - A-G workflow authority is documented in `AGENTS.md`,
    `docs/agent_rules.yml`, `docs/agent_constitution.md`, and
    `docs/codex_module_workflow.md`.
  - There are 126 contract files, 144 implementation handoffs, and 116
    contract-test reports.
  - `tools/select_validation.py` maps changed paths to focused checks.
  - `.github/workflows/repo-checks.yml` runs tests, Ruff, and protected-surface
    gate for PRs.
  - Current open PR list is empty.
  - Current branch is aligned with origin by count: `0 0`.
- subjective_rationale: Workflow maturity is strong. The repo has a durable
  operating system for Codex work, and handoffs are more reliable than chat
  memory.
- why_not_higher: There is not yet a private-local-v1 release-readiness packet,
  this rerun still needs Codex F submission, and CI is not a full substitute for
  local frontend/build/secret evidence.
- v1_0_blocker: `no`
- release_profile_relevance: High for `private_local_v1`.
- next_action:
  - Route this baseline to Codex F after validation.
  - Keep issue #136 open until baseline and prioritized follow-ups are durable.
  - Add a release-readiness packet before private-local-v1 decision.
- related_issues_contracts_tests: `docs/codex_module_workflow.md`,
  `tools/select_validation.py`, `.github/workflows/repo-checks.yml`,
  issue #136.
- remediation_plan:
  - current_score: `4`
  - target_score_for_active_release_profile: `4`
  - path_to_5: complete one private-local-v1 release cycle with reviewed PR,
    recorded validation, known residual risks, and issue/tracker closure.
  - recommended_issue_count: `1`
  - proposed_issue_titles:
    - `[release] Create private-local-v1 release-readiness packet`
  - proposed_issue_bodies_or_acceptance_criteria:
    - Summarize branch/PR state, tests, frontend checks, local artifact status,
      scanner status, Pyright advisory status, and unresolved blockers.
    - Do not mark release ready while P1 findings remain open.
  - internal_project_area: Quality / Governance
  - priority: high
  - release_profile_blocker: `no`
  - should_create_now: `deferred`
  - deferral_reason: Create after P1 local app/install/safety gaps are routed.
  - related_contracts_tests_tools_or_issues: issue #136, this baseline.

### 7. Installability And Operational Portability

- category: Installability and operational portability
- status: `scored`
- score: `3`
- score_confidence: `medium`
- scored_measures:
  - `Clean checkout setup is reproducible for the active release profile (arc42/Q42; DORA)`
  - `Generated app-data folders are separated from repo files (arc42/Q42; OpenSSF Scorecard)`
  - `Launcher and dependency metadata are present but not release-proven on a clean machine (DORA; SPACE; OpenSSF Scorecard)`
- open_public_reference_inspiration: arc42/Q42, DORA, OpenSSF Scorecard, SPACE.
- objective_evidence:
  - `pyproject.toml` defines package metadata, app extras, dev extras, and
    package data for analytics and Match Journal migrations.
  - `frontend/package.json` and lockfile-backed frontend dependencies are
    present.
  - Local environment checker profiles exist and ran without reading private
    contents.
  - `clean_clone` report status is `warning`: 27 checks, 0 blocked, 0 errors,
    8 warnings.
  - `clean_install_transition_audit` status is `warning`: 33 checks, 0 blocked,
    0 errors, 3 warnings.
  - Frontend build passed.
- subjective_rationale: The project is installable on the current machine and
  has a credible clean-install transition model, but the selected profile needs
  proof from a clean checkout or explicitly controlled local setup.
- why_not_higher: Clean install/fresh machine proof is not complete; local
  environment reports still warn; and generated local app state exists outside
  source control as expected but is not release-cycle proven.
- v1_0_blocker: `yes`
- release_profile_relevance: Critical for `private_local_v1`.
- next_action:
  - Run and record a clean checkout install/startup proof.
  - Resolve or intentionally accept local environment warnings.
  - Keep generated app-data and build outputs out of Git.
- related_issues_contracts_tests: issue #227, issue #153,
  `docs/contracts/pre_v1_clean_install_transition.md`,
  `docs/contract_test_reports/pre_v1_clean_install_transition.md`,
  `tools/check_local_environment.py`.
- remediation_plan:
  - current_score: `3`
  - target_score_for_active_release_profile: `4`
  - path_to_5: prove clean checkout setup, local app launch, backend/frontend
    health, generated app-data handling, and validation commands from a clean
    state; repeat before any public release.
  - recommended_issue_count: `1`
  - proposed_issue_titles:
    - `[release] Prove private-local-v1 clean checkout install and launch path`
  - proposed_issue_bodies_or_acceptance_criteria:
    - Install Python dev/app dependencies from `pyproject.toml`.
    - Install frontend dependencies from `frontend/package-lock.json`.
    - Run backend/frontend health checks and local environment profiles.
    - Confirm generated outputs are ignored/absent from Git.
  - internal_project_area: Quality / Governance / Local App / UI
  - priority: high
  - release_profile_blocker: `private_local_v1`
  - should_create_now: `yes`
  - deferral_reason: `N/A`
  - related_contracts_tests_tools_or_issues: local artifact and clean-install
    contracts/reports.

### 8. Supply-Chain And Repo Hygiene

- category: Supply-chain and repo hygiene
- status: `scored`
- score: `3`
- score_confidence: `medium`
- scored_measures:
  - `Dependency and generated-artifact hygiene are visible in repo-owned tooling (NIST SSDF; OpenSSF Scorecard)`
  - `Build/release provenance expectations are appropriate to the release profile (SLSA; OpenSSF Scorecard)`
  - `CI and local validation are documented without overstating public-release controls (OpenSSF Scorecard; NIST SSDF)`
- open_public_reference_inspiration: OpenSSF Scorecard, SLSA, NIST SSDF.
- objective_evidence:
  - Python dependencies and optional app/dev extras are declared in
    `pyproject.toml`.
  - Frontend dependencies are declared in `frontend/package.json`.
  - `.github/workflows/repo-checks.yml` runs Python tests and Ruff and runs
    protected-surface gate on PRs.
  - Generated artifact families are documented in `.gitignore` and
    `docs/local_artifacts_manifest.json`.
  - Pyright advisory report exists and is non-gating.
- subjective_rationale: Repo hygiene is solid for private local work, but not
  mature enough for public release or supply-chain claims.
- why_not_higher: Python dependency locking/version policy is limited, Pyright
  has advisory findings, all-repo secret scan debt remains, CI does not include
  every local/frontend/privacy check, and no build provenance/attestation is
  expected for private-local-v1.
- v1_0_blocker: `no`
- release_profile_relevance: Medium for `private_local_v1`, higher for public
  release.
- next_action:
  - Keep supply-chain expectations scoped to private-local-v1.
  - Decide whether any frontend or secret checks should become release-packet
    requirements rather than CI gates.
  - Defer SLSA/OpenSSF public-release work.
- related_issues_contracts_tests: `pyproject.toml`, `frontend/package.json`,
  `.github/workflows/repo-checks.yml`, Pyright advisory reports, validation
  selector reports.
- remediation_plan:
  - current_score: `3`
  - target_score_for_active_release_profile: `3`
  - path_to_5: define dependency lock/version policy, broaden CI or release
    packet checks intentionally, and reserve provenance controls for public
    release.
  - recommended_issue_count: `1`
  - proposed_issue_titles:
    - `[quality] Define private-local-v1 dependency and validation packet policy`
  - proposed_issue_bodies_or_acceptance_criteria:
    - Decide which frontend, secret, Pyright advisory, and local environment
      checks belong in release packets versus CI.
    - Do not create new gates without contract approval.
  - internal_project_area: Quality / Governance
  - priority: medium
  - release_profile_blocker: `no`
  - should_create_now: `deferred`
  - deferral_reason: P1 install and private-artifact work should go first.
  - related_contracts_tests_tools_or_issues: validation matrix and Pyright
    advisory contracts.

### 9. Documentation And Onboarding

- category: Documentation and onboarding
- status: `scored`
- score: `3`
- score_confidence: `medium`
- scored_measures:
  - `Onboarding docs explain current setup and project authority without relying on chat memory (arc42/Q42; CHAOSS)`
  - `Handoff artifacts reduce restart cost for future threads (SPACE; CHAOSS)`
  - `Beginner-friendly docs preserve technical truth ownership (arc42/Q42; SPACE)`
- open_public_reference_inspiration: arc42/Q42, CHAOSS, SPACE.
- objective_evidence:
  - `README.md`, `docs/project_roadmap.md`, authority docs, role docs,
    templates, ADRs, contracts, handoffs, and reports exist.
  - Agent docs checker passed: 46 files, errors 0, warnings 0.
  - The roadmap is current enough to name local app, manual import, analytics,
    Match Journal, live mode, professional discipline, and AI as separate
    phases.
- subjective_rationale: Codex onboarding is very strong; human setup
  documentation is less current than the actual local app and analytics work.
- why_not_higher: README still emphasizes the older parser/Sheets flow and
  mentions a four-thread workflow, while current governance uses A-G and the
  roadmap has moved into local app/analytics/live-mode work. Clean-install
  setup docs are not release-proven.
- v1_0_blocker: `no`
- release_profile_relevance: Medium for `private_local_v1`, high for
  `shared_with_developer_v1`.
- next_action:
  - Update README only after the private-local-v1 run path is proven.
  - Add a minimal "how to run the local app" section.
  - Keep parser truth model visible.
- related_issues_contracts_tests: `README.md`, `docs/project_roadmap.md`,
  authority docs, issue #155.
- remediation_plan:
  - current_score: `3`
  - target_score_for_active_release_profile: `3`
  - path_to_5: after clean-install proof, update README/onboarding to match the
    actual local app path, validation commands, and current A-G workflow.
  - recommended_issue_count: `1`
  - proposed_issue_titles:
    - `[docs] Update README for private-local-v1 local app and validation flow`
  - proposed_issue_bodies_or_acceptance_criteria:
    - Document install, frontend/backend startup, validation commands, generated
      artifact boundaries, and the A-G workflow.
    - Do not change runtime behavior.
  - internal_project_area: Quality / Governance
  - priority: medium
  - release_profile_blocker: `no`
  - should_create_now: `deferred`
  - deferral_reason: Wait until clean-install and local-app readiness evidence
    stops moving.
  - related_contracts_tests_tools_or_issues: issue #155, clean-install
    readiness issue proposed above.

### 10. Analytics Readiness

- category: Analytics readiness
- status: `scored`
- score: `4`
- score_confidence: `medium`
- scored_measures:
  - `Analytics uses parser-normalized facts and provenance rather than becoming parser truth (arc42/Q42; SPACE)`
  - `Analytics schema, ingest, and views have targeted validation (arc42/Q42; DORA)`
  - `Analytics views are curated product surfaces rather than generic database browsing (arc42/Q42; SPACE)`
- open_public_reference_inspiration: arc42/Q42, DORA, SPACE.
- objective_evidence:
  - Analytics contracts/reports exist for SQLite schema, migration loader,
    parser-normalized replay ingest, gameplay-action ingest, opponent-card
    observation ingest, field evidence ingest, legacy JSONL adapter, manual
    import, browser upload, folder upload, derived views, replay view harness,
    and local-app analytics views.
  - Analytics-focused tests exist and passed as part of the full Python suite.
  - Local app frontend tests and build passed.
  - `docs/project_roadmap.md` states analytics reads downstream facts and
    provenance, not parser truth.
- subjective_rationale: Analytics is mature enough to support private local
  use after local app/install proof. It is not yet "release-proven" because real
  data operation and live capture are not final.
- why_not_higher: Real historical import/use against the current private
  dataset was not performed in this audit, live parser-owned fact capture is
  still active roadmap work, and sample-size/confidence UX still needs release
  use evidence.
- v1_0_blocker: `no`
- release_profile_relevance: High for `private_local_v1`.
- next_action:
  - Include manual import plus curated analytics views in the local-app
    readiness smoke.
  - Keep analytics downstream of parser-normalized ingest.
  - Record sample-size/degraded-data warnings in release packet.
- related_issues_contracts_tests: issues #204, #207; analytics contracts and
  reports; `tests/test_analytics_*.py`; frontend tests.
- remediation_plan:
  - current_score: `4`
  - target_score_for_active_release_profile: `4`
  - path_to_5: prove real private-local-v1 import-to-view workflow and repeated
    analytics usefulness without hidden parser-truth feedback.
  - recommended_issue_count: `1`
  - proposed_issue_titles:
    - `[analytics] Prove private-local-v1 import-to-curated-views smoke`
  - proposed_issue_bodies_or_acceptance_criteria:
    - Use approved local app/import flow.
    - Confirm match/game/history/action/observation views render safe summaries.
    - Do not store raw private payloads in durable source artifacts.
  - internal_project_area: Analytics / Local App / UI
  - priority: high
  - release_profile_blocker: `no`
  - should_create_now: `deferred`
  - deferral_reason: Can be grouped with local app readiness smoke.
  - related_contracts_tests_tools_or_issues: analytics app reports, local-app
    smoke issue proposed above.

### 11. Future AI Integration Readiness

- category: Future AI integration readiness
- status: `intentionally_deferred`
- score: `N/A`
- score_confidence: `high`
- scored_measures:
  - `AI explanation remains downstream of deterministic parser and analytics facts (arc42/Q42; SPACE)`
  - `Model-provider runtime integration requires separate issue, contract, and credential boundary (NIST SSDF; arc42/Q42)`
- open_public_reference_inspiration: arc42/Q42, SPACE, NIST SSDF.
- objective_evidence:
  - `AGENTS.md`, `docs/agent_rules.yml`, `docs/agent_constitution.md`,
    `docs/project_roadmap.md`, and ADR-0002 preserve AI as downstream
    explanation/recommendation only.
  - The roadmap places AI-assisted coaching after deterministic analytics.
  - No current prompt or contract authorizes OpenAI/model-provider runtime
    integration.
- subjective_rationale: Deferral is the mature posture for
  `private_local_v1`. The repo has clear boundaries and does not need AI
  runtime capability to release a local parser/analytics app.
- why_not_higher: Not scored by design for this profile.
- v1_0_blocker: `deferred`
- release_profile_relevance: Low for `private_local_v1`; higher for later AI
  roadmap phases.
- next_action:
  - Preserve AI boundary wording.
  - Do not create AI runtime work until deterministic local analytics are
    release-proven.
  - Route future AI work through A/B/C/E with credential boundaries.
- related_issues_contracts_tests: ADR-0002, `docs/project_roadmap.md`,
  authority docs.
- remediation_plan:
  - current_score: `N/A`
  - target_score_for_active_release_profile: `N/A`
  - path_to_5: not applicable until an AI integration issue is active.
  - recommended_issue_count: `0`
  - proposed_issue_titles: []
  - proposed_issue_bodies_or_acceptance_criteria: []
  - internal_project_area: Future AI Integration
  - priority: deferred
  - release_profile_blocker: `no`
  - should_create_now: `deferred`
  - deferral_reason: Future AI is intentionally out of scope for
    `private_local_v1`.
  - related_contracts_tests_tools_or_issues: ADR-0002 and roadmap AI phase.

## Baseline Strengths

- Repo authority and role routing are mature and current.
- Parser truth ownership is explicit and repeatedly protected.
- Contract, handoff, and contract-test artifacts are abundant and searchable.
- Full Python and frontend test suites passed in this audit.
- Local app and analytics have moved beyond pure planning into tested backend,
  frontend, import, view, and status surfaces.
- Protected-surface and secret/private-marker tools exist and are routinely
  used in path-scoped review.
- Pyright is correctly advisory, not silently turned into a required gate.
- Future AI is appropriately deferred and downstream.

## Baseline Gaps

- Private-local-v1 cannot be called ready until clean checkout install/startup
  and local-app runtime smoke are proven.
- All-repo secret/private-marker scan debt is unresolved.
- `.env*` ignore-coverage uncertainty appears in local environment reports.
- Pyright advisory findings remain substantial.
- README/onboarding lags current local app and A-G workflow reality.
- Live Player.log mode is still under active development, and raw/private live
  behavior was not tested in this audit.
- This rerun created blocker remediation issues, but GitHub Actions and Codex F
  submission are still pending.

## Unknown Or Not-Checked Evidence

- GitHub Actions were not run by this local audit.
- No live private Player.log was tailed, read, hashed, copied, or inspected.
- No actual app-data root contents were inspected.
- No live workbook, deployed Apps Script, Google Sheets, OpenAI/model-provider,
  production, or external integration behavior was checked.
- Authorized remediation GitHub issues were created only for
  `private_local_v1` blocker rows with `should_create_now: yes`.
- No PR was opened.

## Suggested Remediation Issue List

Created blocker issues:

1. `[release] Prove private-local-v1 clean checkout install and launch path`
   - Blocker: yes.
   - Created: https://github.com/Tahjali11/Mythic-Edge/issues/253
   - Acceptance criteria: clean checkout setup, Python/app deps, frontend deps,
     backend/frontend health, local environment reports, no generated artifacts
     committed.

2. `[quality] Triage private-local-v1 private artifact scanner and env ignore posture`
   - Blocker: yes.
   - Created: https://github.com/Tahjali11/Mythic-Edge/issues/252
   - Acceptance criteria: classify current all-repo scanner findings, resolve
     or document `.env*` ignore-coverage behavior, and do not weaken scanner
     coverage.

3. `[release] Prove private-local-v1 local app startup and status smoke`
   - Blocker: yes.
   - Created: https://github.com/Tahjali11/Mythic-Edge/issues/251
   - Acceptance criteria: backend/frontend startup, setup/status, manual import
     status, analytics views, Match Journal status, and live watcher metadata
     status render safely without destructive controls.

Draft only; do not create until separately authorized:

4. `[docs] Update README for private-local-v1 local app and validation flow`
   - Blocker: no.
   - Acceptance criteria: README reflects current A-G workflow, local app run
     path, validation commands, and generated/private artifact boundaries.

5. `[quality] Define private-local-v1 dependency and validation packet policy`
   - Blocker: no.
   - Acceptance criteria: decide which checks are release-packet requirements
     versus CI gates; keep Pyright advisory unless future contract changes it.

## Validation Run And Result

- `git fetch --prune origin` -> passed.
- `git status --short --branch --untracked-files=all` -> branch
  `codex/engineering-maturity-baseline...origin/codex/engineering-maturity-baseline`.
- `git rev-list --left-right --count HEAD...origin/codex/analytics-foundation`
  -> `0 0` before the submitter branch was created.
- `git rev-list --left-right --count HEAD...origin/codex/engineering-maturity-baseline`
  -> `0 0` before this report update.
- `gh issue view 136` -> issue open.
- `gh issue view 248` -> issue open.
- `gh issue view 249` -> issue open.
- `gh issue view 251` -> issue open, local-app startup/status smoke.
- `gh issue view 252` -> issue open, private-artifact scanner/env posture.
- `gh issue view 253` -> issue open, clean checkout install/launch path.
- `gh pr list --state open --json ...` -> `[]`.
- `py -m pytest -q` -> `1653 passed, 1 skipped, 1 warning`.
- `npm --prefix frontend test -- --run` -> 3 files passed, 68 tests passed.
- `npm --prefix frontend run typecheck` -> passed.
- `npm --prefix frontend run build` -> passed; generated `frontend/dist`
  removed afterward.
- `py -m ruff check src tests tools` -> passed.
- `py tools/run_pyright_advisory_report.py --format json` ->
  `advisory_findings`, `type_findings: 253`, helper behavior non-gating.
- `py tools/check_agent_docs.py` -> passed, checked 46 files, errors 0,
  warnings 0.
- `py tools/check_local_environment.py --profile clean_clone --format json` ->
  status `warning`, summary blocked 0, errors 0, warnings 8.
- `py tools/check_local_environment.py --profile clean_install_transition_audit --format json`
  -> status `warning`, summary blocked 0, errors 0, warnings 3.
- `py tools/check_secret_patterns.py --all` -> result `failed`,
  `forbidden: 540`, `warnings: 898`; treated as pre-existing all-repo
  maturity debt, not a new finding introduced by this report.
- `py tools/check_protected_surfaces.py --base origin/codex/analytics-foundation`
  -> passed, `changed_paths: 0`, `forbidden: 0`, `warnings: 0`.
- Path-scoped protected-surface scan over the source contract and baseline
  report -> passed, `changed_paths: 2`, `forbidden: 0`, `warnings: 0`.
- Path-scoped secret/private-marker scan over the source contract and baseline
  report -> passed, `forbidden: 0`, `warnings: 0`.
- Current-branch path-scoped protected-surface scan over the source contract and
  baseline report with base `origin/codex/engineering-maturity-baseline` ->
  passed, `changed_paths: 2`, `forbidden: 0`, `warnings: 0`.
- Current-branch path-scoped secret/private-marker scan over the source contract
  and baseline report with base `origin/codex/engineering-maturity-baseline` ->
  passed, `forbidden: 0`, `warnings: 0`.
- `git diff --check` -> passed after report creation.

## Protected-Surface Status

No protected parser/runtime/analytics/local-app/workbook/webhook/App Script/
Sheets/OpenAI/AI/production behavior was changed. This audit added only the
baseline report artifact.

Path-scoped protected-surface validation over the source contract and baseline
report passed with `forbidden: 0` and `warnings: 0`.

## Secret / Private-Marker Status

No secrets, credentials, raw logs, private JSONL artifacts, generated SQLite
databases, runtime files, failed posts, workbook exports, or local-only
artifacts were intentionally read, modified, staged, or committed.

All-repo scanner debt remains a private-local-v1 blocker until triaged.

Path-scoped secret/private-marker validation over the source contract and
baseline report passed with `forbidden: 0` and `warnings: 0`.

## Forbidden Scope

Forbidden scope was not touched. This audit did not implement code, change
runtime behavior, add gates, make Pyright required/failing, claim formal
compliance, stage files, open a PR, target main, or close issues.

GitHub remediation issues were created only after explicit authorization and
only for `private_local_v1` blocker rows that were marked
`should_create_now: yes`.

## Recommendation

Route to Codex F for artifact submission after final validation.

Created P1 remediation issues #251, #252, and #253 are now linked to #249 and
to this baseline artifact. Non-blocking and deferred rows remain report drafts
only.

## Pasteable Next-Thread Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #249.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/249

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/136

Source issue:
https://github.com/Tahjali11/Mythic-Edge/issues/248

Branch:
codex/engineering-maturity-baseline

Source contract:
docs/contracts/engineering_maturity_index_open_framework.md

Baseline report:
docs/contract_test_reports/engineering_maturity_baseline.md

Submit only the reviewed docs-only maturity baseline artifacts:
- docs/contracts/engineering_maturity_index_open_framework.md
- docs/contract_test_reports/engineering_maturity_baseline.md

Before staging, inspect git status and verify no unrelated generated/private/local artifacts are included.

Run or verify:
- git status --short --branch --untracked-files=all
- git diff --check
- py tools\check_agent_docs.py
- path-scoped protected-surface scan over the source contract and baseline report
- path-scoped secret/private-marker scan over the source contract and baseline report

Do not implement maturity fixes. The authorized blocker remediation issues have already been created as #251, #252, and #253; do not create more remediation GitHub issues unless explicitly authorized. Do not change parser/runtime/analytics/local app/workbook/webhook/App Script/Sheets/OpenAI/AI/production behavior. Do not create CI gates or make Pyright required/failing. Do not stage unrelated files, target main, close issue #249, close source issue #248, close tracker #136, or close the remediation issues unless explicitly asked.
```

```yaml
workflow_handoff:
  role_performed: "Codex E: Governance Reviewer / Baseline Auditor"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/249"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/136"
  source_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/248"
  completed_thread: "E"
  next_thread: "F"
  next_role: "Codex F: Module Submitter"
  branch: "codex/engineering-maturity-baseline"
  selected_release_profile: "private_local_v1"
  source_contract: "docs/contracts/engineering_maturity_index_open_framework.md"
  target_artifact: "docs/contract_test_reports/engineering_maturity_baseline.md"
  verdict: "baseline_complete_with_private_local_v1_blockers"
  private_local_v1_blockers:
    - "Clean checkout install/local app startup proof is not complete."
    - "All-repo secret/private-marker scanner debt remains unresolved."
    - ".env* ignore-coverage uncertainty remains in local environment reports."
  remediation_issues_created:
    - "https://github.com/Tahjali11/Mythic-Edge/issues/251"
    - "https://github.com/Tahjali11/Mythic-Edge/issues/252"
    - "https://github.com/Tahjali11/Mythic-Edge/issues/253"
  validation:
    - "py -m pytest -q -> 1653 passed, 1 skipped, 1 warning"
    - "npm --prefix frontend test -- --run -> 3 files passed, 68 tests passed"
    - "npm --prefix frontend run typecheck -> passed"
    - "npm --prefix frontend run build -> passed; frontend/dist removed"
    - "py -m ruff check src tests tools -> passed"
    - "py tools/run_pyright_advisory_report.py --format json -> advisory_findings, type_findings 253, non-gating"
    - "py tools/check_agent_docs.py -> passed"
    - "clean_clone local environment report -> warning, blocked 0, errors 0, warnings 8"
    - "clean_install_transition_audit local environment report -> warning, blocked 0, errors 0, warnings 3"
    - "py tools/check_secret_patterns.py --all -> failed with pre-existing all-repo maturity debt, forbidden 540, warnings 898"
    - "gh issue view 251/252/253 -> all open"
    - "git diff --check -> passed after report creation"
    - "path-scoped protected-surface scan over source contract and baseline report -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan over source contract and baseline report -> passed, forbidden 0, warnings 0"
    - "current-branch path-scoped protected-surface and secret/private-marker scans -> passed, forbidden 0, warnings 0"
  forbidden_scope_touched: false
  recommended_next_actions:
    - "Codex F should stage only the source contract and baseline report after path-scoped validation."
    - "Do not create additional remediation issues unless explicitly authorized."
  stop_conditions:
    - "Do not implement maturity fixes."
    - "Do not create CI/Pyright gates."
    - "Do not make Pyright required/failing."
    - "Do not claim formal compliance."
    - "Do not create remediation GitHub issues unless explicitly authorized."
    - "Do not change parser, analytics, SQLite, local app, workbook, production, or AI behavior."
```
