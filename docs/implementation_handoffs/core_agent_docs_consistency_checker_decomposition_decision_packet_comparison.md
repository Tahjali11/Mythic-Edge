# Core Agent Docs Consistency Checker Decomposition Handoff

## Issue

<https://github.com/Tahjali11/Mythic-Edge/issues/667>

## Tracker

Project roadmap: <https://github.com/Tahjali11/Mythic-Edge/issues/568>

Related decomposition tracker:
<https://github.com/Tahjali11/Mythic-Edge/issues/463>

Related ARS gate issue:
<https://github.com/Tahjali11/Mythic-Edge/issues/664>

## Contract

`docs/contracts/core_agent_docs_consistency_checker_decomposition_decision_packet.md`

## Internal Project Area

Quality / Governance; local advisory check surface.

## Truth Owner

Active governance docs, current GitHub issue scope, current contract scope,
accepted ADRs, and handoff artifacts own authority. `tools/check_agent_docs.py`
is advisory evidence only; it does not own repo authority, parser truth,
readiness, security assurance, or privacy assurance.

## Bridge-Code Status

`not_bridge_code`.

## Role Performed

Codex C: Module Implementer.

## What Changed

Implemented the authorized behavior-preserving same-repo decomposition for
`tools/check_agent_docs.py`.

The public CLI entrypoint remains `tools/check_agent_docs.py`. The script still
owns `main(argv)`, `build_parser()`, repository checks, CLI handling, stdout /
stderr routing, and exit-code selection. It now imports and re-exports stable
internal pieces from focused sibling modules:

- `tools/check_agent_docs_contract.py`
  - constants and contract vocabulary such as severities, result values,
    required files, role names, schema keys, ADR heading expectations, and
    protected-surface terms.
- `tools/check_agent_docs_models.py`
  - `Finding`, `CheckResult`, and `Reference`.
- `tools/check_agent_docs_report.py`
  - `render_report()` and `render_json()`.

The compatibility facade keeps the names existing tests and local tools import
from `tools/check_agent_docs.py`, including constants, dataclasses,
`_sort_findings()`, `run_check()`, `render_report()`, `render_json()`, and
`main()`.

## Behavior Preservation Evidence

Baseline outputs were captured before editing under local `/tmp` scratch space
and compared byte-for-byte after extraction.

Before/after comparisons passed for:

- `python3 tools/check_agent_docs.py`
- `python3 tools/check_agent_docs.py --format json`
- `python3 tools/check_agent_docs.py --repo-root /tmp/mythic-edge-does-not-exist-667`
- `python3 tools/check_agent_docs.py --format yaml`
- exit code for text report
- exit code for JSON report
- exit code for invalid repo root
- exit code for invalid format
- stdout/stderr split for invalid repo root
- stdout/stderr split for invalid format

Observed preserved behavior:

- passing repo checks 36 files;
- text heading remains `Agent Docs Consistency Check`;
- JSON keys and checked-file list remain unchanged;
- severity values remain `error` and `warning`;
- result values remain `passed`, `warning`, `failed`, and `error`;
- valid text and JSON reports exit `0`;
- invalid repo root exits `2`;
- invalid format exits `2`;
- advisory-only checker status is unchanged.

## Files Changed

- `tools/check_agent_docs.py`
- `tools/check_agent_docs_contract.py`
- `tools/check_agent_docs_models.py`
- `tools/check_agent_docs_report.py`
- `docs/implementation_handoffs/core_agent_docs_consistency_checker_decomposition_decision_packet_comparison.md`

Existing untracked source artifact present before this pass:

- `docs/contracts/core_agent_docs_consistency_checker_decomposition_decision_packet.md`

## Code Changed

Runtime checker code was reorganized only. No checker behavior, CLI option,
output schema, checked-file set, severity semantics, stdout/stderr routing,
exit code, CI behavior, governance authority, parser behavior, EventBus
behavior, API behavior, frontend behavior, live-capture behavior, workbook /
webhook behavior, or Apps Script behavior changed.

## Tests Added Or Updated

No test files changed. Existing focused tests continued to exercise the public
compatibility facade and imported names after extraction.

## Interface Changes

None.

The public path remains:

```bash
python3 tools/check_agent_docs.py
```

The public CLI options remain:

```bash
--repo-root
--format {text,json}
```

## Contracted Area Status

Stayed inside the contracted `local_advisory_check_surface` decomposition
boundary. No ARS or Refactor Scout runs were performed. No protected product
surfaces changed.

## Governance Checklist Outcome

- Public-safe/no-echo boundary: no private data, raw logs, generated reports,
  runtime artifacts, secrets, or local paths committed.
- Vocabulary and example coherence: stable checker vocabulary moved to
  `tools/check_agent_docs_contract.py` without value changes.
- Authority/readiness semantics: checker remains advisory evidence only.
- Fail-closed schema or validator checks: no checker rules changed.
- Protected-surface rollout phase: no protected-surface enforcement, CI, or
  readiness gate change.

## Validation Run

```bash
git status --short --branch
git fetch --prune
git rev-parse HEAD
git rev-parse origin/main
gh issue view 667 --repo Tahjali11/Mythic-Edge --json number,title,state,body,url,labels,comments

python3 tools/check_agent_docs.py
python3 tools/check_agent_docs.py --format json
python3 tools/check_agent_docs.py --repo-root /tmp/mythic-edge-does-not-exist-667
python3 tools/check_agent_docs.py --format yaml
python3 -m pytest -q tests/test_check_agent_docs.py
python3 -m py_compile tools/check_agent_docs.py tools/check_agent_docs_contract.py tools/check_agent_docs_models.py tools/check_agent_docs_report.py
python3 -m ruff check tools/check_agent_docs.py tools/check_agent_docs_contract.py tools/check_agent_docs_models.py tools/check_agent_docs_report.py tests/test_check_agent_docs.py

cmp /tmp/mythic-edge-667-baseline/check_agent_docs.before.txt /tmp/mythic-edge-667-baseline/check_agent_docs.after2.txt
cmp /tmp/mythic-edge-667-baseline/check_agent_docs.before.json /tmp/mythic-edge-667-baseline/check_agent_docs.after2.json
cmp /tmp/mythic-edge-667-baseline/text.exit /tmp/mythic-edge-667-baseline/text.after2.exit
cmp /tmp/mythic-edge-667-baseline/json.exit /tmp/mythic-edge-667-baseline/json.after2.exit
cmp /tmp/mythic-edge-667-baseline/invalid_root.stdout /tmp/mythic-edge-667-baseline/invalid_root.after2.stdout
cmp /tmp/mythic-edge-667-baseline/invalid_root.stderr /tmp/mythic-edge-667-baseline/invalid_root.after2.stderr
cmp /tmp/mythic-edge-667-baseline/invalid_root.exit /tmp/mythic-edge-667-baseline/invalid_root.after2.exit
cmp /tmp/mythic-edge-667-baseline/invalid_format.stdout /tmp/mythic-edge-667-baseline/invalid_format.after2.stdout
cmp /tmp/mythic-edge-667-baseline/invalid_format.stderr /tmp/mythic-edge-667-baseline/invalid_format.after2.stderr
cmp /tmp/mythic-edge-667-baseline/invalid_format.exit /tmp/mythic-edge-667-baseline/invalid_format.after2.exit
```

Observed results so far:

- `HEAD` and `origin/main` both resolve to
  `70191d1c11ac49d01ae308db1612e7669c304f9a`.
- Issue #667 is open.
- Focused checker tests passed: 19 tests.
- `py_compile` passed for the public script and extracted helper modules.
- Ruff passed for the public script, extracted helper modules, and focused
  tests.
- Before/after text, JSON, invalid-root, invalid-format, and exit-code
  comparisons passed byte-for-byte.

Final path-scoped validation after this handoff update:

```bash
python3 tools/check_agent_docs.py
python3 tools/check_agent_docs.py --format json
python3 tools/check_agent_docs.py --repo-root /tmp/mythic-edge-does-not-exist-667
python3 tools/check_agent_docs.py --format yaml
git diff --check
git ls-files --others --modified --exclude-standard -- tools tests docs | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
git ls-files --others --modified --exclude-standard -- tools tests docs | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
git ls-files --others --modified --exclude-standard -- tools tests docs | python3 tools/select_validation.py --base origin/main --paths-from-stdin --format text
python3 -m ruff check src tests tools
python3 tools/run_pyright_advisory_report.py
python3 changed-file ASCII/final-newline/trailing-whitespace hygiene check
```

Observed final results:

- Text and JSON checker commands passed with `result: passed`.
- Invalid root and invalid format still exited `2`.
- Final text, JSON, invalid-root stdout/stderr, and invalid-format
  stdout/stderr matched the saved pre-edit baseline byte-for-byte.
- Final exit-code values matched the saved pre-edit baseline.
- `git diff --check` passed.
- Secret/private marker scan passed across 6 changed paths.
- Protected-surface gate passed across 6 changed paths.
- Validation selector completed with `selection_status: ok`; all required and
  recommended selected commands were run.
- Full Ruff passed across `src`, `tests`, and `tools`.
- Pyright advisory helper ran in advisory mode and reported existing type
  findings without blocking this change.
- ASCII/final-newline/trailing-whitespace hygiene passed across 6 changed
  paths.

## Still Unverified

- CI was not run locally and no CI behavior was changed.
- No ARS or Refactor Scout evidence was collected, per the contract boundary.
- Broader repo tests were not required for this same-file local advisory helper
  split; focused checker tests and byte-for-byte CLI comparisons covered the
  touched public behavior.

## Reviewer Focus

Codex E should focus on:

- whether the re-export compatibility facade is sufficient for current tests
  and local tooling;
- whether the dual `tools.*` / sibling import path is acceptable for both
  direct CLI execution and file-path import in tests;
- whether future follow-up decomposition should extract reference inventory and
  rule families after this first stable split;
- whether byte-for-byte baseline evidence adequately proves behavior
  preservation for this first split.

## Next Workflow Action

Next role: Codex E - Module Reviewer.

Pasteable prompt:

```text
Use the Mythic Edge workflow rules.

Act as Codex E: Module Reviewer for issue #667.

Repository:
Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/667

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Related ARS gate issue:
https://github.com/Tahjali11/Mythic-Edge/issues/664

Related decomposition tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/463

Contract:
docs/contracts/core_agent_docs_consistency_checker_decomposition_decision_packet.md

Implementation handoff:
docs/implementation_handoffs/core_agent_docs_consistency_checker_decomposition_decision_packet_comparison.md

Candidate:
tools/check_agent_docs.py

Review the behavior-preserving same-repo decomposition. Verify that
tools/check_agent_docs.py remains the public CLI entrypoint and compatibility
facade, that CLI options, accepted formats, exit codes, text heading, JSON
keys, severity/result values, checked-file inventory, finding order,
stdout/stderr behavior, and advisory-only status are unchanged, and that the
new helper modules do not change checker behavior or protected surfaces.

Lead with findings if any. Do not change code, run ARS or Refactor Scout, alter
CI, change parser/EventBus/API/frontend/live-capture/workbook/webhook/Apps
Script behavior, or claim readiness, parser truth, security assurance, or
privacy assurance.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/667"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  related_ars_gate_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/664"
  related_decomposition_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/463"
  completed_thread: "C"
  next_thread: "E"
  verdict: "agent_docs_consistency_checker_same_repo_decomposition_ready_for_review"
  source_artifact: "docs/contracts/core_agent_docs_consistency_checker_decomposition_decision_packet.md"
  target_artifact: "docs/implementation_handoffs/core_agent_docs_consistency_checker_decomposition_decision_packet_comparison.md"
  candidate_surface: "tools/check_agent_docs.py"
  candidate_id: "agent_doc_consistency_check"
  candidate_surface_class: "local_advisory_check_surface"
  base_branch: "origin/main"
  latest_verified_origin_main: "70191d1c11ac49d01ae308db1612e7669c304f9a"
  implementation_authorized: true
  file_move_authorized: false
  cross_repo_extraction_authorized: false
  ars_run_authorized: false
  refactor_scout_run_authorized: false
  source_mutation_authorized: false
  parser_behavior_change_authorized: false
  ci_change_authorized: false
  readiness_claimed: false
  parser_truth_claimed: false
  reliability_readiness_claimed: false
  security_assurance_claimed: false
  privacy_assurance_claimed: false
```
