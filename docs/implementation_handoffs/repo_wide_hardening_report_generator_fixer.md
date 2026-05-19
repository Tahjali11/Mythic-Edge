# Repo-Wide Hardening Report Generator Fixer Handoff

## Role Performed

Codex D: Module Fixer.

## Issue And Tracker

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/100
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/82
- Branch: `codex/repo-wide-hardening-run`

## Source Artifacts

- Contract: `docs/contracts/repo_wide_hardening_report_generator.md`
- Implementation handoff: `docs/implementation_handoffs/repo_wide_hardening_report_generator_comparison.md`
- Review report: `docs/contract_test_reports/repo_wide_hardening_report_generator.md`

## Finding Fixed

P1: bare Google workbook/document/Apps Script deployment IDs in
operator-supplied manifest values could pass through report rendering when they
were not part of a Docs/Sheets URL or a labeled field such as
`spreadsheet_id=...` or `deployment_id=...`.

## Files Changed

- `tools/generate_hardening_report.py`
- `tests/test_hardening_report_generator.py`
- `docs/implementation_handoffs/repo_wide_hardening_report_generator_fixer.md`

Existing issue #100 package files remain present in the working tree. The
unrelated untracked skill-installation files remain excluded from this fixer
scope:

- `docs/codex_skill_bundle.md`
- `docs/codex_skills/`
- `tools/install_codex_skills.py`
- `tools/install_mythic_edge_skill.py`

## Fix Summary

Added a focused regression test that supplies standalone Google-style document,
workbook, and Apps Script deployment IDs in rendered manifest fields. The test
also includes a rendered 40-character git SHA to guard against over-redacting
normal PR metadata.

Updated `redact_text()` with a narrow bare-Google-ID candidate pass:

- Apps Script deployment IDs beginning with `AKfycb` are redacted.
- Long URL-safe Google Drive-style IDs with mixed case and Google-like shape
  are redacted.
- 40-character git SHAs are preserved.

The implementation chooses redaction rather than deterministic exit `2` because
the values can be safely removed before rendering while preserving report-only
behavior.

## Tests Added Or Updated

- Added `test_report_redacts_standalone_google_ids_from_manifest_values()` in
  `tests/test_hardening_report_generator.py`.

Focused failure before the implementation patch:

```text
py -m pytest -q tests\test_hardening_report_generator.py
result: failed; standalone document ID remained in output
```

Focused pass after the implementation patch:

```text
py -m pytest -q tests\test_hardening_report_generator.py
10 passed
```

## Validation

```text
py -m pytest -q tests\test_hardening_report_generator.py tests\test_select_validation.py
36 passed
```

```text
py tools\generate_hardening_report.py
passed; printed Markdown to stdout
```

```text
py tools\generate_hardening_report.py --output docs\contract_test_reports\repo_wide_hardening_status_report.md
passed; wrote the approved status report path
```

```text
py -m ruff check src tests tools
All checks passed!
```

```text
py tools\check_secret_patterns.py --base origin/codex/repo-wide-hardening-run
result: passed; scanned_paths: 0; forbidden: 0; warnings: 0
```

```text
path-scoped secret/private-marker scan over the three Codex D touched paths
result: passed; scanned_paths: 3; forbidden: 0; warnings: 0
```

```text
py tools\check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run
result: passed; changed_paths: 0; forbidden: 0; warnings: 0
```

```text
py tools\check_surface_authorization.py --base origin/codex/repo-wide-hardening-run --authorization-file issue=.tmp\issue-100.md --authorization-file contract=docs\contracts\repo_wide_hardening_report_generator.md --authorization-file handoff=docs\implementation_handoffs\repo_wide_hardening_report_generator_comparison.md
authorization_status: ok; changed_paths: 0
```

Temporary `.tmp\issue-100.md` authorization evidence was created for the
surface-authorization command and removed afterward.

```text
py tools\select_validation.py --base origin/codex/repo-wide-hardening-run
selection_status: ok; zero_changed_paths advisory
```

```text
git diff --check
passed
```

## Forbidden Scope Status

No parser/runtime/workbook/webhook/Apps Script behavior changed. The generator
still does not execute validation commands, query GitHub live, decide merge or
deploy readiness, close issues, update the tracker, or change CI behavior.

## Remaining Risks

- Independent Codex E confirmation is still needed.
- Broad changed-file hardening gates report zero changed paths because the
  issue #100 package is still untracked relative to the selected base.
- Future operator manifests may contain unusual Google ID shapes not covered by
  the conservative bare-ID heuristic; labeled IDs and Google URLs remain
  covered by the existing redaction rules.

## Next Recommended Role

Codex E: Module Reviewer / confirmation thread.

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/100"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/82"
  completed_thread: "D"
  next_thread: "E"
  next_role: "Codex E: Module Reviewer / confirmation thread"
  source_artifact: "docs/implementation_handoffs/repo_wide_hardening_report_generator_fixer.md"
  review_artifact: "docs/contract_test_reports/repo_wide_hardening_report_generator.md"
  contract: "docs/contracts/repo_wide_hardening_report_generator.md"
  branch: "codex/repo-wide-hardening-run"
  fixed_findings:
    - "P1 bare Google workbook/document/deployment IDs in manifest-rendered text are now redacted."
  validation:
    - "py -m pytest -q tests\\test_hardening_report_generator.py tests\\test_select_validation.py -> 36 passed"
    - "py tools\\generate_hardening_report.py -> passed"
    - "py tools\\generate_hardening_report.py --output docs\\contract_test_reports\\repo_wide_hardening_status_report.md -> passed"
    - "py -m ruff check src tests tools -> passed"
    - "py tools\\check_secret_patterns.py --base origin/codex/repo-wide-hardening-run -> passed"
    - "path-scoped secret/private-marker scan over Codex D touched paths -> passed"
    - "py tools\\check_protected_surfaces.py --base origin/codex/repo-wide-hardening-run -> passed"
    - "py tools\\check_surface_authorization.py --base origin/codex/repo-wide-hardening-run --authorization-file issue=.tmp\\issue-100.md --authorization-file contract=docs\\contracts\\repo_wide_hardening_report_generator.md --authorization-file handoff=docs\\implementation_handoffs\\repo_wide_hardening_report_generator_comparison.md -> ok"
    - "py tools\\select_validation.py --base origin/codex/repo-wide-hardening-run -> ok"
    - "git diff --check -> passed"
  stop_conditions:
    - "Do not stage unrelated untracked skill-installation files."
    - "Do not broaden beyond P1 redaction confirmation."
    - "Do not change parser/runtime/workbook/webhook/Apps Script behavior."
    - "Do not query GitHub live from the generator or make it run validation commands."
    - "Do not decide merge/deploy readiness, close issues, or mark tracker #82 complete."
```
