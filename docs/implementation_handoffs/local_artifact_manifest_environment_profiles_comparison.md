# Local Artifact Manifest And Environment Profiles Comparison

## Role Performed

Codex C: Module Implementer / comparison thread.

## Source Issue Reviewed

<https://github.com/Tahjali11/Mythic-Edge/issues/153>

## Related Issue Reviewed

<https://github.com/Tahjali11/Mythic-Edge/issues/227>

Issue #227 remains separate clean-install and checkout-retirement work. This
pass did not implement #227 behavior.

## Contract Used

`docs/contracts/local_artifact_manifest_environment_profiles.md`

## Branch And Git Status

Branch confirmed: `codex/analytics-foundation`.

Initial status:

```text
## codex/analytics-foundation...origin/codex/analytics-foundation
?? docs/contracts/local_artifact_manifest_environment_profiles.md
```

The contract artifact was untracked source material from Codex B. It was read
and left as a source artifact.

## Files Inspected

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/contracts/local_artifact_manifest_environment_profiles.md`
- `.gitignore`
- `pyproject.toml`
- `src/mythic_edge_parser/local_app/paths.py`
- `tools/check_protected_surfaces.py`
- `tools/check_secret_patterns.py`
- `tests/test_check_secret_patterns.py`
- `tests/test_check_protected_surfaces.py`
- `tests/test_analytics_local_app_config.py`
- PR #65 source-material manifest and checker patch, read-only

## Current Behavior Compared To Contract

What already existed:

- `.gitignore` already ignores major local generated families and frontend
  generated outputs.
- The protected-surface checker already classifies risky path families.
- The secret/private-marker scanner already performs content scanning with
  redacted findings.
- Local app path helpers already use symbolic app-data labels and avoid folder
  creation in status helpers.
- Local app tests already verify path redaction and no-write setup/status
  behavior.

Gaps found:

- No current source-controlled local artifact manifest existed.
- No report-only local environment checker existed.
- No canonical profile set existed for clean clone, local developer app,
  analytics development, live parser readiness, or historical import readiness.
- No focused tests covered manifest schema, alias mapping, report-only exit
  behavior, private path redaction, or no local app state creation for this
  checker.
- `.env*` ignore coverage is not confirmed by the current ignore policy; this
  pass records that as a suspected gap instead of editing `.gitignore`.

## Implementation Option Chosen

Implemented the smallest v1 report-only path authorized by the contract:

- Add a JSON manifest as the machine-readable source of artifact
  classifications.
- Add a standard-library-only checker that loads the manifest, selects a
  profile, performs metadata-only checks, and renders text or JSON.
- Add focused tests for schema, profile references, aliases, redaction,
  private-content non-reading, no app-data creation, report-only exit codes,
  and JSON shape.
- Add this implementation handoff.

## Files Changed

- `docs/local_artifacts_manifest.json`
- `tools/check_local_environment.py`
- `tests/test_check_local_environment.py`
- `docs/implementation_handoffs/local_artifact_manifest_environment_profiles_comparison.md`

The source contract `docs/contracts/local_artifact_manifest_environment_profiles.md`
remains untracked source material from Codex B and was not edited.

## Exact Manifest Sections Changed

`docs/local_artifacts_manifest.json`:

- Added `schema_version: local_artifacts_manifest.v1`.
- Added `object: mythic_edge_local_artifacts_manifest`.
- Added aliases for stale PR #65 concepts:
  - `live_parser` -> `live_parser_readiness`
  - `analytics_dev` -> `analytics_development`
- Added required profiles:
  - `clean_clone`
  - `local_developer_app`
  - `analytics_development`
  - `live_parser_readiness`
  - `historical_import_readiness`
- Added required artifact classifications:
  - Repo-Owned Source Files
  - Generated Local App State
  - Private Local Inputs
  - Private Local Outputs
  - Generated Nonprivate Support Data
  - Secret And Credential Surfaces
- Added artifact entries for repo source, local app state, selected private
  inputs, local output families, generated support outputs, and secret-adjacent
  surfaces.

## Exact Checker Sections Changed

`tools/check_local_environment.py`:

- Added manifest loading and validation.
- Added profile alias resolution.
- Added report-only CLI:
  - `--profile`
  - `--repo-root`
  - `--manifest`
  - `--format text|json`
  - `--app-data-root`
  - `--player-log-path`
  - `--source-path`
  - `--source-folder`
- Added safe repo metadata checks:
  - existence
  - file or directory kind
  - Git tracked evidence for repo-owned source
  - Git ignore evidence for local/generated families
- Added safe app-data checks using symbolic display paths only.
- Added safe user-selected private input checks using existence, kind, and
  extension only.
- Added environment-variable-name presence checks without printing values.
- Added stable JSON report shape and human-readable text output.
- Preserved report-only exit behavior:
  - `0` for generated reports, including warnings and blocked readiness
  - `2` for invocation or manifest errors

## Exact Test Sections Changed

`tests/test_check_local_environment.py`:

- Added manifest schema and artifact field coverage.
- Added profile and alias reference coverage.
- Added unknown-profile and malformed-manifest exit-code coverage.
- Added clean-clone private-artifact non-requirement coverage.
- Added blocked-readiness-with-exit-zero coverage.
- Added private path and private content redaction coverage for JSON and text.
- Added app-data no-creation coverage.
- Added environment variable value non-disclosure coverage.
- Added stable report shape coverage.
- Added stale PR #65 raw expanded path regression coverage.
- Added JSONL extension checking without payload reading.

## Code Changed

Code changed: yes, one new report-only tooling script.

Tests changed: yes, one new focused test module.

Docs changed: yes, one new manifest and one handoff.

Parser/runtime behavior changed: no.

Analytics behavior changed: no.

Local app behavior changed: no.

CI gates changed: no.

## Interface Changes

New local quality CLI:

```powershell
py tools\check_local_environment.py --profile clean_clone
py tools\check_local_environment.py --profile local_developer_app
py tools\check_local_environment.py --profile analytics_development
py tools\check_local_environment.py --profile live_parser_readiness
py tools\check_local_environment.py --profile historical_import_readiness
```

The checker is a report surface only. It does not create setup state, run
imports, start runtime processes, inspect private payloads, or modify repo
files.

## Validation Run

```text
py -m pytest -q tests\test_check_local_environment.py
-> 14 passed

py -m pytest -q tests\test_check_secret_patterns.py tests\test_check_protected_surfaces.py
-> 76 passed, 1 skipped

py -m pytest -q tests\test_analytics_local_app_config.py tests\test_analytics_local_app_backend.py tests\test_analytics_manual_jsonl_import.py
-> 35 passed, 1 warning from FastAPI/Starlette TestClient deprecation

py -m ruff check tools tests src
-> passed

git diff --check
-> passed

new-file whitespace/ascii/final-newline check
-> passed

py tools\check_secret_patterns.py --all
-> command exited 0 in all-repo advisory mode; report result remains failed because of pre-existing repository findings outside this module

path-scoped protected-surface scan over contract, manifest, checker, tests, and handoff
-> passed, forbidden 0, warnings 0

path-scoped secret/private-marker scan over contract, manifest, checker, tests, and handoff
-> warning result, forbidden 0, warnings 7 from manifest artifact-reference placeholders

py tools\check_local_environment.py --profile local_developer_app --format json
-> exited 0; generated a warning-status report without raw path output

py tools\check_local_environment.py --profile analytics_dev --format json
-> exited 0; alias resolved to analytics_development
```

## Protected-Surface Status

No forbidden protected surfaces were changed. No parser state, event classes,
match/game identity, deduplication, analytics schema, migrations, ingest,
views, workbook schema, webhook payload shape, Apps Script behavior, Google
Sheets behavior, output transport, production behavior, AI/model-provider
behavior, Line Tracer behavior, or coaching behavior was changed.

## Secret/Private-Marker Status

The new checker does not print raw private paths, local usernames, selected
private filenames, private file contents, environment variable values, tokens,
keys, workbook identifiers, or transport endpoints.

Path-scoped secret/private-marker scan had no forbidden findings. The warnings
are artifact-reference warnings from the manifest documenting local artifact
families with placeholder context.

All-repo advisory scanning still reports pre-existing findings outside this
module. That is not new to this pass and remains outside the authorized scope.

## Generated/Private Artifact Status

No generated/private/local artifacts were created, moved, copied, sanitized,
uploaded, imported, hashed, deleted, or committed.

The checker was run against existing local state and reported symbolic
presence/missing information only.

## Remaining Risks Or Unverified Layers

- `.env*` ignore coverage is a suspected policy gap recorded by the checker;
  `.gitignore` was not edited under this first implementation pass.
- #227 clean-install and checkout-retirement behavior remains unimplemented.
- Live parser readiness with a real operator path was not verified.
- Historical import readiness with a real private source was not verified.
- Live workbook state, deployed Apps Script state, Google Sheets behavior, and
  production behavior were not verified and were intentionally out of scope.
- All-repo secret/private-marker advisory findings remain pre-existing cleanup
  debt outside this module.

## Forbidden Scope Touched

Forbidden scope touched: false.

This pass did not:

- implement #227 clean-install or checkout-retirement behavior;
- merge or revive PR #65;
- edit `.gitignore`;
- add CI gates;
- create local app state or SQLite files;
- run imports;
- read private payloads;
- change parser/runtime/analytics/local app/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior.

## Next Recommended Role

Codex E: Module Reviewer / contract-test thread.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #153.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/153

Related issue:
https://github.com/Tahjali11/Mythic-Edge/issues/227

Branch:
codex/analytics-foundation

Contract:
docs/contracts/local_artifact_manifest_environment_profiles.md

Implementation handoff:
docs/implementation_handoffs/local_artifact_manifest_environment_profiles_comparison.md

Files to review:
- docs/local_artifacts_manifest.json
- tools/check_local_environment.py
- tests/test_check_local_environment.py
- docs/implementation_handoffs/local_artifact_manifest_environment_profiles_comparison.md

Review goal:
Verify that the implementation satisfies the local artifact manifest and environment profile checker contract without exceeding scope.

Check specifically:
- The manifest uses the required v1 schema, profiles, classifications, and artifact-entry fields.
- PR #65 concepts map only through current profile names or aliases and stale PR #65 behavior is not restored blindly.
- The checker is report-only and exits 0 for generated warning/blocked reports, 2 for invocation or manifest errors.
- Reports use symbolic/redacted paths and do not echo private paths, usernames, selected private filenames, payloads, values, hashes, credentials, workbook identifiers, or transport endpoints.
- The checker never reads private file contents and never creates app-data folders, SQLite files, logs, generated outputs, or repo-local artifacts.
- Existing protected-surface and secret/private-marker behavior is preserved.
- Existing local app setup/status/import behavior is unchanged.
- #227 clean-install and checkout-retirement behavior remains unimplemented.

Do not:
- edit implementation files unless the user explicitly reroutes to Codex D;
- implement #227 behavior;
- merge or revive stale PR #65;
- edit .gitignore, CI gates, parser/runtime behavior, analytics schema/migrations/ingest/views, local app runtime behavior, workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior;
- create, delete, move, rename, copy, sanitize, upload, import, hash, archive, or commit generated/private/local artifacts or secrets;
- stage, commit, push, open a PR, close issue #153 or #227, or target main unless explicitly asked.

Recommended validation:
git status --short --branch
py -m pytest -q tests\test_check_local_environment.py
py -m pytest -q tests\test_check_secret_patterns.py tests\test_check_protected_surfaces.py
py -m pytest -q tests\test_analytics_local_app_config.py tests\test_analytics_local_app_backend.py tests\test_analytics_manual_jsonl_import.py
py -m ruff check tools tests src
git diff --check
py tools\check_secret_patterns.py --all
Run path-scoped protected-surface and secret/private-marker scans over the contract, manifest, checker, tests, and handoff.

Final review report must lead with findings ordered by severity. If no blocking findings exist, say so clearly and include remaining risks, validation run, protected-surface status, secret/private-marker status, generated/private artifact status, and next recommended role.
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/153"
  related_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/227"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "GitHub issue #153, stale PR #65 source material, and docs/contracts/local_artifact_manifest_environment_profiles.md"
  target_artifact: "docs/implementation_handoffs/local_artifact_manifest_environment_profiles_comparison.md"
  branch: "codex/analytics-foundation"
  risk_tier: "Medium-High"
  validation:
    - "py -m pytest -q tests\\test_check_local_environment.py -> 14 passed"
    - "py -m pytest -q tests\\test_check_secret_patterns.py tests\\test_check_protected_surfaces.py -> 76 passed, 1 skipped"
    - "py -m pytest -q tests\\test_analytics_local_app_config.py tests\\test_analytics_local_app_backend.py tests\\test_analytics_manual_jsonl_import.py -> 35 passed, 1 warning"
    - "py -m ruff check tools tests src -> passed"
    - "git diff --check -> passed"
    - "new-file whitespace/ascii/final-newline check -> passed"
    - "py tools\\check_secret_patterns.py --all -> exited 0 in all-repo advisory mode; pre-existing all-repo findings remain"
    - "path-scoped protected-surface scan including handoff -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan including handoff -> forbidden 0, warnings 7"
  stop_conditions:
    - "Do not implement #227 clean-install or checkout-retirement behavior."
    - "Do not merge or revive stale PR #65 directly."
    - "Do not edit .gitignore or CI gates without a follow-up contract."
    - "Do not create, mutate, read, copy, sanitize, upload, move, delete, hash, import, archive, or commit generated/private/local artifacts."
    - "Do not change parser/runtime/analytics/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
    - "Do not target main."
```

## Codex D Fixer Addendum

Role performed: Codex D: Module Fixer.

Source finding:

- `docs/contract_test_reports/local_artifact_manifest_environment_profiles.md`
- CT-153-001 P1: `.env*` secret-surface checks only inspected `.env.local`,
  so repo-local `.env` or `.env.<suffix>` files could be missed.

Fault category: implementation mismatch with the manifest contract.

Fix produced:

- Added focused regression coverage for `.env`, `.env.local`, and
  `.env.production` in a temporary Git repo.
- Updated `tools/check_local_environment.py` so the `.env*` repo-relative
  manifest pattern is checked as a metadata-only glob.
- The checker reports a matched `.env*` family as present local state without
  reading values or echoing matched filenames.
- The display path remains symbolic: `<repo>\.env*`.

Files changed by this D pass:

- `tools/check_local_environment.py`
- `tests/test_check_local_environment.py`
- `docs/implementation_handoffs/local_artifact_manifest_environment_profiles_comparison.md`

Validation run:

```text
py -m pytest -q tests\test_check_local_environment.py -> 15 passed
py -m pytest -q tests\test_check_secret_patterns.py tests\test_check_protected_surfaces.py -> 76 passed, 1 skipped
py -m pytest -q tests\test_analytics_local_app_config.py tests\test_analytics_local_app_backend.py tests\test_analytics_manual_jsonl_import.py -> 35 passed, 1 existing FastAPI/Starlette warning
py -m ruff check tools tests src -> passed
git diff --check -> passed
```

Protected-surface status:

- No parser/runtime/analytics schema/migration/ingest/view/local app runtime/
  workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior was
  changed.

Secret/private-marker status:

- The focused regression writes synthetic `.env*` files only inside pytest temp
  directories.
- The checker still reports `contents_read: false` and does not print `.env*`
  values.
- Path-scoped secret/private-marker scan should still be rerun by Codex E after
  review; this D pass did not intentionally add real secrets or private
  artifacts.

Generated/private artifact status:

- No generated/private/local artifacts were intentionally created, moved,
  copied, sanitized, uploaded, imported, hashed, archived, deleted, or
  committed.
- Pytest temporary `.env*` files were test-local only.

Remaining review focus:

- Confirm the `.env*` glob handling is narrow enough for the manifest contract
  and does not turn the checker into a general deep filesystem scanner.
- Confirm `.gitignore` remains intentionally unchanged for this pass.
- Confirm issue #227 clean-install and checkout-retirement behavior remains
  unimplemented.

Still-unverified layers:

- Live operator machines with real `.env*` files.
- Live parser readiness with a real operator path.
- Historical import readiness with a real private source.
- Workbook, Apps Script, Google Sheets, OpenAI/AI, and production behavior,
  all intentionally out of scope.

Next recommended role: Codex E confirmation thread.

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/153"
  related_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/227"
  completed_thread: "D"
  next_thread: "E"
  next_role: "Codex E: Module Reviewer / confirmation thread"
  source_artifact: "docs/contract_test_reports/local_artifact_manifest_environment_profiles.md"
  implementation_handoff: "docs/implementation_handoffs/local_artifact_manifest_environment_profiles_comparison.md"
  branch: "codex/analytics-foundation"
  finding_fixed:
    - "CT-153-001 P1: `.env*` secret-surface checks only inspected `.env.local`, so real `.env` files could be missed."
  validation:
    - "py -m pytest -q tests\\test_check_local_environment.py -> 15 passed"
    - "py -m pytest -q tests\\test_check_secret_patterns.py tests\\test_check_protected_surfaces.py -> 76 passed, 1 skipped"
    - "py -m pytest -q tests\\test_analytics_local_app_config.py tests\\test_analytics_local_app_backend.py tests\\test_analytics_manual_jsonl_import.py -> 35 passed, 1 existing warning"
    - "py -m ruff check tools tests src -> passed"
    - "git diff --check -> passed"
  forbidden_scope_touched: false
  next_recommended_role: "Codex E confirmation"
```
