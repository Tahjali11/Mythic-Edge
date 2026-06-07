# Quality Pyright Evidence-Ledger Tests Contract

## Module

Pyright advisory cleanup for `tests/test_evidence_ledger.py`.

This contract defines a narrow quality slice for reducing Pyright advisory
findings in the evidence-ledger test module without changing evidence-ledger
behavior, weakening assertions, changing Pyright gate posture, or requiring
zero repo-wide Pyright findings.

Plain English: the tests are doing useful checks over a large dynamic ledger
mapping, but Pyright cannot see enough shape information. The fix should teach
the tests how to describe those shapes, not teach the project to ignore the
tests.

## Source Issue

Recommended new child issue under:

- Tracker: <https://github.com/Tahjali11/Mythic-Edge/issues/136>

Source artifact:

- Pyright advisory report and Codex A grouping supplied in workflow handoff

No GitHub child issue URL was supplied in this Codex B pass.

## Branch

Current branch:

```text
codex/analytics-foundation
```

Observed during this Codex B pass:

```text
8dfc7b7394e55120c5026aeef87d77a650c551f9
```

Local branch state was one commit ahead of
`origin/codex/analytics-foundation` and had an unrelated untracked contract
artifact:

```text
docs/contracts/analytics_local_developer_app_shell.md
```

This contract does not stage, commit, push, open a PR, or target `main`.

## Authority And Source Artifacts Read

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- GitHub tracker #136
- `docs/contracts/code_hardening_pyright_advisory.md`
- `docs/contracts/repo_wide_pyright_advisory_report.md`
- `pyproject.toml`
- `pyrightconfig.json`
- `tools/run_pyright_advisory_report.py`
- `tools/run_pyright_advisory.ps1`
- `tests/test_pyright_advisory_report.py`
- `src/mythic_edge_parser/app/evidence_ledger.py`
- `tests/test_evidence_ledger.py`
- `docs/contracts/player_log_evidence_ledger_schema.md`
- relevant evidence-ledger handoff/report artifacts

## Risk Tier

Medium.

Reasons:

- This is test-only quality work, not parser behavior work.
- The affected test file protects the Player.log evidence ledger, a high-value
  provenance surface.
- A careless type cleanup could weaken exact evidence-ledger assertions,
  exclude tests from Pyright, or hide real shape drift.
- The Pyright tool remains advisory and must not become a failing gate.

## Owning Layer

Primary owner: quality and type-safety evidence for tests.

Truth boundaries:

- `src/mythic_edge_parser/app/evidence_ledger.py` owns evidence-ledger
  metadata and validation behavior.
- `tests/test_evidence_ledger.py` owns focused assertions that the ledger
  registry, vocabulary, provenance entries, privacy posture, and validation
  rules remain intact.
- Pyright owns advisory static type-checking evidence only.
- Pyright findings do not own parser truth, evidence-ledger truth, analytics
  truth, workbook truth, merge readiness, or deploy readiness.

This contract must not move parser/evidence truth into tests, Pyright config,
analytics, workbook formulas, dashboards, Apps Script, webhooks, or AI output.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/quality_pyright_evidence_ledger_tests.md`

Future implementation file authorized for Codex C:

- `tests/test_evidence_ledger.py`

Future handoff/report artifacts:

- `docs/implementation_handoffs/quality_pyright_evidence_ledger_tests_comparison.md`
- optional `docs/contract_test_reports/quality_pyright_evidence_ledger_tests.md`
  if Codex E produces a formal report

Referenced but not owned:

- `src/mythic_edge_parser/app/evidence_ledger.py`
- `tools/run_pyright_advisory_report.py`
- `tools/run_pyright_advisory.ps1`
- `pyrightconfig.json`
- `pyproject.toml`
- evidence-ledger contracts, handoffs, snapshots, and reports

Codex C must route back to Codex B before editing any referenced-but-not-owned
file.

## Observed Current Behavior

Pyright posture:

- `pyproject.toml` includes `pyright>=1.1,<2` in the `dev` optional dependency
  group.
- `pyrightconfig.json` includes `src` and `tests`, excludes local/generated
  artifact paths, targets Python `3.11`, and uses `typeCheckingMode: basic`.
- `tools/run_pyright_advisory_report.py` produces a stable advisory report and
  exits `0` for categorized advisory findings.
- `tools/run_pyright_advisory.ps1` remains a Windows shortcut but throws when
  Pyright returns exit `1`; changing that wrapper is not in this contract.

Observed advisory report during this Codex B pass:

```text
py tools\run_pyright_advisory_report.py --format json
status: advisory_findings
errors: 645
warnings: 0
information: 0
type_findings: 645
local_resolver_noise: 0
tooling_config_blockers: 0
helper exit: 0
```

Observed rule counts:

```text
reportGeneralTypeIssues: 264
reportOperatorIssue: 190
reportArgumentType: 98
reportIndexIssue: 56
reportOptionalMemberAccess: 25
reportAttributeAccessIssue: 10
reportCallIssue: 2
```

Observed file grouping from raw Pyright JSON using the active interpreter:

```text
tests/test_evidence_ledger.py: 557
src/mythic_edge_parser/app/golden_replay.py: 19
tests/test_gre_annotations_parser.py: 15
src/mythic_edge_parser/parsers/gre/annotations.py: 14
```

Current evidence-ledger test shape:

- `tests/test_evidence_ledger.py` contains many constants and exact assertions
  over the evidence-ledger registry.
- Helpers currently use broad shapes such as `dict[str, object]`.
- `evidence_ledger.build_player_log_evidence_ledger()` and
  `evidence_ledger.iter_ledger_entries()` return dynamic dictionaries.
- Pyright frequently sees values such as `entry["direct_evidence"]`,
  `entry["fallback_evidence"]`, `family["seed_fields"]`, and
  `family["future_fields"]` as plain `object`.
- That causes advisory findings for iteration, set operations, membership
  checks, indexing, optional access, and argument types.

Root cause:

- The test module is using dynamic JSON-like mappings but does not provide
  local helper functions or type aliases that narrow those mappings before
  iterating or applying set/list operations.
- The findings are concentrated in test ergonomics and static analysis shape
  visibility, not in a known evidence-ledger runtime behavior bug.

## Required Guarantees

Codex C must preserve these guarantees:

- Pyright remains advisory and non-blocking.
- Zero repo-wide Pyright findings is not required.
- `tests/test_evidence_ledger.py` remains included in Pyright.
- Evidence-ledger assertions must not be weakened, skipped, deleted, xfailed,
  or converted to broad smoke tests.
- Expected field lists, entry IDs, forbidden downstream surfaces, privacy
  assertions, validation-error assertions, and deterministic-serialization
  assertions must remain semantically equivalent or stronger.
- The implementation must not change evidence-ledger runtime metadata or
  validation behavior.
- The implementation must not change parser behavior, parser state final
  reconciliation, parser event classes, match/game identity, deduplication,
  workbook schema, webhook payload shape, Apps Script behavior, Google Sheets
  sync, Match Journal, OpenAI/model-provider behavior, AI/coaching behavior, or
  production behavior.
- The implementation must not create or commit generated/private/runtime
  artifacts or secrets.

## Allowed Implementation Strategy

Codex C may edit `tests/test_evidence_ledger.py` to make test-local dynamic
shapes explicit.

Allowed techniques:

- add test-local type aliases using standard-library typing
- import `Any`, `Mapping`, `Sequence`, `cast`, or similar standard typing
  helpers if needed
- change helper return annotations from `dict[str, object]` to more accurate
  dynamic mapping/list shapes
- add small test-local narrowing helpers such as:
  - string-list extractor
  - signal-list extractor
  - entry-by-id lookup with checked entry IDs
  - family lookup with checked field shapes
  - mapping-list extractor for direct/fallback evidence
- keep `cast(...)` calls close to the dynamic boundary where the ledger returns
  JSON-like data
- use assertions inside helpers to preserve runtime test safety before casting
- consolidate repeated type-narrowing code when it reduces duplication without
  hiding assertion intent

Allowed example shape, names not required:

```python
from collections.abc import Mapping, Sequence
from typing import Any, cast

LedgerEntry = Mapping[str, Any]
EvidenceSignal = Mapping[str, Any]

def _entry_list(value: object) -> Sequence[LedgerEntry]:
    assert isinstance(value, list)
    assert all(isinstance(item, Mapping) for item in value)
    return cast(Sequence[LedgerEntry], value)
```

The exact implementation may differ. The required outcome is that tests remain
clear, exact, and type-visible.

## Forbidden Implementation Strategy

Codex C must not:

- add file-level `# pyright: ignore` or `# type: ignore` suppression
- add broad line-level ignores instead of narrowing data shapes
- remove `tests/test_evidence_ledger.py` from `pyrightconfig.json`
- change `pyrightconfig.json` to hide this test file or all tests
- change Pyright from advisory to required/failing
- require zero repo-wide Pyright findings
- edit `tools/run_pyright_advisory_report.py` or
  `tools/run_pyright_advisory.ps1`
- change source evidence-ledger data to satisfy the type checker
- weaken exact equality, subset, disjointness, privacy, or forbidden-surface
  assertions
- replace meaningful assertions with `assert value` or broad smoke checks
- introduce runtime dependencies or new package managers
- store raw Pyright output as a committed generated artifact

## Public Interface

No production public interface is authorized.

The only workflow/public surface this contract relies on is the existing
advisory report command:

```powershell
py tools\run_pyright_advisory_report.py --format json
```

Codex C may introduce test-local helper functions inside
`tests/test_evidence_ledger.py`, but they are not production API and must not
be imported by application code.

## Inputs

Primary input:

- Pyright diagnostics over the current repo using `pyrightconfig.json`.

Required grouping evidence:

- total advisory finding count
- `tests/test_evidence_ledger.py` finding count
- rule counts for the file or whole report
- before/after comparison in the implementation handoff

Primary code input:

- dynamic evidence-ledger mappings returned by
  `evidence_ledger.build_player_log_evidence_ledger()`
  and `evidence_ledger.iter_ledger_entries()`

These inputs are test data and static-analysis evidence only. They do not own
parser truth.

## Outputs

Expected Codex C outputs:

- updated `tests/test_evidence_ledger.py`
- `docs/implementation_handoffs/quality_pyright_evidence_ledger_tests_comparison.md`

Required handoff evidence:

- before/after Pyright count for `tests/test_evidence_ledger.py`
- before/after overall Pyright advisory count
- whether any residual findings remain in `tests/test_evidence_ledger.py`
- whether all evidence-ledger tests still pass
- confirmation that no source behavior or protected surface was touched

## Invariants

- Evidence-ledger tests stay behaviorally meaningful.
- The same ledger field families, entry IDs, direct evidence, fallback
  evidence, policies, notes, privacy checks, and validator checks remain
  asserted.
- Type narrowing exists to make dynamic JSON-like shapes explicit, not to
  bypass test failures.
- Test helpers may improve readability, but must not become a second
  evidence-ledger schema implementation.
- The Pyright report remains advisory evidence, not a merge/deploy gate.

## Error Behavior

If Codex C cannot reduce `tests/test_evidence_ledger.py` diagnostics without
weakening assertions or changing source behavior:

- stop
- document the exact residual diagnostics
- explain why the next step needs a broader contract
- route back to Codex B

If focused tests fail after typing changes:

- treat it as a real implementation failure
- do not paper over it with weaker assertions
- fix the test typing or route to D/E depending on workflow state

If `py tools\run_pyright_advisory_report.py --format json` reports
`tooling_config_blocker`:

- do not continue type-cleanup claims
- document the blocker
- route to a tooling-specific issue or contract

If the PowerShell wrapper throws because Pyright returns exit `1`:

- record it as known wrapper behavior
- do not change the wrapper under this contract
- use `tools/run_pyright_advisory_report.py` for the approved advisory report

## Side Effects

Allowed side effects for Codex C:

- modify `tests/test_evidence_ledger.py`
- create
  `docs/implementation_handoffs/quality_pyright_evidence_ledger_tests_comparison.md`

Forbidden side effects:

- source behavior changes
- Pyright config changes
- CI gate changes
- wrapper/report helper changes
- generated report files
- raw logs, runtime artifacts, SQLite files, failed posts, workbook exports,
  secrets, or local-only artifacts
- GitHub issue closure, tracker completion, PR creation, staging, commit, push,
  or merge unless a later role explicitly authorizes it

## Dependency Order

Recommended Codex C order:

1. Confirm branch and worktree state.
2. Re-run the advisory report and file grouping to establish the current
   baseline.
3. Inspect the most common `tests/test_evidence_ledger.py` diagnostics.
4. Add test-local type aliases/narrowing helpers.
5. Update assertions only where needed to use the typed helpers while preserving
   exact semantics.
6. Run focused evidence-ledger tests.
7. Re-run Pyright advisory report and file grouping.
8. Write the implementation handoff with before/after counts and residuals.

## Compatibility

This contract must preserve compatibility with:

- current evidence-ledger registry shape
- current evidence-ledger schema snapshot tests
- current evidence-ledger drift report tests
- current Pyright advisory helper/report shape
- current advisory-only Pyright policy

It must not require changing historical evidence-ledger contracts or snapshots.

## Tests Required

Focused validation:

```powershell
py -m pytest -q tests\test_evidence_ledger.py
py -m ruff check tests\test_evidence_ledger.py
py tools\run_pyright_advisory_report.py --format json
git diff --check
```

Required file-grouping probe for before/after evidence:

```powershell
@'
import json, subprocess, sys
from collections import Counter

completed = subprocess.run(
    ["pyright", "--project", "pyrightconfig.json", "--pythonpath", sys.executable, "--outputjson"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    check=False,
)
payload = json.loads(completed.stdout)
by_file = Counter()
for diagnostic in payload.get("generalDiagnostics", []):
    path = str(diagnostic.get("file") or "").replace("\\", "/")
    marker = "/MythicEdge/"
    if marker in path:
        path = path.split(marker, 1)[1]
    by_file[path] += 1
print("pyright_exit", completed.returncode)
print("tests/test_evidence_ledger.py", by_file.get("tests/test_evidence_ledger.py", 0))
print("total", sum(by_file.values()))
'@ | py -
```

Recommended adjacent validation when time allows:

```powershell
py -m pytest -q tests\test_evidence_schema_snapshot.py tests\test_evidence_schema_drift_report.py
py tools\check_secret_patterns.py --all
@'
tests/test_evidence_ledger.py
docs/implementation_handoffs/quality_pyright_evidence_ledger_tests_comparison.md
'@ | py tools\check_protected_surfaces.py --base origin/codex/analytics-foundation --paths-from-stdin
```

## Acceptance Criteria

Codex C satisfies this contract when:

- `tests/test_evidence_ledger.py` still passes.
- Ruff passes for `tests/test_evidence_ledger.py`.
- Pyright advisory report still runs through
  `tools/run_pyright_advisory_report.py` and remains advisory.
- `tests/test_evidence_ledger.py` Pyright diagnostics are reduced
  substantially, with a preferred target of `0` diagnostics for that file.
- Zero repo-wide Pyright diagnostics is not required.
- Any remaining `tests/test_evidence_ledger.py` diagnostics are explicitly
  listed with rule, count, and reason.
- No assertions are weakened, skipped, xfailed, or hidden behind broad ignores.
- No Pyright config, CI gate, source behavior, parser behavior, workbook,
  webhook, Apps Script, Google Sheets, Match Journal, OpenAI, AI/coaching, or
  production surface is changed.
- The implementation handoff records before/after counts and residual risks.

## Open Questions

- Whether future work should introduce production `TypedDict` definitions for
  evidence-ledger data. This contract does not authorize that because it would
  touch source interfaces.
- Whether `tools/run_pyright_advisory.ps1` should delegate to
  `tools/run_pyright_advisory_report.py` so Windows users do not hit a thrown
  exception on advisory findings. This contract records the gap but does not
  authorize it.
- Whether the other Pyright clusters should become separate child issues under
  tracker #136. This contract covers only `tests/test_evidence_ledger.py`.

## Next Workflow Action

Next role: Codex C: Module Implementer / comparison thread.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex C: Module Implementer / comparison thread for the Pyright evidence-ledger tests quality contract.

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/136

Source contract:
docs/contracts/quality_pyright_evidence_ledger_tests.md

Branch:
codex/analytics-foundation

Goal:
Reduce Pyright advisory findings in tests/test_evidence_ledger.py by adding test-local type aliases and narrowing helpers while preserving evidence-ledger assertions exactly. Produce docs/implementation_handoffs/quality_pyright_evidence_ledger_tests_comparison.md.

Before editing:
- Confirm the branch is codex/analytics-foundation.
- Inspect git status and exclude unrelated changes, especially any untracked docs/contracts/analytics_local_developer_app_shell.md artifact.
- Re-run the Pyright advisory report and file-grouping probe to capture the current baseline.
- State what the tests are supposed to do, what Pyright is actually reporting, why the findings are concentrated in dynamic test helper shapes, and the exact minimal implementation plan.

Read:
- AGENTS.md
- docs/agent_rules.yml
- docs/agent_constitution.md
- docs/codex_module_workflow.md
- docs/agent_threads/implementation.md
- docs/templates/implementation_handoff.md
- docs/contracts/quality_pyright_evidence_ledger_tests.md
- docs/contracts/repo_wide_pyright_advisory_report.md
- docs/contracts/code_hardening_pyright_advisory.md
- pyrightconfig.json
- tools/run_pyright_advisory_report.py
- tests/test_pyright_advisory_report.py
- src/mythic_edge_parser/app/evidence_ledger.py
- tests/test_evidence_ledger.py
- relevant evidence-ledger schema snapshot/drift report tests if needed

Implement only:
- test-local type aliases, casts, and narrowing helpers in tests/test_evidence_ledger.py
- assertion updates needed to use those helpers while preserving exact behavior
- docs/implementation_handoffs/quality_pyright_evidence_ledger_tests_comparison.md with before/after Pyright counts and residual findings

Do not:
- edit source evidence-ledger behavior
- edit pyrightconfig.json
- edit tools/run_pyright_advisory_report.py or tools/run_pyright_advisory.ps1
- make Pyright required or failing
- require zero repo-wide Pyright findings
- remove tests from Pyright
- add broad pyright/type ignores
- weaken, skip, xfail, delete, or broaden evidence-ledger assertions
- change parser behavior, parser state final reconciliation, parser event classes, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets sync, Match Journal, OpenAI/model-provider behavior, AI/coaching behavior, production behavior, secrets, raw logs, generated data, runtime status files, failed posts, workbook exports, or local-only artifacts
- target main
- close tracker #136
- stage, commit, push, or open a PR

Validation:
py -m pytest -q tests\test_evidence_ledger.py
py -m ruff check tests\test_evidence_ledger.py
py tools\run_pyright_advisory_report.py --format json
git diff --check

Also run this file-grouping probe before and after implementation and record both results:

@'
import json, subprocess, sys
from collections import Counter

completed = subprocess.run(
    ["pyright", "--project", "pyrightconfig.json", "--pythonpath", sys.executable, "--outputjson"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    check=False,
)
payload = json.loads(completed.stdout)
by_file = Counter()
for diagnostic in payload.get("generalDiagnostics", []):
    path = str(diagnostic.get("file") or "").replace("\\", "/")
    marker = "/MythicEdge/"
    if marker in path:
        path = path.split(marker, 1)[1]
    by_file[path] += 1
print("pyright_exit", completed.returncode)
print("tests/test_evidence_ledger.py", by_file.get("tests/test_evidence_ledger.py", 0))
print("total", sum(by_file.values()))
'@ | py -

Final handoff must include:
- role performed
- source contract used
- files changed
- exact helper/test sections changed
- before/after Pyright counts for tests/test_evidence_ledger.py and repo total
- what was verified
- what remains unverified
- whether any assertions or protected surfaces were touched
- next recommended role
- workflow_handoff block
```

```yaml
workflow_handoff:
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/136"
  issue: "recommended new child issue under #136"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "Pyright advisory report and Codex A grouping"
  target_artifact: "docs/contracts/quality_pyright_evidence_ledger_tests.md"
  branch: "codex/analytics-foundation"
  risk_tier: "Medium"
  validation:
    - "git status --short --branch"
    - "git diff --check"
    - "path-scoped protected-surface gate for docs/contracts/quality_pyright_evidence_ledger_tests.md"
  stop_conditions:
    - "Do not edit code in Codex B."
    - "Do not make Pyright a required/failing gate."
    - "Do not require zero repo-wide Pyright findings."
    - "Do not weaken evidence-ledger test assertions."
    - "Do not change production parser/runtime/workbook/webhook/App Script/Sheets/OpenAI/AI behavior."
```
