# Validation Matrix Reconciliation Contract

## Module

Validation matrix reconciliation for Mythic Edge workflow validation routing.

This contract defines how Mythic Edge should reconcile the stale PR #65
`docs/validation_matrix.json` idea with the current repo-owned validation
selector, hardening orchestrator, internal project boundaries, local app,
frontend, SQLite analytics, local artifact manifest, clean-install transition,
and advisory Pyright workflow.

Plain English: keep one executable validation selector, keep one local
orchestrator, and add a selector-backed reference layer so humans and Codex can
choose checks without inventing a second source of truth.

## Source Issue

- <https://github.com/Tahjali11/Mythic-Edge/issues/152>

Source material:

- stale PR #65: <https://github.com/Tahjali11/Mythic-Edge/pull/65>
- stale PR #65 `docs/validation_matrix.json`, source material only
- Codex A problem-representation comment on issue #152

## Related Authority

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/decisions/ADR-0001-parser-owns-truth.md`
- `docs/decisions/ADR-0002-local-deterministic-scorer-decides-llm-explains.md`
- `docs/decisions/ADR-0003-player-log-drift-policy.md`
- `docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md`
- `docs/decisions/ADR-0005-external-integration-collaboration-surfaces.md`
- `docs/decisions/ADR-0006-repository-boundary-strategy.md`

## Tracker

N/A.

## Branch

Current branch:

```text
codex/analytics-foundation
```

Do not target `main`.

## Risk Tier

Medium-High.

Reasons:

- validation guidance influences future review and merge confidence;
- a second machine-readable matrix could drift from the selector and
  orchestrator;
- under-routing modern surfaces could skip important local app, frontend,
  analytics, artifact, and clean-install checks;
- over-routing could make small changes painful and encourage validation
  theater;
- accidental CI or Pyright escalation would change project policy.

## Owning Layer

Primary owner: Quality / Governance.

Supporting internal project areas:

- Parser
- Corpus / Provenance
- Analytics
- Local App / UI
- Workbook / Transport
- Generated / Local Artifacts
- Future AI Integration, vocabulary only

## Internal Project Area

Quality / Governance.

This contract is `shared_support` for validation routing across internal
project areas. It does not own runtime product behavior or parser, analytics,
workbook, local app, UI, or AI truth.

## Truth Owner

Validation truth ownership remains split intentionally:

- `tools/select_validation.py` owns executable changed-path to validation
  recommendation selection.
- `tools/run_hardening_orchestrator.py` owns local plan/run validation bundle
  coordination and result capture.
- Individual tools own their own findings:
  - `tools/check_protected_surfaces.py`
  - `tools/check_secret_patterns.py`
  - `tools/check_surface_authorization.py`
  - `tools/check_agent_docs.py`
  - `tools/check_local_environment.py`
  - `tools/run_pyright_advisory_report.py`
- Focused tests own behavioral evidence for their modules.
- GitHub Actions owns only the CI checks it actually runs.
- Codex E and human review own review findings.
- Codex G owns merge, issue closure, and tracker lifecycle decisions after
  explicit approval and satisfied gates.

This contract owns validation routing vocabulary and reconciliation decisions.
It does not make any validation tool the owner of merge readiness, deploy
readiness, parser truth, analytics truth, workbook truth, local app truth, AI
truth, or coaching truth.

## Bridge-Code Status

`shared_support`.

Allowed data flow:

```text
changed repo paths + internal project map + current selector/orchestrator
  -> selector recommendations and human reference matrix
  -> Codex/human validation plans and review evidence
```

Forbidden reverse flow:

- matrix/reference text must not change parser behavior;
- selector recommendations must not authorize protected-surface changes by
  themselves;
- orchestrator output must not become merge, deploy, issue, or tracker truth;
- validation docs must not become runtime product configuration;
- downstream analytics, UI, workbook, or AI surfaces must not feed back into
  parser truth.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/validation_matrix_reconciliation.md`

Future Codex C implementation files authorized by this contract:

- `tools/select_validation.py`, only to update path categories, focused
  command mappings, Pyright priority handling, and safe report metadata for the
  project surfaces named here;
- `tests/test_select_validation.py`, only to pin the selector mapping and
  authority behavior named here;
- optional `docs/validation_matrix.md`, as a human-facing
  non-authoritative reference generated from or manually synchronized with the
  selector/orchestrator contracts;
- optional
  `docs/implementation_handoffs/validation_matrix_reconciliation_comparison.md`.

Narrowly authorized only if Codex C finds a direct selector/orchestrator
contract mismatch:

- `tools/run_hardening_orchestrator.py`
- `tests/test_hardening_orchestrator.py`

The expected implementation should not need orchestrator behavior changes
because the current orchestrator already invokes the selector as a separate
command.

Referenced but not owned:

- stale PR #65 `docs/validation_matrix.json`
- `docs/project_roadmap.md`
- `docs/internal_project_map.md`
- `docs/contracts/repo_wide_validation_selector.md`
- `docs/contracts/repo_wide_hardening_orchestrator.md`
- `.github/workflows/repo-checks.yml`
- `tools/run_repo_checks.ps1`
- `tools/run_touched_file_checks.ps1`
- `tools/check_agent_docs.py`
- `tools/check_protected_surfaces.py`
- `tools/check_secret_patterns.py`
- `tools/check_local_environment.py`
- `docs/local_artifacts_manifest.json`
- `docs/contracts/pre_v1_clean_install_transition.md`
- `docs/contract_test_reports/pre_v1_clean_install_transition.md`
- current parser, analytics, local app, frontend, workbook, and governance
  tests

Not owned:

- parser behavior;
- parser state final reconciliation;
- parser event classes;
- match/game identity or deduplication;
- analytics schema, migrations, ingest, deterministic SQL views, or local app
  query behavior;
- local app backend/frontend runtime behavior;
- workbook schema;
- webhook payload shape;
- Apps Script behavior;
- Google Sheets behavior;
- output transport;
- production behavior;
- AI/model-provider behavior;
- Line Tracer or coaching behavior;
- CI gate policy;
- Pyright gate policy;
- local/generated/private artifacts.

## Observed Current Behavior

Observed on `codex/analytics-foundation` after fast-forward to `a600f80`:

- Issue #152 is open and asks for reconciliation of the stale validation
  matrix idea with the current selector and hardening orchestrator.
- PR #65 is closed and explicitly treated as stale source material.
- PR #65 added `docs/validation_matrix.json`, but that matrix predates current
  local app, frontend, SQLite analytics, local artifact manifest,
  clean-install transition, internal project map, and curated analytics view
  work.
- The stale matrix already expressed useful concepts:
  - baseline `git diff --check`;
  - protected-surface gate;
  - secret/private-marker scan;
  - surface-specific validation commands;
  - advisory validation unless a current issue, contract, or CI gate says
    otherwise.
- Current `tools/select_validation.py` exists and is the executable
  changed-path selector.
- Current `tests/test_select_validation.py` covers:
  - explicit `--base` requirement;
  - changed-path and stdin modes;
  - path normalization and outside-repo path redaction;
  - docs-only narrow checks;
  - governance-doc checker routing;
  - focused hardening tool mappings;
  - focused parser/workbook/output mappings;
  - fixture and CI/dependency routing;
  - protected-surface warning routing;
  - stable JSON output fields.
- Current selector always recommends, for non-empty changed paths:
  - protected-surface gate;
  - secret/private-marker scan;
  - `git diff --check`.
- Current selector recommends Ruff for Python/dependency surfaces.
- Current selector recommends the Pyright advisory report for `src/`, `tools/`,
  and `pyproject.toml` surfaces, but currently uses `recommended` priority.
- Current selector has focused mappings for many parser, hardening, workbook,
  output, runtime, and parser fixture surfaces.
- Current selector does not yet clearly cover every modern surface introduced
  after PR #65, especially:
  - `frontend/`;
  - `src/mythic_edge_parser/local_app/`;
  - `tools/dev_app/`;
  - analytics SQLite migration, ingest, adapter, and curated view families;
  - local artifact manifest and clean-install transition checker profiles;
  - internal project boundary docs as validation-routing vocabulary.
- Current `tools/run_hardening_orchestrator.py` exists and is the executable
  local planner/runner for named validation bundles.
- Current orchestrator:
  - requires explicit `--base`;
  - defaults to plan-only;
  - includes the validation selector as a distinct command;
  - preserves Pyright advisory classification;
  - does not decide merge, deploy, or tracker readiness.
- Current `.github/workflows/repo-checks.yml` runs:
  - full pytest;
  - protected-surface gate on pull requests;
  - Ruff.
- Current CI does not run the selector, orchestrator, secret/private-marker
  scan, local environment checker, frontend checks, or Pyright advisory report
  as required gates.
- Current `docs/internal_project_map.md` names the internal project areas and
  flat-layout ownership policy.
- Current `docs/project_roadmap.md` frames the project as a local MTGA
  decision-support system with parser reliability, code hardening, evidence
  ledger, local analytics, local app, Match Journal, live mode, deterministic
  analytics, and future AI layers.
- Current `docs/local_artifacts_manifest.json` and
  `tools/check_local_environment.py` define report-only local artifact and
  clean-install readiness checks.
- `docs/contract_test_reports/pre_v1_clean_install_transition.md` records
  CT-227-001 as a non-blocking gap: live-looking secret material in
  `.env.example` was manually verified by the scanner, but not pinned by a
  dedicated focused scanner test.

## Contract Decision

Issue #152 must reconcile validation routing, not revive stale PR #65.

Required decisions:

- Do not revive or merge PR #65 directly.
- Do not add `docs/validation_matrix.json` as a new canonical executable config
  in this issue.
- Keep `tools/select_validation.py` as the executable changed-path validation
  selector authority.
- Keep `tools/run_hardening_orchestrator.py` as the executable local
  validation bundle planner/runner authority.
- Add or update a selector-backed validation matrix/reference layer for humans
  and Codex.
- Use the implementation slice to update selector mappings and focused tests
  for modern project surfaces.
- Do not add GitHub Actions gates in this issue.
- Keep Pyright advisory and non-blocking.

## What Validation Matrix Reconciliation Should Accomplish

The reconciliation must:

- make current validation routing readable by internal project area;
- prevent stale matrix guidance from competing with selector/orchestrator code;
- tell Codex C/E/F/G which checks are expected for changed surface families;
- clarify required, recommended, and advisory validation vocabulary;
- expose modern routing gaps in selector mappings;
- keep local artifact and privacy checks visible;
- keep frontend and local app checks visible when those surfaces change;
- keep analytics checks tied to SQLite schema, migration, ingest, views, and
  app-facing query surfaces;
- preserve current CI behavior unless a later contract changes it.

It must not:

- create a hidden second validation engine;
- make a docs matrix runtime config;
- imply that a matrix entry authorizes protected-surface drift;
- make Pyright required/failing;
- widen CI;
- change parser, analytics, local app, workbook, transport, AI, or coaching
  behavior.

## Validation Matrix Artifact Decision

`docs/validation_matrix.json` is not needed now as a canonical config.

If Codex C creates a matrix artifact in this issue, the preferred artifact is:

```text
docs/validation_matrix.md
```

Required status for `docs/validation_matrix.md`:

- human-facing reference;
- selector-backed;
- non-authoritative when it conflicts with `tools/select_validation.py`;
- not loaded by selector or orchestrator at runtime;
- not a CI config;
- not a gate policy;
- not a protected-surface authorization artifact.

If a JSON artifact is created despite this default, it must be explicitly
classified as one of:

- generated documentation snapshot;
- test fixture / comparison fixture;
- non-authoritative reference.

It must not be runtime selector config unless a later issue and contract
authorizes moving selector config out of Python.

## Selector Authority Decision

`tools/select_validation.py` remains the executable selector authority.

Required guarantees:

- require explicit `--base`;
- support `--paths-from-stdin` for deterministic tests and path-scoped checks;
- compute changed paths from `<base>...HEAD` in normal mode;
- never run commands;
- never claim commands passed;
- distinguish `required`, `recommended`, and `advisory`;
- deduplicate commands in stable order;
- explain categories and changed paths that triggered each command;
- always recommend protected-surface and secret/private-marker checks for
  non-empty changed-path sets;
- keep docs-only changes narrow;
- route protected warnings to surface-authorization review recommendations;
- keep Pyright advisory and non-blocking;
- avoid full-suite selection when focused mappings are available.

Codex C may update selector mappings and tests to reflect this contract.
Codex C must not replace the selector with a matrix-loaded runtime config.

## Orchestrator Authority Decision

`tools/run_hardening_orchestrator.py` remains the local validation bundle
planner/runner authority.

Required relationship to the matrix:

- orchestrator does not read `docs/validation_matrix.md`;
- orchestrator does not read `docs/validation_matrix.json`;
- orchestrator may continue to invoke `tools/select_validation.py` as one
  command in its plan/run output;
- selector changes may improve orchestrator output indirectly;
- orchestrator profiles must remain plan/run bundles, not surface-specific
  executable matrix rows;
- orchestrator output must continue to say merge, deploy, and tracker
  readiness are not decided by the orchestrator.

No orchestrator behavior change is expected in this issue. Codex C should edit
orchestrator code only if focused comparison finds a direct mismatch with the
existing orchestrator contract.

## GitHub Actions Decision

No GitHub Actions changes are authorized in issue #152.

Current CI may be cited as existing evidence, but Codex C must not:

- add selector or orchestrator CI gates;
- add secret/private-marker scan as a CI gate;
- add local environment checker as a CI gate;
- add frontend checks as CI gates;
- add Pyright as a CI gate;
- make protected-surface warnings fail CI beyond current behavior;
- edit `.github/workflows/repo-checks.yml`.

A future issue may decide whether selector output should be produced in CI as
plan-only evidence. That is out of scope here.

## Priority Vocabulary

The selector and reference matrix must use these meanings:

- `required`: directly relevant checks that should be run for the changed
  surface before review unless explicitly impossible and documented.
- `recommended`: broader or adjacent checks that improve confidence when
  surface coupling, protected warnings, or unmapped source changes increase
  risk.
- `advisory`: useful diagnostic checks that may report findings without
  blocking the implementation by themselves.

Required checks are not automatically merge gates unless CI, a contract, or
human review makes them gates.

Recommended checks are not optional hand-waving. If skipped, the handoff should
say why.

Advisory checks must not produce failing CI or merge-blocking status by
themselves. They may produce follow-up issues, review notes, or risk
disclosure.

## Pyright Advisory Policy

Pyright must remain advisory in this issue.

Required guarantees:

- selector output must not classify Pyright as `required`;
- orchestrator must continue to classify Pyright findings as `advisory`;
- Pyright exit code `1` for type findings must not make orchestrator exit `1`;
- tooling/config blocker cases may remain errors;
- CI must not run Pyright as a required gate in this issue;
- Codex C/E handoffs should record Pyright findings as advisory evidence, not
  mandatory cleanup.

Codex C may update `tools/select_validation.py` so the Pyright recommendation
uses selector priority `advisory` instead of `recommended`, with focused tests
proving it is never `required`.

## Project Surface Mapping Requirements

The selector-backed matrix/reference must cover at least the following internal
project areas.

### Parser

Path families:

- `src/mythic_edge_parser/events.py`
- `src/mythic_edge_parser/router.py`
- `src/mythic_edge_parser/stream.py`
- `src/mythic_edge_parser/log/**`
- `src/mythic_edge_parser/parsers/**`
- parser-owned files in `src/mythic_edge_parser/app/`
- parser regression fixtures
- parser schema snapshots

Expected validation:

- focused parser tests when a focused mapping exists;
- parser regression tests for parser regression fixtures;
- event/schema snapshot tests when event or workbook-facing row shape can
  drift;
- Ruff for Python changes;
- Pyright advisory for source changes;
- protected-surface authorization recommendation when protected categories are
  touched.

### Corpus / Provenance

Path families:

- evidence ledger modules and tests;
- diagnostics, drift sensor, golden replay, feature-equity corpus ratchet;
- evidence schema snapshot/drift report tooling;
- sanitized fixtures and expected manifests;
- Player.log evidence-ledger contracts and reports.

Expected validation:

- focused `tests/test_evidence_*.py`, `tests/test_golden_*.py`,
  `tests/test_log_drift_sensor.py`, `tests/test_feature_equity_*.py`, and
  related replay/diagnostics tests when those surfaces change;
- fixture/schema snapshot tests when fixture or snapshot families change;
- secret/private-marker scan for any fixture or docs changes;
- no raw private log commits.

### Analytics

Path families:

- `src/mythic_edge_parser/app/analytics_migration_loader.py`
- `src/mythic_edge_parser/app/analytics_migrations/**`
- `src/mythic_edge_parser/app/analytics_ingest.py`
- `src/mythic_edge_parser/app/analytics_legacy_jsonl_adapter.py`
- `src/mythic_edge_parser/app/analytics_sidecar.py`
- analytics app history/query modules;
- analytics contracts, handoffs, and reports;
- `tests/test_analytics_*.py`.

Expected validation:

- `tests/test_analytics_migration_loader.py` for migration loader/package-data
  surfaces;
- `tests/test_analytics_schema.py` for schema/migration SQL changes;
- `tests/test_analytics_derived_views.py` for deterministic SQL view changes;
- `tests/test_analytics_parser_normalized_replay_ingest.py`,
  `tests/test_analytics_gameplay_action_ingest.py`,
  `tests/test_analytics_opponent_card_observation_ingest.py`, and
  `tests/test_analytics_field_evidence_ingest.py` for ingest surfaces;
- `tests/test_analytics_legacy_jsonl_artifact_adapter.py`,
  `tests/test_analytics_manual_jsonl_import.py`, and
  `tests/test_analytics_browser_jsonl_upload.py` for local artifact import
  adapter surfaces;
- `tests/test_analytics_replay_view_harness.py` when replay/view expectations
  are involved;
- generated SQLite artifact scan whenever analytics implementation or tests are
  changed.

### Local App / UI

Path families:

- `src/mythic_edge_parser/local_app/**`
- `tools/dev_app/**`
- `frontend/**`
- local app contracts, handoffs, and reports.

Expected validation:

- backend/config/setup tests for local app backend and setup/status surfaces;
- manual/browser import tests for import job surfaces;
- analytics app history/view tests for read-only analytics API surfaces;
- launcher tests for developer launcher surfaces;
- frontend typecheck, tests, and build for frontend source changes:

```bash
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
```

If frontend dependencies are absent, Codex C may run
`npm --prefix frontend ci` before frontend validation, but must not commit
`node_modules` or build output.

### Workbook / Transport

Path families:

- `src/mythic_edge_parser/app/sheet_schema.py`
- `src/mythic_edge_parser/app/sheet_exports.py`
- `src/mythic_edge_parser/app/outputs.py`
- `src/mythic_edge_parser/app/transforms.py`
- `tools/google_apps_script/**`
- workbook/schema snapshots and tests.

Expected validation:

- sheet schema/export/output focused tests;
- event/schema snapshot tests when row or payload shape can drift;
- Apps Script parity checks when Apps Script surfaces are touched;
- protected-surface authorization recommendation.

This issue does not authorize workbook, webhook, or Apps Script behavior
changes.

### Quality / Governance

Path families:

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/**`
- `docs/templates/**`
- `docs/decisions/**`
- issue/PR templates;
- `tools/select_validation.py`
- `tools/run_hardening_orchestrator.py`
- `tools/check_*.py`
- hardening reports and contracts.

Expected validation:

- `tools/check_agent_docs.py`;
- selector tests for selector changes;
- orchestrator tests for orchestrator changes;
- focused hardening tool tests for changed hardening tools;
- Ruff for Python tooling changes;
- path-scoped protected-surface and secret/private-marker checks.

### Generated / Local Artifacts

Path families:

- `docs/local_artifacts_manifest.json`
- `tools/check_local_environment.py`
- `tests/test_check_local_environment.py`
- repo-local `data/**` families;
- generated SQLite and sidecar files;
- frontend build/dependency artifacts;
- `.env*`, credential, token, and webhook URL surfaces;
- private JSONL, raw logs, runtime logs, local status, and workbook exports.

Expected validation:

- `tests/test_check_local_environment.py` for manifest/checker changes;
- clean-clone or relevant local environment profile report when artifact
  policy changes;
- secret/private-marker scan;
- protected-surface gate;
- generated/private artifact scan before handoff.

Do not commit private/generated/local artifacts.

### Future AI Integration

Path families:

- future AI/advisor contracts or docs only, unless a later issue authorizes
  implementation.

Expected validation:

- governance/docs checks for docs-only AI boundary work;
- no model-provider calls;
- no credential/environment contract changes;
- no AI-owned parser, analytics, validation, merge, deploy, hidden-card, or
  coaching truth.

Naming this project area does not authorize OpenAI/model-provider runtime
integration.

## Matrix Reference Shape

If `docs/validation_matrix.md` is created, it must include:

- a status banner: `non-authoritative selector-backed reference`;
- a pointer to `tools/select_validation.py` as executable authority;
- a pointer to `tools/run_hardening_orchestrator.py` as bundle planner/runner;
- a table by internal project area;
- path family examples;
- expected required checks;
- expected recommended checks;
- expected advisory checks;
- protected-surface notes;
- generated/private artifact notes;
- a "When in doubt, run the selector" instruction.

It must not include:

- raw local paths;
- raw logs;
- private JSONL examples;
- generated SQLite examples;
- credentials or webhook URLs;
- CI gate claims;
- merge/deploy/tracker readiness claims.

## Selector Mapping Requirements

Codex C should update selector mappings only where current behavior is
underrepresented.

Required mapping improvements:

- frontend path category and commands;
- local app backend path category and focused Python tests;
- developer launcher path category and tests;
- analytics migration/schema/ingest/view/import path categories and focused
  tests;
- local artifact manifest/checker path category and focused tests;
- internal project map and validation matrix docs as Quality / Governance
  reference surfaces;
- Pyright advisory priority must not be required.

Selector output should continue to be stable, deterministic, and
standard-library-only.

The selector should not load `docs/validation_matrix.md` or
`docs/validation_matrix.json`.

## CT-227-001 Routing Decision

Do not absorb CT-227-001 into #152 by default.

CT-227-001 is a focused scanner coverage gap:

- `.env.example` with live-looking secret material should be caught by
  `tools/check_secret_patterns.py`;
- the behavior was manually verified in the pre-v1 clean-install contract-test
  report;
- it is not a validation matrix behavior.

Required handling:

- mention CT-227-001 as adjacent quality debt in the matrix reference if useful;
- do not modify `tools/check_secret_patterns.py` in issue #152;
- do not add the dedicated scanner regression test in issue #152 unless Codex C
  is already touching `tests/test_check_secret_patterns.py` for an in-scope
  selector/reference reason;
- preferred future route: separate narrow issue,
  `[quality] Pin .env.example secret scanner coverage`.

## Error Behavior

If selector and matrix/reference disagree:

- selector output wins for executable changed-path recommendations;
- update the reference or route a follow-up;
- do not silently change implementation behavior based on docs alone.

If selector and orchestrator disagree:

- selector owns changed-path recommendation content;
- orchestrator owns plan/run command execution and result capture;
- Codex C should add focused tests only for the specific mismatch.

If a path cannot be mapped confidently:

- selector should fall back to existing safe behavior:
  - required safety gates;
  - `git diff --check`;
  - Ruff/Pyright advisory when Python/source applies;
  - recommended broader tests for unmapped source changes.
- Codex C should preserve uncertainty in the implementation handoff.

If a proposed mapping would imply parser, analytics, local app, workbook,
transport, CI, AI, or production behavior change:

- stop and route back to Codex A/B.

## Side Effects

Allowed in Codex B:

- create this contract only.

Allowed in future Codex C:

- edit selector code/tests;
- add or update a non-authoritative validation matrix reference document;
- create implementation handoff artifact.

Not allowed:

- GitHub Actions edits;
- CI gate changes;
- runtime behavior changes;
- schema/migration/view changes;
- parser behavior changes;
- workbook/webhook/Apps Script changes;
- local file cleanup, deletion, copy, archive, rename, or sanitization;
- generated/private/local artifact commits.

## Dependency Order

Future implementation should follow this order:

1. Compare stale PR #65 matrix categories to current selector categories.
2. Compare current selector categories to `docs/internal_project_map.md`.
3. Add focused selector mappings/tests for modern surfaces.
4. Adjust Pyright priority if needed so it is advisory and non-required.
5. Add `docs/validation_matrix.md` only as a non-authoritative reference.
6. Run focused selector/orchestrator/docs/safety validation.
7. Produce implementation handoff.

## Compatibility

Required compatibility:

- existing selector CLI remains:

```bash
python3 tools/select_validation.py --base <git-ref>
```

- existing selector `--paths-from-stdin` remains supported;
- selector JSON output fields remain stable unless Codex C documents and tests
  an additive change;
- existing orchestrator CLI remains:

```bash
python3 tools/run_hardening_orchestrator.py --base <git-ref> --profile <profile>
```

- orchestrator `plan`, `quick`, `full`, and `post-hardening` profiles remain;
- Pyright advisory report remains non-blocking for type findings;
- current CI workflow remains unchanged.

## Unknowns

- Whether a future issue should extract selector path families into a generated
  JSON config.
- Whether CI should eventually emit selector output as plan-only evidence.
- Whether frontend checks should become CI gates after local app maturity.
- Whether the validation matrix reference should eventually be generated from
  selector constants rather than maintained manually.
- Whether CT-227-001 should be pinned before or after broader local artifact
  policy work.

## Suspected Gaps

- Current selector does not explicitly route all current frontend/local app
  surfaces.
- Current selector may under-route analytics migration/view/ingest families
  relative to the newer analytics contracts.
- Current selector may under-route local artifact manifest and clean-install
  surfaces.
- Current selector marks Pyright as `recommended` rather than clearly
  `advisory`.
- Current docs do not provide one concise human-readable validation matrix by
  internal project area.

## Tests Required

Codex C validation should be scoped to actual changed files, but likely
required commands are:

```bash
python3 -m pytest -q tests/test_select_validation.py
python3 -m pytest -q tests/test_hardening_orchestrator.py
python3 -m pytest -q tests/test_check_local_environment.py tests/test_check_secret_patterns.py tests/test_check_protected_surfaces.py
python3 -m ruff check tools tests src
python3 tools/check_agent_docs.py
git diff --check
```

If frontend mappings or reference sections are added or changed:

```bash
npm --prefix frontend run typecheck
npm --prefix frontend run test -- --run
npm --prefix frontend run build
```

If Codex C changes only selector/docs and does not touch frontend code, Codex C
may validate frontend routing through selector tests instead of running the
frontend suite. If frontend commands are not run, the handoff must say so.

If analytics mappings are changed, focused selector tests must prove the
selected analytics commands. Codex C does not need to run every analytics suite
unless selector implementation or test changes touch analytics code.

Safety checks:

```bash
printf '%s\n' <changed-files> | python3 tools/check_secret_patterns.py --base origin/codex/analytics-foundation --paths-from-stdin
printf '%s\n' <changed-files> | python3 tools/check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
```

Generated/private artifact check:

```bash
find . -path './.git' -prune -o \( -name '*.sqlite' -o -name '*.sqlite3' -o -name '*.db' -o -name '*.sqlite-wal' -o -name '*.sqlite-shm' -o -name '*.sqlite-journal' \) -print
```

Codex E should verify:

- selector remains executable authority;
- orchestrator remains bundle planner/runner;
- any matrix/reference is non-authoritative;
- no CI changes;
- no Pyright gate escalation;
- modern surfaces route to focused checks;
- CT-227-001 is not accidentally hidden or mislabeled as solved.

## Acceptance Criteria

- `docs/contracts/validation_matrix_reconciliation.md` exists.
- The contract answers all issue #152 matrix authority questions.
- Codex C route is narrow and implementable.
- Selector authority remains clear.
- Orchestrator authority remains clear.
- `docs/validation_matrix.json` is not revived as canonical runtime config.
- GitHub Actions remain out of scope.
- Pyright remains advisory and non-blocking.
- Modern frontend, local app, analytics, local artifact, and internal project
  boundary surfaces have selector mapping requirements.
- CT-227-001 is routed as adjacent scanner coverage debt, not silently solved.
- Protected surfaces are explicitly preserved.

## Expected Codex C Scope

Expected Codex C implementation scope:

- update `tools/select_validation.py` mapping categories and focused commands;
- update `tests/test_select_validation.py` focused mapping tests;
- optionally add `docs/validation_matrix.md` as a non-authoritative
  selector-backed reference;
- optionally update orchestrator tests only if selector/orchestrator
  interaction needs a focused assertion;
- create
  `docs/implementation_handoffs/validation_matrix_reconciliation_comparison.md`.

Expected Codex C non-scope:

- no CI edits;
- no stale PR #65 merge;
- no `docs/validation_matrix.json` as executable config;
- no parser/runtime/analytics/local app/frontend/workbook/webhook/Apps Script
  behavior changes;
- no local artifact cleanup or generated/private artifact commits.

## Next Workflow Action

Next role: Codex C: Module Implementer.

Pasteable prompt:

```yaml
prompt: |
  Use the Mythic Edge agent constitution.
  Use $mythic-edge-workflow.

  Act as Codex C: Module Implementer for issue #152, validation matrix reconciliation.

  Issue:
  https://github.com/Tahjali11/Mythic-Edge/issues/152

  Branch:
  codex/analytics-foundation

  Contract:
  docs/contracts/validation_matrix_reconciliation.md

  Expected handoff artifact:
  docs/implementation_handoffs/validation_matrix_reconciliation_comparison.md

  Goal:
  Compare the current selector, orchestrator, stale PR #65 validation-matrix source material, and modern project surfaces against the validation matrix reconciliation contract. Implement only the smallest selector/docs/test changes needed to satisfy the contract.

  Read first:
  - AGENTS.md
  - docs/agent_rules.yml
  - docs/agent_constitution.md
  - docs/codex_module_workflow.md
  - docs/agent_threads/implementation.md
  - docs/contracts/validation_matrix_reconciliation.md
  - docs/project_roadmap.md
  - docs/internal_project_map.md
  - docs/contracts/repo_wide_validation_selector.md
  - tools/select_validation.py
  - tests/test_select_validation.py
  - docs/contracts/repo_wide_hardening_orchestrator.md
  - tools/run_hardening_orchestrator.py
  - tests/test_hardening_orchestrator.py
  - .github/workflows/repo-checks.yml
  - docs/local_artifacts_manifest.json
  - docs/contracts/pre_v1_clean_install_transition.md
  - docs/contract_test_reports/pre_v1_clean_install_transition.md
  - current focused local app, frontend, analytics, selector, orchestrator, protected-surface, secret scanner, and local environment checker tests as needed

  Implement only if supported by the comparison:
  - Update tools/select_validation.py for modern frontend, local app, analytics, local artifact, clean-install, and internal project boundary routing.
  - Update tests/test_select_validation.py to pin those mappings and Pyright advisory/non-required behavior.
  - Add docs/validation_matrix.md only as a non-authoritative selector-backed human reference, if it improves handoff clarity.
  - Touch tools/run_hardening_orchestrator.py or tests/test_hardening_orchestrator.py only for a direct contract mismatch.
  - Produce docs/implementation_handoffs/validation_matrix_reconciliation_comparison.md.

  Do not:
  - Target main.
  - Revive or merge PR #65 directly.
  - Add docs/validation_matrix.json as canonical executable config.
  - Add CI gates or edit .github/workflows/repo-checks.yml.
  - Make Pyright required/failing.
  - Replace selector or orchestrator behavior beyond the narrow contract route.
  - Change parser behavior, parser state final reconciliation, parser event classes, match/game identity, or deduplication.
  - Change analytics schema, migrations, ingest semantics, deterministic views, local app/UI behavior, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets behavior, output transport, production behavior, AI/model-provider behavior, Line Tracer, or coaching behavior.
  - Delete, move, rename, archive, sanitize, copy, or clean local files.
  - Commit raw Player.log files, private JSONL artifacts, generated SQLite databases, runtime logs, failed delivery artifacts, workbook exports, secrets, credentials, API keys, tokens, webhook URLs, or local-only artifacts.

  Validation:
  - python3 -m pytest -q tests/test_select_validation.py
  - python3 -m pytest -q tests/test_hardening_orchestrator.py
  - python3 -m pytest -q tests/test_check_local_environment.py tests/test_check_secret_patterns.py tests/test_check_protected_surfaces.py
  - python3 -m ruff check tools tests src
  - python3 tools/check_agent_docs.py
  - git diff --check
  - Run path-scoped secret/private-marker and protected-surface checks for changed files.
  - Run generated/private artifact scans.
  - Run frontend typecheck/test/build only if frontend implementation or frontend validation behavior is directly changed; otherwise prove frontend routing with selector tests and document skipped frontend runtime checks.

workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/152"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/validation_matrix_reconciliation.md"
  target_artifact: "docs/implementation_handoffs/validation_matrix_reconciliation_comparison.md"
  risk_tier: "Medium-High"
  branch: "codex/analytics-foundation"
  validation:
    - "Codex B documentation-only contract pass"
    - "Codex C should run focused selector/orchestrator/local-environment/scanner/protected-surface tests as applicable"
  stop_conditions:
    - "Do not target main."
    - "Do not revive stale PR #65 directly."
    - "Do not add CI gates or make Pyright required/failing."
    - "Do not create docs/validation_matrix.json as canonical executable config."
    - "Do not create a second unsynchronized validation authority."
    - "Do not change parser/runtime/analytics/local app/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
    - "Do not create, delete, move, copy, sanitize, archive, or commit generated/private/local artifacts or secrets."
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/152"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/validation_matrix_reconciliation.md"
  target_artifact: "docs/implementation_handoffs/validation_matrix_reconciliation_comparison.md"
  risk_tier: "Medium-High"
  branch: "codex/analytics-foundation"
  validation:
    - "Codex B documentation-only contract pass"
    - "Codex C should run python3 -m pytest -q tests/test_select_validation.py"
    - "Codex C should run python3 -m pytest -q tests/test_hardening_orchestrator.py"
    - "Codex C should run python3 -m pytest -q tests/test_check_local_environment.py tests/test_check_secret_patterns.py tests/test_check_protected_surfaces.py"
    - "Codex C should run python3 -m ruff check tools tests src"
    - "Codex C should run python3 tools/check_agent_docs.py"
    - "Codex C should run git diff --check"
    - "Codex C should run path-scoped secret/private-marker and protected-surface checks"
    - "Codex C should run generated/private artifact scans"
  stop_conditions:
    - "Do not target main."
    - "Do not revive stale PR #65 directly."
    - "Do not add CI gates or make Pyright required/failing."
    - "Do not create docs/validation_matrix.json as canonical executable config."
    - "Do not create a second unsynchronized validation authority."
    - "Do not change parser/runtime/analytics/local app/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
    - "Do not create, delete, move, copy, sanitize, archive, or commit generated/private/local artifacts or secrets."
```
