# Pre-v1 Clean-install Transition Comparison

## Role performed

Codex C: Module Implementer / comparison thread.

## Source issue reviewed

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/227
- Related completed issue: https://github.com/Tahjali11/Mythic-Edge/issues/153

## Contract used

- `docs/contracts/pre_v1_clean_install_transition.md`

## Branch and git status

- Branch: `codex/analytics-foundation`
- Initial status: branch aligned with `origin/codex/analytics-foundation`; contract was untracked.
- No files were staged, committed, pushed, merged, or submitted.

## Files inspected

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/implementation.md`
- `docs/templates/implementation_handoff.md`
- `docs/contracts/pre_v1_clean_install_transition.md`
- `docs/local_artifacts_manifest.json`
- `tools/check_local_environment.py`
- `tests/test_check_local_environment.py`
- `docs/contract_test_reports/local_artifact_manifest_environment_profiles.md`
- `tools/check_secret_patterns.py`
- `tools/check_protected_surfaces.py`
- local app adjacency tests for config, backend, and developer launcher behavior

## Current behavior compared to contract

The completed issue #153 artifacts already provided a manifest-driven local environment checker, redacted display paths, no content reads for private/generated artifact families, symbolic app-data reporting, and focused tests for secret/private and protected-surface behavior.

The remaining gap was transition readiness. The `clean_clone` profile treated tracked `.env.example` as part of the broad `.env*` secret-adjacent pattern, which blocked the profile even though the contract defines exact tracked `.env.example` as repo-owned template source. The repo also did not have a `clean_install_transition_audit` profile for report-only Git metadata and local artifact readiness checks.

## Implementation option chosen

Extend the existing #153 manifest/checker/test surface instead of adding a new transition tool. This keeps the transition audit report-only, reuses the established redaction and no-content-read behavior, and avoids cleanup, migration, clone, app startup, parser startup, import, `.gitignore`, CI, or runtime behavior changes.

## Files changed

- `docs/local_artifacts_manifest.json`
- `tools/check_local_environment.py`
- `tests/test_check_local_environment.py`
- `docs/implementation_handoffs/pre_v1_clean_install_transition_comparison.md`

## Exact manifest sections changed

- Added `env_example_template` to the `clean_clone` profile as a required repo-owned source artifact.
- Added `clean_install_transition_audit` as a report-only profile.
- Added Git metadata artifacts for working-tree state, branch upstream count, stash count, and untracked-unignored count.
- Added `env_example_template` artifact policy:
  - exact tracked `.env.example` is allowed;
  - content is not read or printed;
  - modified tracked `.env.example` requires review;
  - untracked `.env.example` remains handled by the broad `.env*` never-commit policy;
  - real `.env`, `.env.local`, `.env.production`, and other non-example variants remain blocked by the existing `env_files` policy.

## Exact checker sections changed

- Added a `git_metadata` path-scope evaluator for report-only transition metadata.
- Added count-only working-tree, upstream ahead/behind, stash, and untracked-unignored checks.
- Added tracked `.env.example` special handling so exact tracked template source does not trip the broad `.env*` finding.
- Added modified tracked `.env.example` warning behavior.
- Kept all Git metadata output count-only; no changed paths, filenames, stash text, file contents, private payloads, or local machine paths are printed.

## Exact test sections changed

- Added `clean_install_transition_audit` to the required profile coverage.
- Added focused tests proving:
  - tracked `.env.example` is accepted in `clean_clone`;
  - untracked `.env.example` requires review and does not print values;
  - modified tracked `.env.example` warns and does not print values;
  - real `.env`, `.env.local`, and `.env.production` remain blocked by existing coverage;
  - transition audit exits successfully as report-only;
  - transition audit reports dirty, stash, and untracked state by count only;
  - private filenames, stash text, and private file contents are not printed.

## Code/tests/docs status

- Code changed: yes, checker-only.
- Tests changed: yes, focused checker tests.
- Docs changed: yes, manifest and implementation handoff.
- Runtime behavior changed: no.
- Parser, analytics, local app, workbook, webhook, Apps Script, Sheets, OpenAI, AI, coaching, and production behavior changed: no.

## Validation run

- `py -m pytest -q tests\test_check_local_environment.py` -> passed, 20 passed.
- `py -m ruff check tools\check_local_environment.py tests\test_check_local_environment.py` -> passed.
- `py tools\check_local_environment.py --profile clean_clone --format json` -> exited 0; status warning; blocked 0; tracked `.env.example` accepted.
- `py tools\check_local_environment.py --profile clean_install_transition_audit --format json` -> exited 0; status warning; blocked 0; report-only Git/local artifact summary.
- `py -m pytest -q tests\test_check_secret_patterns.py tests\test_check_protected_surfaces.py` -> passed, 76 passed, 1 skipped for platform symlink support.
- `py -m pytest -q tests\test_analytics_local_app_config.py tests\test_analytics_local_app_backend.py tests\test_analytics_dev_app_launcher.py` -> passed, 31 passed, 1 third-party deprecation warning.
- `py -m ruff check tools tests src` -> passed.
- `git diff --check` -> passed.
- `py tools\check_agent_docs.py` -> passed.
- Path-scoped protected-surface scan over contract, manifest, checker, tests, and handoff -> passed, forbidden 0, warnings 0.
- Path-scoped secret/private-marker scan over contract, manifest, checker, tests, and handoff -> warning, forbidden 0, warnings 7 from pre-existing manifest placeholder artifact-path policy entries; the warning lines were not introduced by this change.
- ASCII/trailing-whitespace/final-newline checks for the untracked contract and new handoff -> passed.

## `.env.example` policy result

Exact tracked `.env.example` is now treated as repo-owned template source for `clean_clone` and `clean_install_transition_audit`. The checker does not read or print its values. Untracked or locally modified `.env.example` requires manual review. Real `.env*` variants other than exact tracked `.env.example` remain blocked by the never-commit policy.

## Protected-surface status

No parser, runtime, analytics runtime, local app runtime, workbook, webhook, Apps Script, Sheets, AI, production, fixture, snapshot, baseline, generated-data, or CI gate behavior was changed.

## Secret/private-marker status

No secret values, private payload contents, raw local artifact contents, stash contents, raw paths, webhook URLs, workbook identifiers, or credential material were read, printed, copied, sanitized, uploaded, imported, hashed, moved, deleted, or committed. The path-scoped secret/private-marker scan returned zero forbidden findings and seven warnings from pre-existing manifest placeholder artifact-path policy entries.

## Generated/private artifact status

No generated/private artifact was created, modified, read for contents, copied, cleaned, archived, imported, uploaded, hashed, deleted, or committed. No fresh clone was created. No local app, parser, import, or cleanup workflow was started.

## Remaining risks and unverified layers

- The transition audit is report-only and does not decide whether a checkout can be retired.
- The current machine still has local/generated artifact families present; the checker reports them symbolically and does not inspect contents.
- `.gitignore` remains unchanged by contract. The broad `.env*` policy can still report ignore-policy warnings when no real env file exists.
- Live workbook state, deployed Apps Script state, production behavior, and any future clean-install execution remain unverified and out of scope.
- Issue #227 remains open; no PR was opened.

## Forbidden scope touched

No forbidden scope was touched. No files were deleted, moved, renamed, archived, copied, sanitized, uploaded, imported, hashed, cleaned, staged, committed, pushed, or merged. No `.gitignore` or CI gates were edited.

## Next recommended role

Codex E: Module Reviewer / contract-test thread.

## Pasteable Codex E prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / contract-test thread for issue #227.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/227

Related completed issue:
https://github.com/Tahjali11/Mythic-Edge/issues/153

Branch:
codex/analytics-foundation

Contract:
docs/contracts/pre_v1_clean_install_transition.md

Implementation handoff:
docs/implementation_handoffs/pre_v1_clean_install_transition_comparison.md

Goal:
Review the Codex C implementation against the pre-v1 clean-install transition contract. Verify that the change is limited to report-only manifest/checker/test behavior, accepts exact tracked `.env.example` as repo-owned template source, keeps real `.env*` variants blocked, adds the clean-install transition audit profile, and does not perform cleanup, clone creation, app startup, parser startup, import, artifact migration, `.gitignore`, CI, runtime, workbook, webhook, Apps Script, Sheets, AI, coaching, or production changes.

Review:
- Lead with findings, ordered by severity.
- Confirm whether the implementation satisfies the contract.
- Check that `.env.example` handling does not read or print values.
- Check that transition audit Git metadata is count-only and does not print changed paths, filenames, stash text, private payloads, or local machine paths.
- Check that generated/private artifact families remain symbolic/report-only and are not read, copied, deleted, hashed, imported, uploaded, or committed.
- Check that parser/runtime/analytics/local app/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior is unchanged.
- Check that `.gitignore` and CI gates were not edited.
- Preserve unrelated worktree changes.

Validation to run:
git status --short --branch --untracked-files=all
py -m pytest -q tests\test_check_local_environment.py
py tools\check_local_environment.py --profile clean_clone --format json
py tools\check_local_environment.py --profile clean_install_transition_audit --format json
py -m pytest -q tests\test_check_secret_patterns.py tests\test_check_protected_surfaces.py
py -m pytest -q tests\test_analytics_local_app_config.py tests\test_analytics_local_app_backend.py tests\test_analytics_dev_app_launcher.py
py -m ruff check tools tests src
py tools\check_agent_docs.py
git diff --check

Also run path-scoped protected-surface and secret/private-marker scans over:
docs/contracts/pre_v1_clean_install_transition.md
docs/local_artifacts_manifest.json
tools/check_local_environment.py
tests/test_check_local_environment.py
docs/implementation_handoffs/pre_v1_clean_install_transition_comparison.md

Do not:
- delete, move, rename, archive, copy, sanitize, upload, import, hash, clean, or commit local/private/generated artifacts;
- create a fresh clone;
- rename the current checkout;
- run destructive cleanup commands;
- start local app, parser, import, or cleanup workflows;
- inspect secret values or private payload contents;
- change parser/runtime/analytics/local app/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior;
- edit `.gitignore` or CI gates unless explicitly rerouted by the user;
- stage, commit, push, open a PR, merge, target main, or close #227 unless explicitly asked.

Final handoff must include:
- role performed;
- issue and related issue used;
- contract and implementation handoff reviewed;
- files reviewed;
- findings, if any, ordered by severity;
- validation run and result;
- `.env.example` policy verdict;
- transition-audit report-only verdict;
- protected-surface status;
- secret/private-marker status;
- generated/private artifact status;
- whether forbidden scope was touched;
- whether issue #227 is ready for submitter review;
- next recommended role;
- workflow_handoff block.
```

## workflow_handoff

```yaml
workflow_handoff:
  role_performed: "Codex C: Module Implementer / comparison thread"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/227"
  related_completed_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/153"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "GitHub issue #227 and completed #153 manifest/checker artifacts"
  contract_artifact: "docs/contracts/pre_v1_clean_install_transition.md"
  target_artifact: "docs/implementation_handoffs/pre_v1_clean_install_transition_comparison.md"
  branch: "codex/analytics-foundation"
  risk_tier: "High"
  validation:
    - "py -m pytest -q tests\\test_check_local_environment.py -> passed, 20 passed"
    - "py -m ruff check tools\\check_local_environment.py tests\\test_check_local_environment.py -> passed"
    - "py tools\\check_local_environment.py --profile clean_clone --format json -> exited 0, blocked 0"
    - "py tools\\check_local_environment.py --profile clean_install_transition_audit --format json -> exited 0, blocked 0"
    - "py -m pytest -q tests\\test_check_secret_patterns.py tests\\test_check_protected_surfaces.py -> passed, 76 passed, 1 skipped"
    - "py -m pytest -q tests\\test_analytics_local_app_config.py tests\\test_analytics_local_app_backend.py tests\\test_analytics_dev_app_launcher.py -> passed, 31 passed"
    - "py -m ruff check tools tests src -> passed"
    - "git diff --check -> passed"
    - "py tools\\check_agent_docs.py -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> warning, forbidden 0, warnings 7 pre-existing manifest placeholder artifact-path policy entries"
    - "ASCII/trailing-whitespace/final-newline checks for untracked contract and handoff -> passed"
  remaining_unverified:
    - "Codex E review"
    - "Actual clean-install execution"
    - "Checkout retirement decision"
    - "Live workbook state"
    - "Deployed Apps Script state"
    - "Production behavior"
  stop_conditions:
    - "Do not delete, move, rename, archive, copy, sanitize, upload, import, hash, clean, or commit local/private/generated artifacts."
    - "Do not create a fresh clone, rename the current checkout, run destructive cleanup commands, or start local app/parser/import workflows."
    - "Do not inspect secret values or private payload contents."
    - "Do not change parser/runtime/analytics/local app/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior."
    - "Do not edit .gitignore or CI gates unless explicitly rerouted by the user."
    - "Do not target main or close #227."
```
