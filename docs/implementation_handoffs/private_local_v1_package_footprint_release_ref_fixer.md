# Private Local V1 Package Footprint Release Ref Fixer Handoff

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/272

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/136

## Contract

`docs/contracts/private_local_v1_package_footprint_release_ref.md`

## Review Artifact

`docs/contract_test_reports/private_local_v1_package_footprint_release_ref.md`

## Implementation Handoff

`docs/implementation_handoffs/private_local_v1_package_footprint_release_ref_comparison.md`

## Required Governance

- `docs/agent_constitution.md`
- `docs/agent_threads/module_fixer.md`

## Internal Project Area

Quality / Governance, with setup-helper support only.

## Truth Owner

The #272 contract owns private-local-v1 package-footprint and release-ref
metadata expectations. Parser/state remains the owner of parser truth. SQLite
remains local analytics support and does not become parser truth.

## Bridge-Code Status

`shared_support`

## Role Performed

Codex D: Module Fixer.

## Source Finding

CT-272-001 P1: report-only handling was insufficient because required
package/readiness manifest/report metadata fields were missing.

Fault category: implementation gap.

## Fix Produced

Implemented a narrow metadata-only setup-helper fix:

- added first-class `release_profile`;
- added first-class `package_mode`;
- added first-class `release_ref`;
- added first-class `public_release_ready: false`;
- added first-class `production_ready: false`;
- threaded the existing `--release-ref` value into check/install setup output;
- preserved proof/setup metadata when proof mode writes final artifacts.

No package shape, clone behavior, release tag, release branch, installer,
default install-root behavior, parser behavior, analytics schema, workbook
behavior, webhook behavior, Apps Script behavior, Sheets behavior, OpenAI/model
provider behavior, AI/coaching behavior, or production behavior changed.

## Files Changed

- `tools/dev_app/private_local_v1_setup.py`
- `tests/test_private_local_v1_setup.py`
- `docs/implementation_handoffs/private_local_v1_package_footprint_release_ref_fixer.md`

Existing #272 artifacts remain in the working tree and were preserved:

- `docs/contracts/private_local_v1_package_footprint_release_ref.md`
- `docs/implementation_handoffs/private_local_v1_package_footprint_release_ref_comparison.md`
- `docs/contract_test_reports/private_local_v1_package_footprint_release_ref.md`

## Code Changed

Yes, metadata-only setup-helper code changed in
`tools/dev_app/private_local_v1_setup.py`.

Runtime install mechanics were not changed. The helper still reports in check
mode without creating folders, blocks unsafe existing-install state, writes
install artifacts only in install/proof paths already covered by existing
tests, and uses symbolic roots in JSON output.

## Tests Changed

Updated `tests/test_private_local_v1_setup.py`:

- check mode now asserts package/readiness metadata on the top-level result,
  manifest, and setup report;
- install mode now asserts the same metadata in persisted manifest/report
  files;
- added a focused configured release-ref regression for direct setup config;
- added a CLI JSON-report regression proving `--release-ref` is reflected in
  top-level, manifest, and report metadata.

Before implementation, the focused tests failed on missing `release_profile`
and unsupported `PrivateLocalV1Config(release_ref=...)`.

After implementation, focused setup tests passed.

## Interface Changes

Metadata fields were added to private-local-v1 setup JSON output:

- `release_profile`
- `package_mode`
- `release_ref`
- `public_release_ready`
- `production_ready`

`PrivateLocalV1Config` now accepts optional `release_ref` with the existing
default `codex/analytics-foundation`.

No CLI flag was added or removed. The existing `--release-ref` flag is now used
for check/install JSON metadata instead of being proof-only.

## Contracted Area Status

Stayed inside the #272 Quality / Governance setup metadata area.

No protected downstream product surface was changed.

## Validation Run

```powershell
git status --short --branch --untracked-files=all
py -m pytest -q tests\test_private_local_v1_setup.py
py -m pytest -q tests\test_analytics_dev_app_launcher.py tests\test_analytics_local_app_backend.py tests\test_analytics_local_app_config.py tests\test_analytics_migration_loader.py
py -m ruff check tools tests
py -m ruff check src tests tools
py tools\dev_app\private_local_v1_setup.py --check --install-root <disposable_temp_root> --json-report
git diff --check
py tools\check_agent_docs.py
path-scoped protected-surface scan over the #272 contract, comparison, report, fixer handoff, setup helper, and focused tests
path-scoped secret/private-marker scan over the #272 contract, comparison, report, fixer handoff, setup helper, and focused tests
```

Results:

- Branch confirmed: `codex/analytics-foundation`.
- Focused setup tests before fix: failed as expected.
- Focused setup tests after fix: `10 passed`.
- Adjacent setup/local-app/config/migration tests: `62 passed`, with one
  existing FastAPI/Starlette deprecation warning.
- Ruff over `tools tests`: passed.
- Ruff over `src tests tools`: passed.
- Check-only setup JSON report against a disposable temp root: passed.
  Observed `package_mode=managed_full_checkout`,
  `release_ref=codex/analytics-foundation`,
  `public_release_ready=False`, `production_ready=False`, and temp root
  remained absent.
- `git diff --check`: passed.
- `py tools\check_agent_docs.py`: passed.
- Path-scoped protected-surface scan over the six touched #272 files: passed,
  `forbidden: 0`, `warnings: 0`.
- Path-scoped secret/private-marker scan over the six touched #272 files:
  passed, `forbidden: 0`, `warnings: 0`.

## Still Unverified

- Full repository pytest was not rerun by this D thread.
- Codex E has not yet independently confirmed the metadata fields.
- No release branch, release tag, slim package, installer, public release
  readiness, production readiness, live workbook readiness, deployed Apps
  Script readiness, or AI/coaching readiness is claimed.

## Generated Artifact Status

No generated/private/runtime/local artifact was retained.

The check-only validation used a disposable temp root and confirmed that root
remained absent.

## Forbidden Scope Status

Forbidden scope touched: false.

No staging, commit, push, PR, merge, issue closure, tracker closure, target-main
action, release tag, release branch, installer, real default-root mutation,
destructive local-folder operation, parser change, analytics schema change,
workbook/webhook/App Script/Sheets change, OpenAI/model-provider change,
AI/coaching change, or production behavior change was performed.

## Remaining Review Focus

Codex E should verify:

- the new metadata appears in check-mode top-level JSON, manifest, and setup
  report;
- the new metadata appears in install-mode persisted manifest/report files;
- `--release-ref` is reflected in check/install JSON metadata;
- public and production readiness remain explicit false values;
- no install mechanics, clone mechanics, package shape, release-tag behavior,
  or protected product surface changed.

## Next Workflow Action

Next role: Codex E: Module Reviewer / confirmation thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / confirmation thread for issue #272.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/272

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/136

Branch:
codex/analytics-foundation

Contract:
docs/contracts/private_local_v1_package_footprint_release_ref.md

Review artifact:
docs/contract_test_reports/private_local_v1_package_footprint_release_ref.md

Fixer handoff:
docs/implementation_handoffs/private_local_v1_package_footprint_release_ref_fixer.md

Confirm only CT-272-001:
- manifest/setup report output includes release_profile, package_mode, release_ref, public_release_ready false, and production_ready false;
- check/install JSON output uses the configured release ref;
- public and production readiness remain explicitly false;
- no package shape, clone behavior, release tag, release branch, installer, real default-root behavior, parser/runtime/analytics/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior, or generated/private artifact behavior changed.

Suggested validation:
git status --short --branch --untracked-files=all
py -m pytest -q tests\test_private_local_v1_setup.py
py -m pytest -q tests\test_analytics_dev_app_launcher.py tests\test_analytics_local_app_backend.py tests\test_analytics_local_app_config.py tests\test_analytics_migration_loader.py
py -m ruff check src tests tools
py tools\dev_app\private_local_v1_setup.py --check --install-root <disposable_temp_root> --json-report
git diff --check
py tools\check_agent_docs.py
path-scoped protected-surface and secret/private-marker scans over the #272 package.

Return a confirmation report and route to Codex F only if CT-272-001 is fixed.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/272"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/136"
  completed_thread: "D"
  next_thread: "E"
  next_role: "Codex E: Module Reviewer / confirmation thread"
  branch: "codex/analytics-foundation"
  source_artifact: "docs/contracts/private_local_v1_package_footprint_release_ref.md"
  review_artifact: "docs/contract_test_reports/private_local_v1_package_footprint_release_ref.md"
  implementation_handoff: "docs/implementation_handoffs/private_local_v1_package_footprint_release_ref_fixer.md"
  finding_fixed:
    - "CT-272-001 P1: private-local-v1 setup manifest/report output now includes first-class package/readiness metadata."
  code_changed: true
  tests_changed: true
  validation:
    - "focused setup tests before fix failed as expected"
    - "focused setup tests after fix -> 10 passed"
    - "adjacent setup/local-app/config/migration tests -> 62 passed, 1 existing third-party warning"
    - "ruff tools/tests and src/tests/tools -> passed"
    - "check-only setup JSON report with disposable temp root -> passed, metadata present, temp root absent"
    - "git diff --check -> passed"
    - "agent docs check -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
  protected_surface_status: "passed, forbidden 0, warnings 0"
  secret_private_marker_status: "passed, forbidden 0, warnings 0"
  generated_artifacts_kept: false
  forbidden_scope_touched: false
  next_recommended_role: "Codex E confirmation thread"
```
