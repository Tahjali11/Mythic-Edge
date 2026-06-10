# Private Local V1 Installation Wizard And First-Run Configuration - Contract Test Report

## Findings First

No remaining blocking findings.

| finding_id | severity | finding_lifecycle | finding_status | blocking_status | original_evidence | verification_evidence | next_route |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CT-314-001 | P2 | fixed_state_followup | fixed | not_blocking | Initial Codex E review found missing setup-helper tests for selected Player.log not-file and unreadable metadata cases required by the contract. | Codex D added `test_install_mode_blocks_player_log_directory_without_writing_config` and `test_install_mode_blocks_unreadable_player_log_metadata_without_writing_config`; `py -m pytest -q tests\test_private_local_v1_setup.py` passed with 16 tests. The tests verify blocked setup, no config/database writes, symbolic `<selected_player_log>` display, `contents_read=false`, `tailing_started=false`, and no raw path/body echo. | F |

## Fixed-State Verdict

CT-314-001 is confirmed fixed.

The D pass is test/handoff-only relative to the original #314 implementation package: it added the required setup-helper regression coverage and did not require runtime implementation changes. The full package still includes the earlier Codex C setup/config code changes, but this confirmation pass found no new protected-surface or privacy regression.

## Role Performed

Codex E: Module Reviewer / confirmation thread.

## Issue / Tracker Reviewed

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/314
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/136
- Issue state checked with GitHub CLI: #314 open
- Tracker state checked with GitHub CLI: #136 open
- Branch reviewed: `codex/analytics-foundation`

## Contract And Handoffs Reviewed

- Contract: `docs/contracts/setup_app_private_local_v1_installation_wizard.md`
- Implementation handoff: `docs/implementation_handoffs/setup_app_private_local_v1_installation_wizard_comparison.md`
- Fixer handoff: `docs/implementation_handoffs/setup_app_private_local_v1_installation_wizard_fixer.md`
- Reviewer guidance: `docs/agent_constitution.md`, `docs/agent_threads/contract_test.md`, `docs/templates/contract_test_report.md`

## Files Reviewed

- `docs/contracts/setup_app_private_local_v1_installation_wizard.md`
- `docs/implementation_handoffs/setup_app_private_local_v1_installation_wizard_comparison.md`
- `docs/implementation_handoffs/setup_app_private_local_v1_installation_wizard_fixer.md`
- `docs/contract_test_reports/setup_app_private_local_v1_installation_wizard.md`
- `src/mythic_edge_parser/local_app/config.py`
- `tools/dev_app/private_local_v1_setup.py`
- `tools/dev_app/setup_private_local_v1.ps1`
- `tests/test_analytics_local_app_config.py`
- `tests/test_private_local_v1_setup.py`

## Contract Matches

- Setup-helper tests now cover selected Player.log path that is a directory/not-file.
- Setup-helper tests now cover selected Player.log metadata denial via a focused monkeypatch.
- Both cases block before config writes and before SQLite database creation.
- Both cases keep setup result/report display symbolic with `<selected_player_log>`.
- Both cases assert `contents_read=false` and `tailing_started=false`.
- The unreadable-metadata test asserts the stable `player_log_metadata_denied` code and safe warning label.
- Check mode remains metadata-only and non-mutating.
- BOM-tolerant config reads and UTF-8-without-BOM config writes remain covered.
- No live capture auto-start was added.
- No parser/runtime, analytics schema/migration/ingest, workbook/webhook/App Script/Sheets, OpenAI/AI/coaching, Line Tracer, or production behavior changed.

## Remaining Mismatches

- None found.

## Missing Tests Or Safeguards

- No blocking missing tests remain for this reviewed #314 slice.
- Still unverified by design: full interactive setup wizard prompt, generic current-user Player.log detector, browser first-run config editing, real default private-local-v1 root, and live browser/launcher proof. These remain outside the D confirmation scope and should not be claimed as complete unless later work covers or explicitly defers them.

## Validation Run And Result

```powershell
git status --short --branch --untracked-files=all
git diff --name-status
gh issue view 314 --repo Tahjali11/Mythic-Edge --json number,title,state,url
gh issue view 136 --repo Tahjali11/Mythic-Edge --json number,title,state,url
py -m pytest -q tests\test_private_local_v1_setup.py
py -m pytest -q tests\test_analytics_local_app_config.py
py -m pytest -q tests\test_analytics_dev_app_launcher.py tests\test_analytics_local_app_backend.py
py -m ruff check src tests tools
git diff --check
py tools\check_agent_docs.py
rg -n "test_install_mode_blocks_player_log_directory_without_writing_config|test_install_mode_blocks_unreadable_player_log_metadata_without_writing_config|player_log_not_file|player_log_metadata_denied|<selected_player_log>|contents_read|tailing_started" tests\test_private_local_v1_setup.py
```

Results:

- Branch/status: `codex/analytics-foundation...origin/codex/analytics-foundation`.
- Issue #314: open.
- Tracker #136: open.
- `py -m pytest -q tests\test_private_local_v1_setup.py`: passed, 16 tests.
- `py -m pytest -q tests\test_analytics_local_app_config.py`: passed, 22 tests.
- `py -m pytest -q tests\test_analytics_dev_app_launcher.py tests\test_analytics_local_app_backend.py`: passed, 39 tests, 1 existing FastAPI/Starlette warning.
- `py -m ruff check src tests tools`: passed.
- `git diff --check`: passed with the existing PowerShell line-ending normalization warning for `tools/dev_app/setup_private_local_v1.ps1`.
- `py tools\check_agent_docs.py`: passed, errors 0, warnings 0.
- Path-scoped protected-surface scan: passed, forbidden 0, warnings 0.
- Path-scoped secret/private-marker scan: passed, forbidden 0, warnings 0.

## Protected-Surface Status

Passed, forbidden 0, warnings 0. Review found no parser/runtime, analytics schema/migration/ingest, live capture, workbook/webhook/App Script/Sheets, OpenAI/AI/coaching, Line Tracer, or production behavior change from the D confirmation slice.

## Secret / Private-Marker Status

Passed, forbidden 0, warnings 0. Review found no raw Player.log content, raw JSONL, generated SQLite contents, runtime artifacts, workbook exports, secrets, credentials, API keys, provider keys, env values, or local-only artifacts exposed by the D fix.

## Generated / Private Artifact Status

No generated/private artifacts are kept in Git status. Validation used pytest temporary directories only.

## Drift Notes

- Issue lifecycle drift: #314 remains open and should not be closed from this review.
- Tracker lifecycle drift: #136 remains open and should not be marked complete from this review.
- Scope note: this reviewed package remains a narrow setup/config foundation, not the full interactive setup wizard or browser first-run flow.

## Forbidden Scope Touched

False.

## Recommendation

Route to Codex F for focused submission of the reviewed #314 setup/config package.

## Next Workflow Action

Next role: Codex F / Module Submitter.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex F: Module Submitter for issue #314.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/314

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/136

Branch:
codex/analytics-foundation

Contract:
docs/contracts/setup_app_private_local_v1_installation_wizard.md

Implementation handoff:
docs/implementation_handoffs/setup_app_private_local_v1_installation_wizard_comparison.md

Fixer handoff:
docs/implementation_handoffs/setup_app_private_local_v1_installation_wizard_fixer.md

Contract-test report:
docs/contract_test_reports/setup_app_private_local_v1_installation_wizard.md

Goal:
Stage only the reviewed #314 files, commit, push, and open/update a draft PR targeting the approved integration branch. Do not include unrelated local work, generated artifacts, raw logs, app-data, secrets, or private artifacts.

Approved files:
- docs/contracts/setup_app_private_local_v1_installation_wizard.md
- docs/implementation_handoffs/setup_app_private_local_v1_installation_wizard_comparison.md
- docs/implementation_handoffs/setup_app_private_local_v1_installation_wizard_fixer.md
- docs/contract_test_reports/setup_app_private_local_v1_installation_wizard.md
- src/mythic_edge_parser/local_app/config.py
- tools/dev_app/private_local_v1_setup.py
- tools/dev_app/setup_private_local_v1.ps1
- tests/test_analytics_local_app_config.py
- tests/test_private_local_v1_setup.py

Before staging:
- Confirm git status and branch.
- Confirm no generated/private/local artifacts are present.
- Verify the path-scoped protected-surface and secret/private-marker scans remain clean over the approved files.

Do not:
- stage unrelated files
- target main
- close #314 or tracker #136
- use or mutate the real default %LOCALAPPDATA%\MythicEdge root
- read, copy, hash, tail, summarize, store, or expose raw Player.log contents
- change parser behavior, parser final reconciliation, analytics schema/migrations/ingest, live capture behavior, workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production behavior

Final output:
- branch
- commit hash
- PR URL
- target branch
- files submitted
- validation summary
- remaining risks
- workflow_handoff block
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/314"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/136"
  completed_thread: "E"
  next_thread: "F"
  branch: "codex/analytics-foundation"
  contract_artifact: "docs/contracts/setup_app_private_local_v1_installation_wizard.md"
  implementation_handoff: "docs/implementation_handoffs/setup_app_private_local_v1_installation_wizard_comparison.md"
  fixer_handoff: "docs/implementation_handoffs/setup_app_private_local_v1_installation_wizard_fixer.md"
  review_artifact: "docs/contract_test_reports/setup_app_private_local_v1_installation_wizard.md"
  findings_confirmed_fixed:
    - "CT-314-001 P2: setup-helper tests now cover selected Player.log not-file and unreadable metadata cases."
  validation:
    - "setup-helper pytest -> passed, 16 tests"
    - "local app config pytest -> passed, 22 tests"
    - "launcher/backend pytest -> passed, 39 tests, 1 existing FastAPI/Starlette warning"
    - "ruff -> passed"
    - "git diff --check -> passed with existing PowerShell line-ending warning"
    - "agent docs check -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
  protected_surface_status: "passed, forbidden 0, warnings 0"
  secret_private_marker_status: "passed, forbidden 0, warnings 0"
  generated_artifacts_kept: false
  forbidden_scope_touched: false
  recommendation: "Route to Codex F."
```
