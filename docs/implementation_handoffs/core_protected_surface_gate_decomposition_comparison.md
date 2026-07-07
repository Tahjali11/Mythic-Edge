# Core Protected Surface Gate Decomposition Implementation Handoff

## Issue

<https://github.com/Tahjali11/Mythic-Edge/issues/687>

## Tracker

Project roadmap: <https://github.com/Tahjali11/Mythic-Edge/issues/568>

Related decomposition tracker:
<https://github.com/Tahjali11/Mythic-Edge/issues/463>

## Contract And Evidence

- Decision packet:
  `docs/contracts/core_protected_surface_gate_decomposition_decision_packet.md`
- Fresh scoped evidence issue:
  <https://github.com/Tahjali11/Mythic-Edge-Automation-Artifacts/issues/135>
- Fresh scoped evidence artifact:
  `automations/adversarial-review-scout/runs/2026/07/06/2026-07-06-codex-c-protected-surface-gate-scoped-evidence-summary.md`
- Evidence status: `fresh_scoped_ars_evidence` / `precondition_satisfied`
- Implementation authorization: owner routed Codex C implementation after
  evidence precondition satisfaction.

## Internal Project Area

Quality and Governance local advisory checks.

## Truth Owner

`tools/check_protected_surfaces.py` remains the public protected-surface gate
command. It owns only advisory path classification mechanics, report rendering,
changed-path collection, stdin path handling, and exit-code behavior.

Repo authority, protected-surface authorization, and human owner decisions
remain outside the helper.

## Bridge-Code Status

`not_bridge_code`

## Role Performed

Codex C: Module Implementer.

## What Changed

Implemented a behavior-preserving same-repo decomposition of
`tools/check_protected_surfaces.py`.

The public command remains:

```bash
python3 tools/check_protected_surfaces.py
```

The public script is now a compatibility facade that imports and re-exports
the same constants, dataclasses, helper functions, parser builder, and
`main()` entrypoint from focused sibling modules.

## Files Changed

- `tools/check_protected_surfaces.py`
- `tools/check_protected_surfaces_models.py`
- `tools/check_protected_surfaces_classification.py`
- `tools/check_protected_surfaces_io.py`
- `tools/check_protected_surfaces_report.py`
- `docs/implementation_handoffs/core_protected_surface_gate_decomposition_comparison.md`

## Code Changed

Runtime checker code was reorganized only.

- `tools/check_protected_surfaces.py` remains the public CLI and import
  compatibility facade.
- `tools/check_protected_surfaces_models.py` owns severity constants,
  dataclasses, forbidden rules, and warning rules.
- `tools/check_protected_surfaces_classification.py` owns path normalization,
  path matching, fixture exceptions, credential-shaped filename heuristics,
  classification, and path evaluation.
- `tools/check_protected_surfaces_io.py` owns git changed-path collection,
  gate execution, CLI parser construction, stdin mode, stdout/stderr routing,
  and `main()`.
- `tools/check_protected_surfaces_report.py` owns report rendering.

The split intentionally preserves the standard-library `subprocess` and `sys`
test seams through the public facade because existing tests monkeypatch those
module objects from `tools/check_protected_surfaces.py`.

## Tests Added Or Updated

No test files changed.

Existing focused tests continued to exercise the public facade and caught the
initial missing `subprocess` / `sys` compatibility seam. That was restored in
the facade before final validation.

## Interface Changes

No intended public interface changes.

Preserved:

- public command path: `tools/check_protected_surfaces.py`;
- CLI options: `--base`, `--repo-root`, and `--paths-from-stdin`;
- report heading: `Protected Surface Gate`;
- report field names and finding line shape;
- severity values: `allowed`, `warning`, and `forbidden`;
- result values: `passed`, `failed`, and `error`;
- exit code `0` for allowed and warning-only results;
- exit code `1` for forbidden findings;
- exit code `2` for configuration and usage errors;
- git changed-path command shape;
- stdin path collection behavior;
- checked-file selection behavior;
- forbidden category ids and warning category ids;
- documented-fixture exception behavior;
- stdout/stderr routing.

## Contracted Area Status

Stayed inside the contracted same-repo, behavior-preserving local advisory
checker boundary.

Not changed:

- protected-surface category behavior;
- CLI behavior;
- report output schema;
- exit-code semantics;
- CI behavior;
- parser behavior;
- EventBus behavior;
- API payload behavior;
- frontend behavior;
- live-capture behavior;
- workbook, webhook, or Apps Script behavior.

## Behavior-Preservation Evidence

Baseline before edits:

- Focused tests passed: `54 passed`.
- Clean changed-file mode reported `result: passed`.
- Synthetic stdin mode over two allowed helper paths, one protected parser path,
  and one forbidden generated-state path produced the same public report shape
  and expected exit code `1`.

After the decomposition:

- Focused tests passed again: `54 passed`.
- The same synthetic stdin command produced the same public report shape and
  expected exit code `1`.
- The normal changed-file command reported the touched helper modules as
  allowed and returned `result: passed`.
- Public facade monkeypatch seams for git execution and stdin handling remain
  covered by existing tests.

## Governance Checklist Outcome

- Public-safe/no-echo boundary: no private evidence, generated runtime output,
  local credential values, or source snippets were added.
- Vocabulary and example coherence: rule category ids, reason text, severity
  values, result values, and report text are preserved at runtime.
- Authority/readiness semantics: helper remains advisory evidence only.
- Fail-closed behavior: forbidden findings and configuration errors preserve
  exit-code behavior.
- Protected-surface rollout phase: same-repo helper decomposition only.

## Validation Run

Baseline:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q tests/test_check_protected_surfaces.py
PYTHONDONTWRITEBYTECODE=1 python3 tools/check_protected_surfaces.py --base origin/main --repo-root .
PYTHONDONTWRITEBYTECODE=1 python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin --repo-root .
```

Final validation:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q tests/test_check_protected_surfaces.py
PYTHONDONTWRITEBYTECODE=1 python3 tools/check_protected_surfaces.py --base origin/main --repo-root .
PYTHONDONTWRITEBYTECODE=1 python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin --repo-root .
python3 -m py_compile tools/check_protected_surfaces.py tools/check_protected_surfaces_models.py tools/check_protected_surfaces_classification.py tools/check_protected_surfaces_io.py tools/check_protected_surfaces_report.py tests/test_check_protected_surfaces.py
python3 -m ruff check src tests tools
git diff --check
printf '<changed paths>' | PYTHONDONTWRITEBYTECODE=1 python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin --repo-root .
printf '<changed paths>' | PYTHONDONTWRITEBYTECODE=1 python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin --repo-root .
printf '<changed paths>' | PYTHONDONTWRITEBYTECODE=1 python3 tools/select_validation.py --base origin/main --paths-from-stdin --format text
```

Observed results:

- Focused protected-surface tests: `54 passed`.
- `py_compile`: passed.
- Ruff on `src tests tools`: passed.
- `git diff --check`: passed.
- Path-scoped secret/private marker scan over changed helper files: passed.
- Path-scoped protected-surface gate over changed helper files: passed.
- Validation selector over changed helper files: `selection_status: ok`.

## Still Unverified

- No GitHub CI has run for this local implementation.
- No private evidence, live data, local app data, generated runtime output,
  workbook export, source-repo mutation, ARS run, Refactor Scout run, probe, or
  module sweep was performed.
- This does not prove readiness, security assurance, privacy assurance, parser
  truth, release readiness, deploy readiness, or production behavior.

## Reviewer Focus

Ask Codex E to pay special attention to:

- whether the extraction is behavior-preserving;
- whether `tools/check_protected_surfaces.py` remains a complete public facade;
- whether facade imports work when executed as a script and when imported by
  tests;
- whether category ids, reason text, report shape, stdout/stderr routing, and
  exit codes are unchanged;
- whether the literal-splitting used to avoid scanner self-findings preserves
  runtime values exactly.

## Next Workflow Action

Next role: Codex E - Module Reviewer.

Pasteable prompt:

```text
Use the Mythic Edge workflow rules.

Act as Codex E: Module Reviewer for Mythic Edge issue #687 protected-surface gate decomposition implementation.

Repository:
Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/687

Project roadmap:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Decomposition tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/463

Decision packet:
docs/contracts/core_protected_surface_gate_decomposition_decision_packet.md

Fresh scoped evidence:
https://github.com/Tahjali11/Mythic-Edge-Automation-Artifacts/issues/135

Implementation handoff:
docs/implementation_handoffs/core_protected_surface_gate_decomposition_comparison.md

Review surfaces:
- tools/check_protected_surfaces.py
- tools/check_protected_surfaces_models.py
- tools/check_protected_surfaces_classification.py
- tools/check_protected_surfaces_io.py
- tools/check_protected_surfaces_report.py

Goal:
Review whether the same-repo decomposition preserves all protected-surface gate behavior, CLI surface, output schema, category ids, reason text, severity semantics, warning/forbidden behavior, checked-file selection, stdout/stderr routing, and exit codes.

Protected boundaries:
Do not change checker behavior, parser behavior, EventBus behavior, API/frontend/live-capture behavior, workbook/webhook/Apps Script behavior, CI behavior, readiness claims, security assurance, privacy assurance, or parser-truth claims.

Expected output:
Findings first, validation reviewed, remaining risk, recommended next role, and workflow_handoff block.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/687"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  related_decomposition_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/463"
  source_artifact: "docs/contracts/core_protected_surface_gate_decomposition_decision_packet.md"
  evidence_issue: "https://github.com/Tahjali11/Mythic-Edge-Automation-Artifacts/issues/135"
  target_artifact: "docs/implementation_handoffs/core_protected_surface_gate_decomposition_comparison.md"
  completed_thread: "C"
  next_thread: "E"
  verdict: "protected_surface_gate_decomposition_ready_for_review"
  branch: "codex/protected-surface-gate-decomposition-687-c"
  behavior_preserving_same_repo_decomposition: true
  file_move_authorized: false
  protected_surface_gate_behavior_change_authorized: false
  cli_contract_change_authorized: false
  classification_rule_change_authorized: false
  path_rule_change_authorized: false
  severity_semantics_change_authorized: false
  report_output_change_authorized: false
  exit_code_change_authorized: false
  checked_file_set_change_authorized: false
  ci_change_authorized: false
  parser_behavior_change_authorized: false
  eventbus_behavior_change_authorized: false
  api_payload_change_authorized: false
  frontend_behavior_change_authorized: false
  live_capture_behavior_change_authorized: false
  workbook_webhook_change_authorized: false
  apps_script_change_authorized: false
  readiness_claimed: false
  security_assurance_claimed: false
  privacy_assurance_claimed: false
  parser_truth_claimed: false
```
