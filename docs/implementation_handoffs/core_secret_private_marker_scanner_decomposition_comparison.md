# Core Secret/Private Marker Scanner Decomposition Implementation Handoff

## Issue

<https://github.com/Tahjali11/Mythic-Edge/issues/684>

## Tracker

<https://github.com/Tahjali11/Mythic-Edge/issues/568>

## Contracts And Evidence

- Decision packet:
  `docs/contracts/core_secret_private_marker_scanner_decomposition_decision_packet.md`
- Evidence preflight:
  `docs/contracts/core_secret_private_marker_scanner_fresh_ars_refactor_evidence_preflight.md`
- Fresh scoped evidence issue:
  <https://github.com/Tahjali11/Mythic-Edge-Automation-Artifacts/issues/132>
- Fresh scoped evidence PR:
  <https://github.com/Tahjali11/Mythic-Edge-Automation-Artifacts/pull/133>
- Fresh scoped evidence merge commit:
  `67d14589728253b3cbde53b198f2ee1f9a23091f`
- Evidence route: `fresh_scoped_ars_evidence`
- Evidence status for #681: `precondition_satisfied`
- Implementation authorization: owner explicitly routed implementation after
  the evidence precondition was satisfied.

## Internal Project Area

Quality and Governance local advisory checks.

## Truth Owner

`tools/check_secret_patterns.py` remains the public scanner command and owns the
scanner command surface, scan modes, result vocabulary, report rendering,
safe-excerpt/no-echo behavior, and exit-code behavior.

## Bridge-Code Status

`not_bridge_code`

## Role Performed

Codex C: Module Implementer.

## What Changed

Implemented a behavior-preserving same-repo decomposition of the
secret/private marker scanner.

The public command remains:

```bash
python3 tools/check_secret_patterns.py
```

The scanner's public CLI options, scan modes, report heading, result values,
severity values, finding category behavior, stdout/stderr routing, and exit-code
semantics were not intentionally changed.

## Files Changed

- `tools/check_secret_patterns.py`
- `tools/check_secret_patterns_detectors.py`
- `tools/check_secret_patterns_models.py`
- `tests/test_check_secret_patterns.py`
- `docs/implementation_handoffs/core_secret_private_marker_scanner_decomposition_comparison.md`

## Code Changed

Runtime code changed only inside the repo-local advisory scanner surface.

- `tools/check_secret_patterns.py` is now the compatibility facade and public
  CLI entrypoint. It keeps path normalization, file scanning, git path
  collection, report rendering, parser construction, and `main()`.
- `tools/check_secret_patterns_detectors.py` now owns regex vocabulary,
  placeholder/sanitized-fixture policy helpers, safe excerpt construction,
  finding construction, detector family helpers, and `scan_text()`.
- `tools/check_secret_patterns_models.py` now owns severity/result/mode
  constants plus the `Finding` and `ScanResult` dataclasses.

## Tests Added Or Updated

- Added `test_facade_preserves_scanner_contract_symbols` to verify the
  compatibility facade still exposes key scanner constants, dataclasses, and
  `scan_text()` through `tools/check_secret_patterns.py`.

Existing focused scanner tests continue to cover:

- CLI usage errors;
- git diff path collection;
- stdin path scanning;
- `--all` advisory exit behavior;
- webhook and credential redaction;
- private local path redaction;
- raw Player.log marker handling;
- artifact payload categories;
- skip/error handling;
- deterministic finding ordering.

## Interface Changes

No intended external interface changes.

Preserved:

- public command path: `tools/check_secret_patterns.py`;
- CLI options: `--base`, `--repo-root`, `--paths-from-stdin`, `--all`;
- scan modes: `changed-files`, `paths-from-stdin`, `all-repo-advisory`;
- result values: `passed`, `warning`, `failed`, `error`;
- severity values: `allowed`, `warning`, `forbidden`;
- report heading: `Secret / Private Marker Scan`;
- exit-code behavior;
- stdout/stderr routing;
- safe-excerpt and no-echo behavior.

Internal helper modules were added behind the existing facade. The facade
re-exports the old scanner constants, models, detector helpers, and `scan_text`
for compatibility with existing focused tests and local imports.

## Contracted Area Status

Stayed inside the contracted same-repo, behavior-preserving scanner
decomposition boundary.

Not changed:

- parser behavior;
- EventBus behavior;
- API payloads;
- frontend behavior;
- live-capture behavior;
- workbook or webhook behavior;
- Apps Script behavior;
- CI behavior;
- scanner CLI behavior;
- scanner output schema;
- scanner exit-code semantics.

## Governance Checklist Outcome

- Public-safe/no-echo boundary: preserved by move-only extraction and focused
  scanner tests.
- Vocabulary and example coherence: preserved; no new finding categories,
  severity values, or result values.
- Authority/readiness semantics: preserved; no readiness, no-secret,
  security-assurance, privacy-assurance, or parser-truth claim.
- Fail-closed schema or validator checks: not applicable; this is a scanner
  code decomposition, not a schema or validator authority change.
- Protected-surface rollout phase: same-repo helper decomposition only.

## Validation Run

Baseline before edits:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q tests/test_check_secret_patterns.py
PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile tools/check_secret_patterns.py tests/test_check_secret_patterns.py
PYTHONDONTWRITEBYTECODE=1 python3 -m ruff check tools/check_secret_patterns.py tests/test_check_secret_patterns.py
printf 'tools/check_secret_patterns.py\ntests/test_check_secret_patterns.py\n' | PYTHONDONTWRITEBYTECODE=1 python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
```

Final validation:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q tests/test_check_secret_patterns.py
PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile tools/check_secret_patterns.py tools/check_secret_patterns_detectors.py tools/check_secret_patterns_models.py tests/test_check_secret_patterns.py
PYTHONDONTWRITEBYTECODE=1 python3 -m ruff check tools/check_secret_patterns.py tools/check_secret_patterns_detectors.py tools/check_secret_patterns_models.py tests/test_check_secret_patterns.py
printf 'tools/check_secret_patterns.py\ntools/check_secret_patterns_detectors.py\ntools/check_secret_patterns_models.py\ntests/test_check_secret_patterns.py\n' | PYTHONDONTWRITEBYTECODE=1 python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
PYTHONDONTWRITEBYTECODE=1 python3 tools/check_secret_patterns.py --base origin/main
PYTHONDONTWRITEBYTECODE=1 python3 tools/check_secret_patterns.py --all
git diff --check
printf '<changed paths>' | PYTHONDONTWRITEBYTECODE=1 python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '<changed paths>' | PYTHONDONTWRITEBYTECODE=1 python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
printf '<changed paths>' | PYTHONDONTWRITEBYTECODE=1 python3 tools/select_validation.py --base origin/main --paths-from-stdin --format text
PYTHONDONTWRITEBYTECODE=1 python3 tools/check_agent_docs.py
PYTHONDONTWRITEBYTECODE=1 python3 -m ruff check src tests tools
PYTHONDONTWRITEBYTECODE=1 python3 tools/run_pyright_advisory_report.py
git diff --no-index --check /dev/null tools/check_secret_patterns_detectors.py
git diff --no-index --check /dev/null tools/check_secret_patterns_models.py
git diff --no-index --check /dev/null docs/implementation_handoffs/core_secret_private_marker_scanner_decomposition_comparison.md
python3 file hygiene check for ASCII, final newline, and CRLF on changed files
```

Observed results:

- Focused scanner tests: `24 passed`.
- `py_compile`: passed.
- Ruff on touched scanner/test files: passed.
- Full Ruff on `src tests tools`: passed.
- Path-scoped scanner over changed files: exit `0`, result `warning`, 0
  forbidden findings, expected warnings only from scanner/test policy text.
- Protected-surface gate over changed files: passed.
- Validation selector over changed files: `selection_status: ok`.
- Agent docs checker: passed.
- Changed-file scanner from `origin/main`: exit `0`, result `passed`, 0
  scanned paths because changed files are currently untracked until staging.
- `--all` advisory scan: exit `0`; result remains advisory and reported
  pre-existing forbidden/warning counts across the full repo. This was not
  treated as a no-secret or cleanliness claim.
- Pyright advisory report: exit `0` from the advisory wrapper, Pyright
  `exit_code: 1`, `status: advisory_findings`, 412 type findings, 0 local
  resolver noise, 0 tooling config blockers. This is advisory and non-blocking
  under current repo policy.
- Normal `git diff --check`: passed.
- New-file no-index whitespace checks printed no errors. They returned `1`
  because each new file differs from `/dev/null`.
- File hygiene check for ASCII, final newline, and CRLF: passed for changed
  files.

## Still Unverified

- No CI was run in GitHub from this local implementation.
- No private evidence, live data, raw logs, workbook exports, app-data, failed
  posts, runtime artifacts, generated private artifacts, or secrets were read.
- This implementation does not prove repository-wide no-secret or
  no-private-data status.

## Reviewer Focus

Ask Codex E to pay special attention to:

- whether the extraction is behavior-preserving;
- whether `tools/check_secret_patterns.py` remains the public CLI facade;
- whether helper-module imports work both when the file is imported by tests and
  when executed as a script;
- whether the new helper modules create any scanner-policy self-scan gap;
- whether no scanner behavior, CLI, output, exit-code, category, severity, safe
  excerpt, no-echo, or checked-file behavior changed.

## Next Workflow Action

Next role: Codex E - Module Reviewer.

Pasteable prompt:

```text
Use the Mythic Edge workflow rules.

Act as Codex E: Module Reviewer for Mythic Edge issue #684.

Repository:
Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/684

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Decision packet:
docs/contracts/core_secret_private_marker_scanner_decomposition_decision_packet.md

Evidence preflight:
docs/contracts/core_secret_private_marker_scanner_fresh_ars_refactor_evidence_preflight.md

Implementation handoff:
docs/implementation_handoffs/core_secret_private_marker_scanner_decomposition_comparison.md

Goal:
Review the behavior-preserving same-repo decomposition of
`tools/check_secret_patterns.py`. Verify that the public CLI facade, scan modes,
report heading, result/severity vocabulary, finding categories, safe-excerpt and
no-echo behavior, stdout/stderr routing, checked-file selection, and exit-code
semantics are preserved.

Protected boundaries:
Do not implement fixes during review. Do not change scanner behavior, CLI,
output schema, exit codes, finding categories, severity semantics, safe excerpts,
no-echo behavior, checked-file set, CI, parser behavior, EventBus behavior,
API/frontend/live-capture/workbook/webhook behavior, or readiness/security/privacy
claims.

Expected output:
Findings first, validation reviewed, remaining risks, recommended next role, and
workflow_handoff block.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/684"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  related_evidence_preflight: "https://github.com/Tahjali11/Mythic-Edge/issues/681"
  evidence_issue: "https://github.com/Tahjali11/Mythic-Edge-Automation-Artifacts/issues/132"
  evidence_pr: "https://github.com/Tahjali11/Mythic-Edge-Automation-Artifacts/pull/133"
  completed_thread: "C"
  next_thread: "E"
  verdict: "secret_private_marker_scan_behavior_preserving_decomposition_ready_for_review"
  risk_tier: "High"
  base_branch: "origin/main"
  target_branch: "main"
  branch: "codex/core-secret-scanner-decomposition-684"
  source_artifact: "docs/contracts/core_secret_private_marker_scanner_decomposition_decision_packet.md"
  target_artifact: "docs/implementation_handoffs/core_secret_private_marker_scanner_decomposition_comparison.md"
  evidence_status_for_issue_681: "precondition_satisfied"
  implementation_scope: "behavior_preserving_same_repo_scanner_decomposition"
  scanner_behavior_change_authorized: false
  scanner_cli_change_authorized: false
  scanner_exit_code_change_authorized: false
  ci_change_authorized: false
  source_repo_mutated: true
  security_assurance_claimed: false
  privacy_assurance_claimed: false
  parser_truth_claimed: false
```
