# Engineering Maturity Index Open Framework Contract

## Module

Mythic Edge Engineering Maturity Index, open-reference framework.

Plain English: this contract defines a practical rubric for asking whether
Mythic Edge is reliable, maintainable, installable, safe to run locally, and
ready enough for its current release profile. It defines the scoring framework.
It does not score the repo yet.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/248
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/136
- Branch: `codex/analytics-foundation`
- Risk tier: Medium-High
- Expected contract artifact:
  `docs/contracts/engineering_maturity_index_open_framework.md`
- Later baseline artifact:
  `docs/contract_test_reports/engineering_maturity_baseline.md`

## Source Artifacts

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/project_roadmap.md`
- GitHub issue `#136`
- GitHub issue `#248`
- `docs/contracts/validation_matrix_reconciliation.md`
- `docs/contracts/repo_wide_validation_selector.md`
- `docs/contracts/code_hardening_pyright_advisory.md`
- `docs/contracts/repo_wide_pyright_advisory_report.md`
- `docs/contracts/internal_project_boundaries.md`
- `docs/contracts/internal_project_boundary_annotation_organization.md`
- `docs/decisions/ADR-0001-parser-owns-truth.md`
- `docs/decisions/ADR-0003-player-log-drift-policy.md`
- `docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md`
- `docs/decisions/ADR-0006-repository-boundary-strategy.md`
- `README.md`
- `pyproject.toml`
- `.github/workflows/repo-checks.yml`
- `tools/select_validation.py`
- `tools/run_repo_checks.ps1`
- `tools/check_protected_surfaces.py`
- `tools/check_secret_patterns.py`
- `tools/run_pyright_advisory_report.py`

## Open/Public Reference Stack

The following references are inspiration and crosswalk material only. They are
not repo authority and this contract does not claim formal compliance.

- arc42 / Q42 quality model:
  https://quality.arc42.org/articles/arc42-quality-model
- DORA metrics:
  https://dora.dev/guides/dora-metrics/
- SPACE framework:
  https://www.microsoft.com/en-us/research/publication/the-space-of-developer-productivity-theres-more-to-it-than-you-think/
- CHAOSS metrics:
  https://github.com/chaoss/metrics
- OWASP SAMM:
  https://owasp.org/www-project-samm/
- NIST SSDF SP 800-218:
  https://csrc.nist.gov/pubs/sp/800/218/final
- OpenSSF Scorecard:
  https://openssf.org/scorecard/
- SLSA:
  https://slsa.dev/levels

## Owning Layer

Primary owner: Quality / Governance.

Supporting internal project areas:

- Parser
- Corpus / Provenance
- Analytics
- Local App / UI
- Workbook / Transport
- Generated / Local Artifacts
- Future AI Integration, deferred vocabulary only

## Truth Owner

The maturity index owns a quality-evaluation framework. It does not own runtime
truth.

It must not become the owner of:

- parser truth;
- evidence truth;
- analytics truth;
- workbook truth;
- local app truth;
- validation tool truth;
- merge readiness;
- deployment readiness;
- AI truth;
- credential or secret policy.

Repo authority remains:

1. system/developer/user instructions;
2. `AGENTS.md`;
3. `docs/agent_rules.yml`;
4. `docs/agent_constitution.md`;
5. current issues/contracts;
6. accepted ADRs;
7. tests, tools, handoffs, reviews, and CI evidence.

## Bridge-Code Status

`shared_support`

Allowed data flow:

```text
repo evidence + contracts + tests + validation tools + release profile
  -> maturity category score row
  -> remediation plan / follow-up issue drafts
```

Forbidden reverse flow:

- a maturity score must not authorize runtime changes by itself;
- a maturity score must not override a contract, ADR, test failure, or protected
  surface warning;
- a maturity score must not become a CI gate;
- a maturity score must not make Pyright required/failing;
- a maturity score must not replace focused implementation validation.

## Files Owned By This Contract

This contract owns:

- `docs/contracts/engineering_maturity_index_open_framework.md`

Future baseline-audit work may create:

- `docs/contract_test_reports/engineering_maturity_baseline.md`

Future remediation planning may create or draft GitHub issues only when the
baseline-audit prompt explicitly authorizes issue creation.

This contract does not authorize edits to runtime code, validation tools, CI,
Pyright configuration, parser code, analytics code, local app code, frontend
code, workbook transport code, Apps Script code, or generated/private artifacts.

## What The Index Is

The Mythic Edge Engineering Maturity Index is a project-specific quality rubric
for evaluating:

- engineering maturity;
- release readiness;
- operational risk;
- local install/run confidence;
- safety around private/generated artifacts;
- parser/evidence reliability;
- long-term improvement areas.

It should help future Codex threads separate real quality risk from cosmetic
preferences and process theater.

## What The Index Is Not

The index is not:

- a formal compliance claim;
- a CI gate;
- a Pyright escalation;
- a single vanity score;
- a substitute for focused tests;
- a substitute for code review;
- a license to refactor working code for style alone;
- authority above repo docs, accepted ADRs, current contracts, or user-approved
  scope;
- a reason to delay useful app or analytics work without concrete release risk;
- a requirement that every category reach score `5` before private local v1.

## Open/Public Reference Crosswalk

| Reference | Use In This Index | Must Not Mean |
| --- | --- | --- |
| arc42 / Q42 | Product/system quality dimensions such as maintainable, operable, reliable, secure, suitable, and usable. Useful for architecture, local app usability, documentation, and maintainability measures. | No claim that Mythic Edge follows arc42 documentation method or any formal quality certification. |
| DORA | Delivery throughput, change/recovery discipline, failure visibility, and release-profile readiness. Useful for validation, release, and recovery measures. | No claim that a personal local app needs enterprise deployment targets or DORA benchmarking. |
| SPACE | Multi-dimensional developer productivity and workflow health. Useful for avoiding single-metric scoring and preserving flow, collaboration, handoff quality, and maintainability. | No individual productivity surveillance, activity-count vanity metrics, or Codex performance score. |
| CHAOSS | Open-source/project-health inspiration: maintainability, issue/PR health, documentation, community/readiness signals. | No claim that Mythic Edge is currently a public open-source community project. |
| OWASP SAMM | Security maturity inspiration for threat-aware development, secure lifecycle practices, and iterative improvement. | No formal SAMM assessment or organizational security program claim. |
| NIST SSDF | Secure software development practices, vulnerability reduction, protection of sensitive artifacts, and common secure-development vocabulary. | No federal procurement or NIST conformance claim. |
| OpenSSF Scorecard | Repository/security hygiene inspiration: dependency, branch, token, CI, and public-repo risk signals. | No requirement to run or pass OpenSSF Scorecard for private local v1. |
| SLSA | Source/build provenance, artifact integrity, and supply-chain trust concepts. | No SLSA level claim, attestation requirement, or build provenance gate for private local v1. |

## Scoring Scale

Scores use a 0-5 scale:

| Score | Label | Meaning |
| --- | --- | --- |
| 0 | absent | The area is missing or not meaningfully addressed. |
| 1 | informal / ad hoc | The area exists through habit, chat context, manual knowledge, or scattered evidence. |
| 2 | documented | The area is described in contracts, docs, ADRs, issues, or README material. |
| 3 | tested or demonstrated | The area has focused tests, successful command evidence, screenshots, smoke checks, CI evidence, or repeatable demonstrations. |
| 4 | enforced by workflow/tooling | The area is supported by repo-local tools, selectors, scans, contract checks, repeatable validation, or review workflow. |
| 5 | release-proven and hard to break quietly | The area has survived release-profile validation, clean setup/use evidence, repeated workflow use, and regression detection strong enough that breakage is unlikely to be silent. |

Scoring rule:

- A category may use sub-measures, but the category score should reflect the
  weakest release-relevant area, not the average of unrelated strengths.
- A score should never exceed the available evidence confidence.
- A score below `5` always requires a path-to-5 plan, even when the gap does
  not block the current release profile.

## Score Confidence Labels

- `high`: supported by current repo evidence, tests, contracts, tools, CI, or
  repeated workflow evidence.
- `medium`: supported by some direct evidence, but not fully validated across
  the active release profile.
- `low`: preliminary judgment, subjective-heavy rationale, stale evidence, or
  insufficient direct validation.

Confidence is not score severity. A score of `2` with high confidence is better
than a score of `4` based on wishful thinking.

## Category Status Labels

- `scored`: evidence is sufficient to assign a 0-5 score.
- `not_applicable`: the category or measure does not apply to the selected
  release profile.
- `intentionally_deferred`: the category or measure is real but intentionally
  out of scope for the selected release profile.
- `insufficient_evidence`: the baseline audit cannot responsibly score the row
  yet.

Rows with `not_applicable`, `intentionally_deferred`, or
`insufficient_evidence` must not fake a numeric score.

## Release Profiles

### `private_local_v1`

The first release profile for the user's own machine/workflow.

Primary emphasis:

- parser/evidence reliability;
- private artifact safety;
- local app startup and diagnostics;
- installability from a clean checkout;
- usable local analytics;
- no production-facing regressions.

Does not require:

- public package release;
- broad community onboarding;
- SLSA attestation;
- OpenSSF Scorecard passing;
- every maturity category at `5`.

### `shared_with_developer_v1`

The profile for sharing with another developer who may run the project locally.

Additional emphasis:

- setup reproducibility;
- README/onboarding clarity;
- dependency installation clarity;
- validation command clarity;
- branch/PR workflow portability;
- clearer issue/remediation plans.

### `public_open_source_release`

The profile for a public open-source release.

Additional emphasis:

- public fixture/privacy policy;
- stronger supply-chain hygiene;
- public documentation;
- dependency and license visibility;
- public support expectations;
- broader security posture.

## Maturity Categories

### 1. Architecture And Truth Ownership

Reference inspiration:

- arc42/Q42
- CHAOSS

Required measures:

- Parser truth ownership is explicit and cited.
- Internal project boundaries are documented.
- Bridge code is labeled and does not reverse truth flow.
- Protected surfaces have explicit authorization paths.

Example scored measures:

- `Parser truth remains upstream of workbook, analytics, UI, and AI (arc42/Q42; CHAOSS)`
- `Internal project ownership is documented without forcing premature repo splits (arc42/Q42; CHAOSS)`

### 2. Parser Correctness And Evidence

Reference inspiration:

- arc42/Q42
- DORA

Required measures:

- Parser state and final reconciliation are contract-tested.
- Player.log evidence boundaries are visible.
- Drift, confidence, finality, and degradation are represented for critical
  outputs where in scope.

Example scored measures:

- `Parser-managed match/game facts are verified at the parser/state layer (arc42/Q42; DORA)`
- `Player.log drift and degraded evidence are surfaced without guessing (arc42/Q42)`

### 3. Test And Corpus Coverage

Reference inspiration:

- arc42/Q42
- CHAOSS

Required measures:

- Focused unit/contract tests exist for critical modules.
- Sanitized/golden fixtures are used where appropriate.
- Snapshot or schema tests protect important shapes.
- Corpus gaps are documented instead of hidden.

Example scored measures:

- `Critical parser and analytics behaviors have focused regression coverage (arc42/Q42; CHAOSS)`
- `Golden fixture and corpus gaps are explicit rather than invisible (CHAOSS; arc42/Q42)`

### 4. Local App Runtime And Usability

Reference inspiration:

- arc42/Q42
- SPACE
- DORA

Required measures:

- Local app launch/status paths are tested or demonstrated.
- User-visible state is safe, understandable, and non-destructive.
- Runtime diagnostics explain blocked/degraded states.
- UI does not claim parser, analytics, or coaching truth it does not own.

Example scored measures:

- `Local app launch and setup status are reproducible enough for the active release profile (arc42/Q42; DORA)`
- `Operator-facing diagnostics reduce guesswork without exposing private artifacts (arc42/Q42; SPACE)`

### 5. Security And Private Artifact Safety

Reference inspiration:

- OWASP SAMM
- NIST SSDF
- OpenSSF Scorecard

Required measures:

- Secret/private-marker scanning exists and is used.
- Protected local/generated artifacts are ignored or blocked.
- Local app responses avoid raw paths, raw payloads, raw hashes, stack traces,
  SQL text, secrets, and environment values.
- External writes and credential changes remain explicit-approval actions.

Example scored measures:

- `Secret/private artifact scanning exists and is routinely used (OWASP SAMM; NIST SSDF; OpenSSF Scorecard)`
- `Raw Player.log, private JSONL, generated SQLite, runtime artifact, and secret boundaries are documented (OWASP SAMM; NIST SSDF)`

### 6. Delivery Workflow And Release Readiness

Reference inspiration:

- DORA
- SPACE
- CHAOSS

Required measures:

- A-G workflow handoffs are durable and current.
- Validation selector/orchestrator guidance is clear.
- Release-readiness evidence is separated from implementation desire.
- Recovery/rollback and unresolved-risk notes are visible.

Example scored measures:

- `Release recovery clarity is visible in issues, handoffs, and validation reports (DORA; SPACE)`
- `Validation routing is deterministic without becoming a second authority (DORA; CHAOSS)`

### 7. Installability And Operational Portability

Reference inspiration:

- arc42/Q42
- DORA
- OpenSSF Scorecard

Required measures:

- Clean checkout setup expectations are documented.
- Launcher/local app startup is tested or demonstrated.
- Generated app-data and local-only folders are separated from repo-owned files.
- Fresh-machine or clean-install proof exists for the active release profile.

Example scored measures:

- `Clean checkout setup is reproducible for the active release profile (arc42/Q42; DORA)`
- `Generated app-data folders are separated from repo files (arc42/Q42; OpenSSF Scorecard)`

### 8. Supply-Chain And Repo Hygiene

Reference inspiration:

- OpenSSF Scorecard
- SLSA
- NIST SSDF

Required measures:

- Dependencies and dev dependencies are declared in repo-owned files.
- CI and local validation are documented.
- Build/generated artifacts are excluded from Git.
- Source/build provenance needs are understood for the selected release profile.

Example scored measures:

- `Build/release provenance expectations are appropriate to the release profile (SLSA; OpenSSF Scorecard)`
- `Dependency and generated-artifact hygiene are visible in repo-owned tooling (NIST SSDF; OpenSSF Scorecard)`

### 9. Documentation And Onboarding

Reference inspiration:

- arc42/Q42
- CHAOSS
- SPACE

Required measures:

- README and roadmap match current behavior.
- Contracts, handoffs, and reports are discoverable.
- Fresh Codex/human contributors can find authority and next steps.
- Beginner-friendly explanations do not weaken technical accuracy.

Example scored measures:

- `Onboarding docs explain current setup and project authority without relying on chat memory (arc42/Q42; CHAOSS)`
- `Handoff artifacts reduce restart cost for future threads (SPACE; CHAOSS)`

### 10. Analytics Readiness

Reference inspiration:

- arc42/Q42
- DORA
- SPACE

Required measures:

- Analytics consumes parser-normalized facts, not raw-log shortcuts.
- SQLite schema and migrations are deterministic and tested.
- Views carry sample-size/confidence limitations where appropriate.
- Analytics stays downstream of parser/evidence truth.

Example scored measures:

- `Analytics uses parser-normalized facts and provenance rather than becoming parser truth (arc42/Q42; SPACE)`
- `Analytics schema, ingest, and views have targeted validation (arc42/Q42; DORA)`

### 11. Future AI Integration Readiness

Reference inspiration:

- arc42/Q42
- SPACE
- NIST SSDF

Required status for current baseline unless a later AI issue is active:

- `intentionally_deferred`

Required measures when active:

- AI consumes deterministic parser/analytics facts.
- AI outputs are labeled as explanation, hypothesis, inference, or
  recommendation.
- AI does not own hidden-card truth, gameplay correctness, player mistake truth,
  parser truth, analytics truth, workbook truth, or model-provider truth.
- OpenAI/model-provider runtime integration is separately contracted.

Example scored measures:

- `AI explanation remains downstream of deterministic parser and analytics facts (arc42/Q42; SPACE)`
- `Model-provider runtime integration requires separate issue, contract, and credential boundary (NIST SSDF; arc42/Q42)`

## Required Row Shape

Each future baseline row must include:

- `category`
- `status`
- `score`, if `status = scored`
- `score_confidence`
- `scored_measures`, each with inline source tags
- `open_public_reference_inspiration`
- `objective_evidence`
- `subjective_rationale`
- `why_not_higher`
- `v1_0_blocker`: `yes`, `no`, or `deferred`
- `release_profile_relevance`
- `next_action`: 1 to 3 items
- `related_issues_contracts_tests`
- `remediation_plan`

Recommended Markdown row format:

```markdown
### <Category>

- status:
- score:
- score_confidence:
- scored_measures:
  - `<measure> (<source tag>; <source tag>)`
- open_public_reference_inspiration:
- objective_evidence:
- subjective_rationale:
- why_not_higher:
- v1_0_blocker:
- release_profile_relevance:
- next_action:
- related_issues_contracts_tests:
- remediation_plan:
```

## Inline Source Tag Policy

Every scored measure must include inline source tags.

Allowed reference tags:

- `arc42/Q42`
- `DORA`
- `SPACE`
- `CHAOSS`
- `OWASP SAMM`
- `NIST SSDF`
- `OpenSSF Scorecard`
- `SLSA`

Examples:

- `Local app launch reproducibility (arc42/Q42; DORA)`
- `Secret/private artifact protection (OWASP SAMM; NIST SSDF; OpenSSF Scorecard)`
- `Release recovery clarity (DORA; SPACE)`
- `Build/release provenance (SLSA; OpenSSF Scorecard)`
- `Maintainability and module ownership (arc42/Q42; CHAOSS)`

Inline tags are not compliance claims. They only identify reference
inspiration.

## Objective Evidence Types

Allowed objective evidence includes:

- issue exists/open/closed state;
- issue linked to tracker;
- contract exists;
- implementation handoff exists;
- review or contract-test report exists;
- ADR accepted;
- focused tests exist;
- focused tests pass;
- GitHub Actions pass;
- validation selector recommends appropriate checks;
- protected-surface scan exists and passes;
- secret/private-marker scan exists and passes or has documented expected
  warnings;
- Pyright advisory report exists without being required/failing;
- README/setup docs match observed behavior;
- launcher/backend/frontend smoke evidence exists;
- clean-install/fresh-machine proof exists;
- raw/private/generated artifacts are ignored or blocked;
- parser/evidence/truth boundaries are documented and tested;
- public/open-source references were used only as inspiration.

Evidence must cite concrete repo artifacts, commands, issues, PRs, or tests.
General impressions alone are not objective evidence.

## Subjective Rationale Requirements

Subjective rationale is allowed, but must be explicit.

Allowed subjective judgments:

- architecture understandability;
- operator/UI clarity;
- maintainability of bridge code;
- usefulness of analytics views;
- ease of future Codex handoff;
- whether complexity is justified by project needs;
- whether release risk is concrete or speculative.

Every subjective rationale must include:

- the current release profile;
- the evidence it considered;
- why the judgment matters;
- what would make confidence higher.

## V1.0 Blocker Policy

The maturity index must distinguish low maturity from release blocking.

Rules:

- A score below `5` does not automatically block `private_local_v1`.
- A score of `4` can still block if the missing evidence is essential to the
  selected release profile.
- A score of `2` can be acceptable if the area is intentionally deferred for the
  selected release profile.
- `public_open_source_release` has a higher bar than `private_local_v1`.
- Blocker status must be decided row-by-row with release-profile relevance.

Private local v1 likely blocker areas:

- parser/evidence correctness for user-visible facts;
- private artifact safety;
- clean checkout/install/run path;
- local app setup/status reliability;
- enough analytics usability to justify the release;
- validation and recovery clarity for the actual local workflow.

## Under-5 Remediation Issue-Generation Policy

Every scored maturity element below `5` must include a path-to-5 remediation
plan in the later baseline audit.

Each under-5 remediation plan must include:

- `current_score`
- `target_score_for_active_release_profile`
- `path_to_5`
- `recommended_issue_count`
- `proposed_issue_titles`
- `proposed_issue_bodies_or_acceptance_criteria`
- `internal_project_area`
- `priority`
- `release_profile_blocker`: `private_local_v1`, `shared_with_developer_v1`,
  `public_release`, or `no`
- `should_create_now`: `yes`, `no`, or `deferred`
- `deferral_reason`, if deferred
- `related_contracts_tests_tools_or_issues`

Issue grouping rule:

- Create or draft one issue per coherent improvement area, not one issue per
  scoring point.
- Group gaps when they share the same root cause, owner, validation path, and
  protected-surface risk.
- Split gaps when they require different owners, different contracts, different
  protected surfaces, or different validation evidence.

Default issue creation rule:

- The baseline audit may draft remediation issue titles and bodies by default.
- It may create GitHub issues only when the user prompt explicitly authorizes
  issue creation.
- It must not create all remediation issues in this framework contract thread.

Path-to-5 vs release blocker distinction:

- Every under-5 row needs a path to 5.
- Not every under-5 row blocks the active release profile.
- The baseline report must make that distinction visible.

## Composite Score Policy

The index should not use a single averaged score as the primary result.

Required primary outputs:

- category scores;
- category confidence;
- release-profile blocker flags;
- remediation issue plan;
- readiness summary by release profile.

Optional composite:

- A composite may be included only as secondary context.
- It must not hide blockers.
- It must not average away a critical low-scoring category.
- It must not be used as a CI gate or go/no-go rule by itself.

## Refresh Cadence

Refresh the index:

- before a `private_local_v1` readiness decision;
- after major roadmap phases;
- after major architecture or truth-boundary changes;
- after major validation-tooling policy changes;
- before sharing with another developer;
- before public/open-source release consideration;
- after significant security/private-artifact policy changes.

Do not refresh the full index:

- for every small feature;
- for typo-only or formatting-only docs changes;
- as a substitute for focused validation;
- as a way to delay useful work without a concrete release risk.

## Future Baseline Audit Policy

The future baseline audit must:

- use this contract as the rubric;
- select one active release profile;
- score every category or mark it with a non-scored status;
- cite repo evidence for every score;
- include subjective rationale where needed;
- include `why_not_higher` for every scored row below `5`;
- include path-to-5 remediation plans for every under-5 row;
- distinguish current-release blockers from long-term improvement items;
- preserve protected-surface and parser truth boundaries;
- avoid formal compliance claims.

Expected baseline artifact:

```text
docs/contract_test_reports/engineering_maturity_baseline.md
```

## Example Rows

These examples show row shape only. They are not the final repo baseline.

### Example: Security And Private Artifact Safety

- category: Security and private artifact safety
- status: `scored`
- score: `4`
- score_confidence: `medium`
- scored_measures:
  - `Secret/private artifact scanning exists and is routinely used (OWASP SAMM; NIST SSDF; OpenSSF Scorecard)`
  - `Raw Player.log, private JSONL, generated SQLite, runtime artifact, and secret boundaries are documented (OWASP SAMM; NIST SSDF)`
  - `Local app responses avoid private path, raw payload, raw hash, SQL, stack trace, and secret exposure (arc42/Q42; OWASP SAMM; NIST SSDF)`
- open_public_reference_inspiration: OWASP SAMM, NIST SSDF, OpenSSF Scorecard,
  arc42/Q42.
- objective_evidence: protected-surface and secret/private-marker tooling,
  local artifact policy work, repeated validation handoffs, and local app
  privacy tests where present.
- subjective_rationale: Mythic Edge has unusually strong private artifact
  discipline for a personal local tool, but some future live/AI/public-release
  surfaces remain unproven.
- why_not_higher: actual clean-install/live-machine behavior and future
  AI/API integrations still need release-profile-specific security passes.
- v1_0_blocker: `no`, unless scans or local app privacy tests regress.
- release_profile_relevance: high for `private_local_v1`; higher for
  `public_open_source_release`.
- next_action:
  - define which checks are required in a v1 readiness packet;
  - keep private artifact scans in baseline audit validation;
  - defer public-release security scoring until public release is in scope.
- related_issues_contracts_tests: `docs/contracts/validation_matrix_reconciliation.md`,
  `tools/check_secret_patterns.py`, `tools/check_protected_surfaces.py`.
- remediation_plan:
  - current_score: `4`
  - target_score_for_active_release_profile: `4`
  - path_to_5: prove clean-install/live-app privacy behavior and any future
    model-provider boundaries before public release.
  - recommended_issue_count: `1`
  - proposed_issue_titles:
    - `[quality] Define v1 readiness private-artifact validation packet`
  - release_profile_blocker: `no`
  - should_create_now: `deferred`
  - deferral_reason: baseline audit should verify current evidence first.

### Example: Installability And Operational Portability

- category: Installability and operational portability
- status: `scored`
- score: `3`
- score_confidence: `medium`
- scored_measures:
  - `Windows launcher starts the local app from an existing checkout (arc42/Q42; DORA)`
  - `Generated app-data folder expectations are documented and separate from repo files (arc42/Q42; OWASP SAMM)`
  - `Fresh-machine setup proof is not yet complete (DORA; SPACE; OpenSSF Scorecard)`
- open_public_reference_inspiration: arc42/Q42, DORA, SPACE, OpenSSF
  Scorecard, OWASP SAMM.
- objective_evidence: local developer app launcher, app-data path contracts,
  Python tooling inventory, and pre-v1 clean-install transition work.
- subjective_rationale: the project is runnable locally, but release-grade
  installation still needs proof from a clean checkout or fresh machine.
- why_not_higher: developer-only setup still depends on existing-machine
  assumptions and actual clean-install execution remains separate work.
- v1_0_blocker: `yes`, if clean-install proof is not completed before private
  local v1.
- release_profile_relevance: critical for `private_local_v1` and
  `shared_with_developer_v1`.
- next_action:
  - prove clean checkout setup;
  - verify launcher startup;
  - verify backend/frontend health and local DB path behavior.
- related_issues_contracts_tests: local artifact and clean-install contracts,
  launcher tests, local app backend tests.
- remediation_plan:
  - current_score: `3`
  - target_score_for_active_release_profile: `4`
  - path_to_5: clean-install proof first, then repeated release-profile use
    before treating it as hard to break quietly.
  - recommended_issue_count: `1`
  - proposed_issue_titles:
    - `[release] Prove private local v1 clean-install startup path`
  - release_profile_blocker: `private_local_v1`
  - should_create_now: `yes`
  - deferral_reason: `N/A`

## Anti-Goals

The maturity index must not become:

- a CI gate;
- a Pyright escalation;
- a formal compliance claim;
- a vanity score;
- a substitute for tests;
- a reason to refactor working code for style alone;
- a reason to delay useful app/analytics work without concrete release risk;
- an authority above repo docs, accepted ADRs, contracts, tests, or
  user-approved scope;
- a requirement that every category reach `5` before `private_local_v1`;
- a way to move truth ownership into quality/governance docs.

## Protected Surfaces

This contract does not authorize changes to:

- parser behavior;
- parser state final reconciliation;
- parser event classes;
- match identity;
- game identity;
- deduplication;
- analytics behavior;
- SQLite schema or migrations;
- local app/UI behavior;
- workbook schema;
- webhook payload shape;
- Apps Script behavior;
- Google Sheets behavior;
- output transport;
- production behavior;
- AI/model-provider behavior;
- CI gate policy;
- Pyright gate policy;
- secrets, credentials, environment variables, raw logs, generated data,
  runtime files, local retry artifacts, workbook exports, local JSONL artifacts,
  generated SQLite files, or local-only artifacts.

## Validation Requirements

For this Codex B contract thread:

```powershell
git diff --check
py tools\check_agent_docs.py
@'
docs/contracts/engineering_maturity_index_open_framework.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
@'
docs/contracts/engineering_maturity_index_open_framework.md
'@ | py tools\check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
```

If the file is untracked, use an equivalent new-file-safe whitespace check
without staging.

For the future baseline audit:

- inspect issue #136 and this contract;
- inspect current contracts, ADRs, tests, tools, README, roadmap, workflow docs,
  and relevant issue/PR evidence;
- do not run implementation code changes;
- run only read-only validation and evidence-gathering commands unless the user
  authorizes otherwise;
- do not create remediation issues unless explicitly authorized.

## Acceptance Criteria

- Contract exists at
  `docs/contracts/engineering_maturity_index_open_framework.md`.
- The contract defines what the index is and is not.
- The open/public reference crosswalk is present and disclaims formal
  compliance.
- Maturity categories are defined.
- Scoring scale, confidence labels, category statuses, and release profiles are
  defined.
- Required row shape is defined.
- Inline source tags are required for scored measures.
- Objective evidence and subjective rationale rules are defined.
- V1 blocker interpretation is defined.
- Under-5 remediation issue-generation policy is defined.
- Anti-goals and protected surfaces are included.
- The contract routes to a future baseline audit instead of scoring the repo in
  this thread.

## Next Workflow Action

Recommended next role:

- Codex A: Thinker / Problem Representation for the read-only baseline audit,
  if no baseline issue exists yet.

Alternative next role:

- Codex E / Contract-Test Baseline Auditor, if the user explicitly wants to
  score the repo directly from this contract without opening a separate issue.

Pasteable prompt for the recommended next thread:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex A: Thinker / Problem Representation for the Mythic Edge Engineering Maturity baseline audit.

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/136

Source contract:
docs/contracts/engineering_maturity_index_open_framework.md

Current branch:
codex/analytics-foundation

Goal:
Create the problem representation for a read-only baseline audit that scores Mythic Edge against the open engineering maturity index without implementing code, creating gates, making Pyright required, claiming formal compliance, or changing runtime behavior.

Expected baseline artifact:
docs/contract_test_reports/engineering_maturity_baseline.md

The baseline audit should select an active release profile, likely private_local_v1 unless the user says otherwise; score or mark every category; cite objective evidence; include subjective rationale where needed; identify v1 blockers; and produce under-5 path-to-5 remediation plans. Draft remediation issue titles/bodies, but do not create issues unless explicitly authorized.

Do not change parser behavior, analytics behavior, SQLite schema/migrations, local app/UI behavior, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets behavior, output transport, production behavior, AI/model-provider behavior, CI gates, Pyright policy, secrets, raw logs, generated data, runtime files, local retry artifacts, workbook exports, local JSONL artifacts, generated SQLite files, or local-only artifacts. Do not target main.

Output must include:
- role performed
- tracker reviewed
- source contract used
- selected release profile
- baseline audit scope
- evidence collection plan
- stop conditions
- expected baseline artifact
- next recommended role
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/248"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/136"
  completed_thread: "B"
  next_thread: "A"
  source_artifact: "GitHub issue #248 problem representation"
  contract_artifact: "docs/contracts/engineering_maturity_index_open_framework.md"
  target_artifact: "docs/contract_test_reports/engineering_maturity_baseline.md"
  risk_tier: "Medium-High"
  branch: "codex/analytics-foundation"
  validation:
    - "git diff --check or new-file-safe equivalent"
    - "py tools/check_agent_docs.py"
    - "path-scoped protected-surface scan"
    - "path-scoped secret/private-marker scan"
  stop_conditions:
    - "Do not score the repo in the framework contract thread."
    - "Do not claim formal compliance with external references."
    - "Do not create CI/Pyright gates."
    - "Do not create all remediation issues in the framework contract thread."
    - "Do not change runtime, parser, analytics, workbook, local app, production, or AI behavior."
```
