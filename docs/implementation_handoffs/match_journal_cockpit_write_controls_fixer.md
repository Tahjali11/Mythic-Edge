# Match Journal Cockpit Write Controls Fixer Handoff

## Role Performed

Codex D: Module Fixer.

## Source Issue And Tracker

- Issue: <https://github.com/Tahjali11/Mythic-Edge/issues/234>
- Tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/202>

## Source Contract And Review

- Contract: `docs/contracts/match_journal_cockpit_write_controls.md`
- Implementation handoff:
  `docs/implementation_handoffs/match_journal_cockpit_write_controls_comparison.md`
- Review artifact:
  `docs/contract_test_reports/match_journal_cockpit_write_controls.md`
- Constitution: `docs/agent_constitution.md`
- Module fixer rules: `docs/agent_threads/module_fixer.md`

## Finding Fixed

CT-234-001 P1: failed or unavailable Match Journal submit responses could still
clear unsaved frontend form input.

CT-234-002 P2: the focused frontend regression for failed submit preservation
was timing-sensitive and failed once in Codex E confirmation before passing on
rerun.

Fault category: frontend state-handling bug. The API helper correctly preserved
safe non-OK Match Journal envelopes, but the React form handlers cleared local
form state after any resolved submit envelope instead of only after a confirmed
successful persisted write.

Follow-up fault category: test synchronization bug. The regression clicked the
submit button after only waiting for the cockpit heading, which could race the
async history/journal readiness state that enables journal write controls.

## Fix Produced

`SetupStatusApp` journal mutation handlers now return a success boolean. The
success classifier treats only `status: "ok"` with no error codes as a saved
write. The cockpit form handlers clear note text, opponent labels, experiment
label, and display-correction inputs only when that boolean is true.

Submit result copy now says `Journal Update Not Saved` for non-success
envelopes instead of calling unavailable or failed writes saved.

The failed-submit preservation regression now waits for the relevant form
control to be enabled, enters the retry value, then waits for the submit button
to be enabled before clicking. This keeps the product assertions unchanged
while avoiding the disabled-control race observed by Codex E.

## Files Changed

- `frontend/src/App.tsx`
- `frontend/src/App.test.tsx`
- `docs/implementation_handoffs/match_journal_cockpit_write_controls_fixer.md`

This D pass did not change backend runtime, Match Journal service/repository,
parser, analytics schema, workbook, webhook, Apps Script, Sheets, OpenAI,
AI/coaching, or production behavior.

## Tests Changed

Added a focused frontend regression:

- `preserves Match Journal form input when sanitized failed submit envelopes resolve`

The test uses sanitized `status: "unavailable"` Match Journal envelopes that
resolve through the submit layer and proves these values remain available for
retry:

- journal note text;
- opponent manual label;
- opponent tier label;
- experiment label;
- display-only correction field;
- display-only correction value.

The test also verifies the failed submit result is visible as
`Journal Update Not Saved` and shows the safe `service_unavailable` code.

Follow-up update for CT-234-002:

- the regression now synchronizes on enabled form controls and enabled submit
  buttons before firing submit events.

## Validation Evidence

```powershell
for ($i = 1; $i -le 3; $i++) {
  npm --prefix frontend test -- --run src/App.test.tsx
}
# three consecutive focused runs passed, 33 tests each

npm --prefix frontend run typecheck
# passed

py -m pytest -q tests\test_match_journal_cockpit_ui_backend.py
# 12 passed, 1 Starlette/FastAPI testclient deprecation warning

py -m pytest -q tests\test_analytics_dev_app_launcher.py
# 10 passed

py -m pytest -q tests\test_analytics_local_app_backend.py tests\test_analytics_local_app_config.py
# 23 passed, 1 Starlette/FastAPI testclient deprecation warning

py -m pytest -q tests\test_match_journal_service.py tests\test_match_journal_repository.py tests\test_match_journal_schema.py
# 63 passed

npm --prefix frontend test -- --run
# 3 files passed, 61 tests passed

npm --prefix frontend run build
# passed; generated frontend/dist was removed afterward

py -m ruff check src tests tools
# passed

py tools\check_agent_docs.py
# passed, errors 0, warnings 0

git diff --check
# passed
```

## Pending Final Safety Checks

Completed after this handoff file was present:

```powershell
path-scoped protected-surface scan
# passed, forbidden 0, warnings 0

path-scoped secret/private-marker scan
# passed, forbidden 0, warnings 0

generated SQLite/database artifact sweep
# no output

Test-Path frontend\dist
# False
```

## Remaining Review Focus

Codex E should confirm:

- sanitized failed/unavailable submit envelopes preserve unsaved values;
- successful `ok` submit envelopes still clear only the saved form;
- failed submit result copy does not imply the write was saved;
- the browser still uses only `/api/journal/...`;
- no pilot-error, destructive, raw SQL, import/export/sync, reset, AI/coaching,
  workbook, webhook, Apps Script, Sheets, or production controls were added.

## Still Unverified

- Manual live-browser retry flow with a disposable app-data root.
- Real local app operation against the user's actual local app data root.
- GitHub Actions.
- Direct status API global CORS hardening, intentionally deferred by contract.
- Pilot-error browser controls, intentionally deferred by contract.

## Forbidden Scope Status

Forbidden scope touched: false.

## Next Recommended Role

Codex E: Module Reviewer / confirmation thread.

## Pasteable Next-Thread Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer / confirmation thread for issue #234.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/234

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/202

Branch:
codex/analytics-foundation

Contract:
docs/contracts/match_journal_cockpit_write_controls.md

Review artifact:
docs/contract_test_reports/match_journal_cockpit_write_controls.md

Fixer handoff:
docs/implementation_handoffs/match_journal_cockpit_write_controls_fixer.md

Confirm the Codex D fix for CT-234-001:
- failed or unavailable Match Journal submit responses preserve unsaved frontend form input;
- successful writes still clear only the saved form;
- failed submit result copy does not imply the write was saved;
- forbidden parser/runtime/analytics/workbook/webhook/App Script/Sheets/OpenAI/AI/coaching/production scope was not touched.

Lead with findings ordered by severity. If no blockers remain, recommend the next appropriate workflow role.
```

## workflow_handoff

```yaml
workflow_handoff:
  role_performed: "Codex D: Module Fixer"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/234"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/202"
  branch: "codex/analytics-foundation"
  source_artifact: "docs/contract_test_reports/match_journal_cockpit_write_controls.md"
  contract: "docs/contracts/match_journal_cockpit_write_controls.md"
  implementation_handoff: "docs/implementation_handoffs/match_journal_cockpit_write_controls_comparison.md"
  target_artifact: "docs/implementation_handoffs/match_journal_cockpit_write_controls_fixer.md"
  finding_fixed:
    - "CT-234-001 P1: failed or unavailable Match Journal submit responses no longer clear unsaved frontend form input."
    - "CT-234-002 P2: failed-submit preservation regression now waits for enabled journal controls before submitting."
  files_changed:
    - "frontend/src/App.tsx"
    - "frontend/src/App.test.tsx"
    - "docs/implementation_handoffs/match_journal_cockpit_write_controls_fixer.md"
  code_changed_or_tests_only: "code+tests"
  validation:
    - "npm --prefix frontend test -- --run src/App.test.tsx -> 33 passed on three consecutive focused runs"
    - "npm --prefix frontend run typecheck -> passed"
    - "py -m pytest -q tests\\test_match_journal_cockpit_ui_backend.py -> 12 passed, 1 warning"
    - "py -m pytest -q tests\\test_analytics_dev_app_launcher.py -> 10 passed"
    - "py -m pytest -q tests\\test_analytics_local_app_backend.py tests\\test_analytics_local_app_config.py -> 23 passed, 1 warning"
    - "py -m pytest -q tests\\test_match_journal_service.py tests\\test_match_journal_repository.py tests\\test_match_journal_schema.py -> 63 passed"
    - "npm --prefix frontend test -- --run -> 61 passed"
    - "npm --prefix frontend run build -> passed; frontend/dist removed afterward"
    - "py -m ruff check src tests tools -> passed"
    - "py tools\\check_agent_docs.py -> passed"
    - "git diff --check -> passed"
    - "path-scoped protected-surface scan -> passed, forbidden 0, warnings 0"
    - "path-scoped secret/private-marker scan -> passed, forbidden 0, warnings 0"
    - "generated SQLite/database artifact sweep -> no output"
    - "Test-Path frontend\\dist -> False"
  forbidden_scope_touched: false
  next_thread: "E"
  next_role: "Codex E: Module Reviewer / confirmation thread"
```
