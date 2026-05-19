# Repo-Wide Agent Docs Consistency Checker Implementation Handoff

Issue: https://github.com/Tahjali11/Mythic-Edge/issues/86

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/82

Contract: `docs/contracts/repo_wide_agent_docs_consistency_checker.md`

Role performed: Codex C: Module Implementer; Codex D: Module Fixer follow-up

Branch: `codex/repo-wide-hardening-run`

Risk tier: Medium

## Summary Of Implementation Comparison

Current repo state before this pass had deterministic hardening tools for
protected paths and secret/private content, but no stable checker for agent
governance-doc consistency.

Confirmed current state:

- `tools/check_secret_patterns.py` exists from issue #84 / PR #85.
- `tools/check_protected_surfaces.py` exists and remains unchanged.
- `tools/check_agent_docs.py` did not exist before this pass.
- `tests/test_check_agent_docs.py` did not exist before this pass.
- `docs/contracts/repo_wide_agent_docs_consistency_checker.md` was already
  present as the untracked source contract artifact for this issue.

This pass implemented the smallest deterministic repo-mode checker required by
the contract and added focused tests. It did not rewrite governance docs, edit
CI, add dependencies, or touch parser/runtime/workbook/App Script behavior.

Codex D follow-up resolved the reviewer-blocking missed invariant for Codex D
loopback prose. The checker now fails if the active workflow doc drops the
statement that D is loopback-only while preserving the normal happy path.

## Findings

No blocking contract ambiguity was found.

Contract mismatch fixed:

- Missing checker implementation: added `tools/check_agent_docs.py`.
- Missing focused tests: added `tests/test_check_agent_docs.py`.
- Missing implementation handoff: added this document.
- Reviewer-blocking Codex D loopback prose mismatch: added an explicit workflow
  doc invariant and focused regression coverage.

Current live governance-doc result after implementation:

```text
Agent Docs Consistency Check
mode: repo
checked_files: 29
errors: 0
warnings: 0

result: passed
```

## Changes Made

Implemented `tools/check_agent_docs.py`:

- repo-mode CLI:
  - `python3 tools/check_agent_docs.py`
  - optional `--repo-root <path>`
  - optional `--format text|json`
- standard-library-only parsing:
  - no PyYAML or new dependency
  - deterministic parsing for the known `docs/agent_rules.yml` shape
  - conservative Markdown backtick/link reference extraction
- stable report:
  - `Agent Docs Consistency Check`
  - `mode: repo`
  - checked file count
  - error/warning counts
  - sorted `ERROR`/`WARNING` findings
  - final result
- enforced invariants:
  - required governance file presence
  - repo-local reference existence and glob matching
  - canonical A-G role registry and Codex H auxiliary role
  - normal path `A -> B -> C -> E -> F -> G`
  - Codex D loopback-only prose in the active workflow doc
  - critical authority-order relationships
  - workflow handoff block keys and valid `next_thread` values
  - `prompt_schema.required` and `handoff_schema.required` presence
  - issue template source/target/branch/protected-surface/validation/stop fields
  - ADR status set, README index, filename, status, and recommended-field checks
  - protected-surface text presence
  - external integration/collaboration boundary text presence
  - advisory CI integration check for unauthorized `check_agent_docs.py` workflow use

Added `tests/test_check_agent_docs.py`:

- CLI/report shape
- warning-only exit behavior
- error and runtime configuration exit behavior
- deterministic finding sorting
- required-file checking
- repo-local reference and glob checking
- role registry, normal-path, and auxiliary-role checks
- focused regression coverage for removing D loopback-only workflow prose while
  preserving `routing.normal_path`
- authority-order inversion detection
- workflow handoff schema checks
- issue template field checks
- ADR status/index/template behavior
- protected-surface and external-surface boundary checks

## Confirmed Matches

- Required governance files are checked.
- Repo-local references are checked conservatively.
- URLs and anchors are ignored.
- Globs must match at least one file.
- Archived docs are not treated as active authority.
- A-G and H role names are compared against the contract registry.
- D remains loopback-only.
- H remains auxiliary and outside the normal path.
- `docs/agent_rules.yml` and `docs/codex_module_workflow.md` preserve
  `A -> B -> C -> E -> F -> G`.
- Removing D loopback-only prose from `docs/codex_module_workflow.md` now
  produces a deterministic `normal_path_mismatch` finding even when
  `routing.normal_path` remains correct.
- Authority-order checks enforce critical relative ordering rather than exact
  prose equality.
- Handoff template required keys and `next_thread` values are checked.
- ADR README status values match `docs/agent_rules.yml`.
- ADR files and README index entries match.
- Warnings exit `0`; errors exit `1`; configuration errors exit `2`.
- CI was not edited.
- No parser/runtime/workbook/App Script behavior was changed.

## Missing Safeguards

No required safeguard remains knowingly missing in the implemented checker.

Future hardening may still add:

- richer YAML parsing if the rule index shape becomes more complex
- JSON report contract tests beyond the current optional output smoke behavior
- GitHub annotation output
- changed-file mode
- CI integration after a future contract authorizes it
- broader Markdown link validation

Those are intentionally outside this first implementation contract.

## CI Decision

Deferred.

The contract explicitly says not to add CI validation for `check_agent_docs.py`
in this issue. This pass did not edit `.github/workflows/repo-checks.yml`.

Reviewer/local command:

```bash
python3 tools/check_agent_docs.py
```

## Validation Evidence

Passed:

```bash
python3 -m pytest -q tests/test_check_agent_docs.py
```

```text
17 passed in 0.08s
```

Passed:

```bash
python3 tools/check_agent_docs.py
```

```text
Agent Docs Consistency Check
mode: repo
checked_files: 29
errors: 0
warnings: 0

result: passed
```

Passed:

```bash
python3 -m pytest -q tests/test_check_secret_patterns.py tests/test_check_protected_surfaces.py
```

```text
77 passed in 0.05s
```

Passed:

```bash
python3 tools/check_agent_docs.py --format json
```

```text
result: passed; errors: 0; warnings: 0
```

Passed with warnings only and exit code `0`:

```bash
python3 tools/check_secret_patterns.py --base origin/main
```

```text
Secret / Private Marker Scan
mode: changed-files
base: origin/main
head: HEAD
scanned_paths: 6
skipped_paths: 0
forbidden: 0
warnings: 19

result: warning
```

Warnings were policy/test/handoff artifact references already classified as
non-failing by the secret/private-marker scanner.

Passed:

```bash
python3 tools/check_protected_surfaces.py --base origin/main
```

```text
Protected Surface Gate
base: origin/main
head: HEAD
changed_paths: 6
forbidden: 0
warnings: 0

result: passed
```

Passed:

```bash
python3 -m ruff check src tests tools
```

```text
All checks passed!
```

Passed:

```bash
git diff --check
```

```text
<no output>
```

Passed:

```bash
python3 -m pytest -q tests
```

```text
710 passed in 1.12s
```

Passed with warnings only and exit code `0`:

```bash
printf 'tools/check_agent_docs.py\ntests/test_check_agent_docs.py\ndocs/contracts/repo_wide_agent_docs_consistency_checker.md\ndocs/contract_test_reports/repo_wide_agent_docs_consistency_checker.md\ndocs/implementation_handoffs/repo_wide_agent_docs_consistency_checker_comparison.md\n' | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
```

```text
scanned_paths: 5; forbidden: 0; warnings: 3; result: warning
```

## Open Risks

- The YAML-like parsing is intentionally narrow and tied to the current
  `docs/agent_rules.yml` shape.
- Markdown reference extraction is conservative by design and is not a complete
  Markdown link validator.
- Authority-order checks use concrete terms and critical relative ordering,
  not semantic proof of every governance sentence.
- ADR recommended-field checks warn rather than fail for heading wording drift.
- CI integration is intentionally deferred, so reviewers and submitters must
  run the tool locally until a future contract authorizes enforcement.

## Still-Unverified Layers

- No live MTGA parser run was executed.
- No live workbook, webhook, or Apps Script integration was inspected.
- No CI run was triggered.
- No tracker #82 completion action was taken.

## Protected Surfaces

Not changed:

- parser behavior
- parser state final reconciliation
- workbook schema
- webhook payload shape
- Apps Script behavior
- parser event classes
- match identity
- game identity
- deduplication
- secrets or environment variable semantics
- raw logs
- generated data
- runtime status files
- failed posts
- workbook exports
- protected-surface path gate behavior
- secret/private-marker scanner behavior
- CI workflow behavior

## Next Workflow Action

Next recommended role: Codex E: Module Reviewer in contract-test mode.

Pasteable next-thread prompt:

```text
Use the Mythic Edge agent constitution.

Act as Codex E: Module Reviewer in contract-test mode for issue #86:
https://github.com/Tahjali11/Mythic-Edge/issues/86

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/82

Branch:
codex/repo-wide-hardening-run

Use:
- docs/contracts/repo_wide_agent_docs_consistency_checker.md
- docs/contract_test_reports/repo_wide_agent_docs_consistency_checker.md
- docs/implementation_handoffs/repo_wide_agent_docs_consistency_checker_comparison.md
- docs/contracts/repo_wide_secret_private_marker_scanner.md
- docs/contract_test_reports/repo_wide_hardening_baseline.md
- tools/check_agent_docs.py
- tests/test_check_agent_docs.py
- tools/check_secret_patterns.py
- tests/test_check_secret_patterns.py
- tools/check_protected_surfaces.py
- tests/test_check_protected_surfaces.py
- AGENTS.md
- docs/agent_rules.yml
- docs/agent_constitution.md
- docs/codex_module_workflow.md
- docs/agent_threads/*.md
- docs/templates/*.md
- .github/ISSUE_TEMPLATE/module_workflow.yml
- .github/pull_request_template.md
- docs/decisions/README.md
- docs/decisions/ADR-*.md

Goal:
Re-review the Module Implementer checker and Codex D loopback-prose fix against
the agent docs consistency checker contract.

Confirm:
- tools/check_agent_docs.py provides deterministic repo-mode checking with standard-library-only parsing.
- The CLI supports python3 tools/check_agent_docs.py, --repo-root, and --format text|json.
- Required governance files are checked.
- Repo-local references in backticks and Markdown links are checked conservatively.
- URLs, anchors, issue/PR links, shell commands, placeholders, and non-file globs are ignored.
- Globs such as docs/agent_threads/*.md require at least one matching file.
- Archived docs are ignored unless active docs cite them confusingly as authority.
- A-G role names and Codex H auxiliary role match the contract registry.
- D remains loopback-only and H remains auxiliary, not part of the normal path.
- Removing D loopback-only prose from the active workflow doc produces a deterministic finding even when routing.normal_path remains A -> B -> C -> E -> F -> G.
- docs/agent_rules.yml and docs/codex_module_workflow.md preserve A -> B -> C -> E -> F -> G.
- Authority-order checks enforce the critical relative ordering without requiring exact prose equality.
- docs/templates/workflow_handoff.md contains required workflow_handoff keys and valid next_thread values.
- docs/agent_rules.yml includes prompt_schema.required and handoff_schema.required.
- .github/ISSUE_TEMPLATE/module_workflow.yml includes source artifact, target artifact, branch, protected surfaces, validation, and stop condition fields.
- ADR statuses in docs/decisions/README.md match docs/agent_rules.yml.
- Numbered ADR files have allowed statuses, README index entries, matching README statuses, and recommended fields warn rather than fail when appropriate.
- Protected-surface and external-surface boundary text checks cover the contract terms.
- Warnings exit 0, error findings exit 1, configuration/runtime errors exit 2.
- Findings are sorted deterministically.
- .github/workflows/repo-checks.yml was not edited and check_agent_docs.py was not wired into CI.
- No parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, or protected surfaces outside this contract changed.

Validation:
Run:
python3 -m pytest -q tests/test_check_agent_docs.py
python3 tools/check_agent_docs.py
python3 tools/check_agent_docs.py --format json
python3 -m pytest -q tests/test_check_secret_patterns.py tests/test_check_protected_surfaces.py
python3 tools/check_secret_patterns.py --base origin/main
python3 tools/check_protected_surfaces.py --base origin/main
python3 -m ruff check src tests tools
git diff --check

If feasible, also run:
python3 -m pytest -q tests

Output:
- Findings first, if any.
- Contract-test verdict.
- Validation results.
- Remaining non-blocking gaps.
- Next recommended role: Codex F: Module Submitter if no blocking findings, otherwise Codex D: Module Fixer or Codex B: Module Contract Writer.
- A workflow_handoff block.

Do not stage, commit, merge, target main, mark tracker #82 complete, edit CI, rewrite agent docs, add dependencies, or change parser/runtime/workbook/App Script behavior during review.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/86"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/82"
  completed_thread: "D"
  next_thread: "E"
  source_artifact: "docs/contract_test_reports/repo_wide_agent_docs_consistency_checker.md"
  target_artifact: "Codex E contract-test re-review for repo-wide agent docs consistency checker"
  risk_tier: "Medium"
  branch: "codex/repo-wide-hardening-run"
  verdict: "Fixer pass complete: checker verifies active workflow docs still describe Codex D as loopback-only."
  validation:
    - "python3 -m pytest -q tests/test_check_agent_docs.py -> 17 passed in 0.08s"
    - "python3 tools/check_agent_docs.py -> passed, checked_files 29, errors 0, warnings 0"
    - "python3 tools/check_agent_docs.py --format json -> passed, result passed"
    - "python3 -m pytest -q tests/test_check_secret_patterns.py tests/test_check_protected_surfaces.py -> 77 passed in 0.05s"
    - "python3 tools/check_secret_patterns.py --base origin/main -> warning-only exit 0, scanned_paths 6, forbidden 0, warnings 19"
    - "python3 tools/check_protected_surfaces.py --base origin/main -> passed, changed_paths 6, forbidden 0, warnings 0"
    - "python3 -m ruff check src tests tools -> All checks passed"
    - "git diff --check -> passed with no output"
    - "python3 -m pytest -q tests -> 710 passed in 1.12s"
    - "new package paths-from-stdin secret scan -> warning-only exit 0, scanned_paths 5, forbidden 0, warnings 3"
  stop_conditions:
    - "Do not edit CI unless separately authorized."
    - "Do not rewrite agent docs unless a narrow blocker is routed back and approved."
    - "Do not add dependencies without contract authorization."
    - "Do not change parser/runtime/workbook/App Script behavior or protected surfaces outside this contract."
    - "Do not target main directly."
    - "Do not mark tracker #82 complete."
```
