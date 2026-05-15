# Code Hardening Protected-Surface Diff Gate Contract

Source issue: https://github.com/Tahjali11/Mythic-Edge/issues/34

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/33

Agent docs:

- `docs/agent_constitution.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/codex_module_workflow.md`

Issue #34 also names `docs/agent_rules.yml` as a rule source. On the current
`codex/code-hardening-suite` branch inspected for this contract, that file is
not present. The first implementation must either keep the policy table in this
contract as the executable source of truth or add/sync `docs/agent_rules.yml`
through a separate explicitly authorized workflow change.

Workflow and repo docs read:

- `.github/pull_request_template.md`
- `.github/workflows/repo-checks.yml`
- `tools/run_repo_checks.ps1`
- `tools/run_touched_file_checks.ps1`
- `.gitignore`

Branch target: `codex/code-hardening-suite`

This contract defines the first protected-surface diff gate for the Code
Hardening suite. It is a contract artifact only. It does not implement code,
change CI, or change parser/runtime/workbook/App Script behavior.

## Module

Protected-surface diff gate.

Likely implementation artifact:

- `tools/check_protected_surfaces.py`

Likely tests:

- `tests/test_check_protected_surfaces.py`

The module should inspect a changed-file list for a branch or pull request and
classify paths into:

- forbidden committed artifacts that fail the gate
- ambiguous protected-surface changes that warn/report but do not fail in the
  first version
- ordinary changes that pass silently or appear only in summary counts

Plain English: this gate should stop obvious local/private/generated artifacts
from being committed, and it should make sensitive source-path changes visible
without pretending to decide whether those source changes are semantically
allowed.

## Owning Layer

Repository coordination and agent workflow.

This hardening gate owns repo-level changed-file classification. It does not
own parser truth, workbook schema truth, webhook payload truth, Apps Script
truth, match/game identity truth, final reconciliation, runtime status truth,
or secret detection by file contents.

Truth boundary:

- `docs/agent_constitution.md`, issue #34, tracker #33, and this contract own
  the initial rule intent.
- The gate owns path classification and exit-code behavior.
- Module contracts and GitHub issues own whether a protected source change is
  authorized.
- Codex reviewers and submitters own interpreting warnings against the issue,
  contract, implementation handoff, and PR template.
- CI owns enforcing the forbidden-artifact exit code once the gate is wired in.
- Workbook formulas, dashboard logic, Apps Script, webhook transport, and AI
  interpretation must not become sources of truth for protected-surface policy.

## Files Owned By This Contract

- `docs/contracts/code_hardening_protected_surface_gate.md`

Expected future implementation files owned by this contract:

- `tools/check_protected_surfaces.py`
- `tests/test_check_protected_surfaces.py`

Related files whose behavior is referenced but not owned by this contract:

- `docs/agent_constitution.md`
- `docs/agent_rules.yml`, when present on the target branch
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `.github/pull_request_template.md`
- `.github/workflows/repo-checks.yml`
- `tools/run_repo_checks.ps1`
- `tools/run_touched_file_checks.ps1`
- `.gitignore`
- `tools/google_apps_script/Code.gs`
- `src/mythic_edge_parser/events.py`
- `src/mythic_edge_parser/app/state.py`
- `src/mythic_edge_parser/app/models.py`
- `src/mythic_edge_parser/app/extractors.py`
- `src/mythic_edge_parser/app/sheet_schema.py`
- `src/mythic_edge_parser/app/outputs.py`
- `src/mythic_edge_parser/app/transforms.py`
- `src/mythic_edge_parser/app/runtime_surfaces.py`
- `src/mythic_edge_parser/app/config.py`
- `src/mythic_edge_parser/app/runner.py`

## Public Interface

### Command

Required initial CLI:

```bash
python3 tools/check_protected_surfaces.py --base <git-ref>
```

Windows-compatible invocation:

```powershell
py tools/check_protected_surfaces.py --base <git-ref>
```

Required arguments:

- `--base <git-ref>`: base branch or ref used to compute changed paths.

Required behavior:

- Compare changed paths from `<git-ref>...HEAD`.
- Inspect committed branch diffs, not arbitrary file contents.
- Exit nonzero only when forbidden committed artifacts are present or when the
  gate cannot compute the changed-file list.
- Print warnings for protected source-path changes without failing the first
  version.

Optional implementation details are allowed if they do not change the contract:

- `--format text`
- `--format json`
- `--github-annotations`
- `--repo-root <path>`
- `--paths-from-stdin` or equivalent test seam

Those optional flags must not be required for the baseline local or CI
invocation.

### Python API

The first implementation may expose small helper functions for tests, such as:

- path normalization
- path classification
- changed-file command construction
- report rendering

If exposed, these helpers are internal to the tool and tests. The stable public
interface is the command above.

## Inputs

### Base Ref

Type: `str`

Source:

- local user command
- GitHub Actions base branch/ref
- Codex F or Codex G handoff prompt

Examples:

- `origin/main`
- `origin/codex/parser-module-audit-suite`
- `origin/codex/code-hardening-suite`

Contract:

- The caller must pass the intended base explicitly.
- The tool should not silently assume `main` for all work.
- If the base ref is missing or invalid, the tool should exit with a clear
  configuration error.

### Changed Paths

Type: `list[str]`

Primary source:

```bash
git diff --name-only <base>...HEAD
```

Allowed equivalent:

- `git diff --name-only --diff-filter=ACMRTUXB <base>...HEAD`

The implementation may exclude deletions from classification because deleted
forbidden files are not committed artifacts in the resulting tree. If deletions
are included in the changed list, they should not cause false forbidden-file
failures unless the implementation explicitly proves the forbidden file still
exists in the branch.

Initial scope:

- branch/PR committed diff paths only
- no untracked-file scan
- no content scan
- no secret-value scan
- no semantic parser/workbook/App Script validation

### Policy Sources

Initial policy source priority:

1. active system/developer/user instructions
2. issue #34 and tracker #33
3. this contract
4. `docs/agent_constitution.md`
5. `.gitignore`
6. `.github/pull_request_template.md`
7. `docs/agent_rules.yml`, when present and reconciled by a future workflow
   change

The executable first version may encode the policy table from this contract in
the tool. It is not required to parse YAML in the first implementation.

## Path Normalization

Required normalization:

- Treat all paths as repo-relative paths.
- Convert backslashes to forward slashes.
- Strip leading `./`.
- Strip repeated leading slashes.
- Collapse redundant `.` path segments where practical.
- Do not require paths to exist for classification tests.
- Do not follow symlinks to classify the target path.
- Treat matching as case-sensitive unless a future contract explicitly changes
  Windows case-folding behavior.

Rationale:

- CI runs on Windows today, but git diff path output is slash-separated.
- Local Codex usage may pass paths with Windows-style separators.
- Classification tests should be deterministic on macOS, Linux, and Windows.

## Classification Policy

### Forbidden Committed Files

Forbidden classifications must fail the gate.

These are clearly disallowed committed artifacts:

| Category | Required path patterns or filenames | Rationale |
| --- | --- | --- |
| Local MTGA logs | `Player.log`, `Player-prev.log`, `*.Player.log`, `*.player.log`, `data/match_logs/**` | Raw local logs must not be committed. Sanitized fixtures under `tests/fixtures/**` are allowed. |
| Runtime logs | `data/runtime_logs/**`, `*.runtime.log` | Local runtime output is not source. |
| Runtime status files | `data/status/**` | Runtime status snapshots are local generated state. |
| Failed posts | `data/failed_posts/**` | Failed webhook queues may contain private payloads. |
| Bad event captures | `data/bad_events/**` | Local diagnostics may contain raw private data. |
| Generated card/oracle data | `data/oracle_data/**`, `data/tier_sources/**`, `data/decklists/**` | Generated or local card/deck/tier data must not silently become source. |
| Raw workbook exports | `data/workbook_exports/**`, `workbook_exports/**`, `exports/workbook/**`, `*.xls`, `*.xlsx`, `*.xlsm` outside explicitly documented fixtures | Workbook exports are local artifacts unless a future issue authorizes a fixture. |
| Secrets and credentials by filename | `.env`, `.env.*`, `*.pem`, `*.key`, `*.p12`, `*.pfx`, `id_rsa`, `id_dsa`, `credentials.json`, `client_secret*.json`, `token.json`, `secrets.*` | Obvious secret-bearing files must fail by path alone. |
| Webhook/API credential files by filename | `webhook_url*`, `webhook*.secret`, `api_key*`, `*token*` when the filename is clearly a credential artifact | Prevent accidental committed integration credentials. |
| Local review/app artifacts | `_review_*/**`, `.github/Mythic-Edge/**` | Already ignored local workflow artifacts should not be committed. |

Notes:

- The first version is path-based only. It must not scan file contents for
  secret strings.
- The gate should keep tests for common false positives, such as ordinary
  source files whose content may mention "token" in code but whose path is not
  a credential artifact.
- Sanitized committed fixtures under `tests/fixtures/**` are not forbidden
  merely because they use `.log`.

### Protected-Surface Warnings

Protected classifications must warn/report but must not fail the gate in the
first implementation.

These paths are ambiguous because they may be legitimate, but they touch
surfaces that require explicit issue/contract authority:

| Category | Required path patterns | Warning reason |
| --- | --- | --- |
| Parser event classes | `src/mythic_edge_parser/events.py` | Event class shape and performance classes are protected. |
| Parser state final reconciliation | `src/mythic_edge_parser/app/state.py`, `src/mythic_edge_parser/app/models.py` | Match/game final truth and reconciliation are protected. |
| Extractor behavior | `src/mythic_edge_parser/app/extractors.py` | Extractor changes can move parser truth. |
| Match/game identity and deduplication | `src/mythic_edge_parser/app/state.py`, `src/mythic_edge_parser/app/transforms.py`, `src/mythic_edge_parser/app/gameplay_actions.py`, parser modules under `src/mythic_edge_parser/parsers/**` | Identity and dedupe changes must be authorized. |
| Workbook schema and exports | `src/mythic_edge_parser/app/sheet_schema.py`, `src/mythic_edge_parser/app/sheet_exports.py`, `src/mythic_edge_parser/app/transforms.py` | Workbook-facing row shape is protected. |
| Webhook payload shape | `src/mythic_edge_parser/app/outputs.py`, `src/mythic_edge_parser/app/runner.py`, `src/mythic_edge_parser/app/transforms.py` | Transport should move parser facts, not redefine them. |
| Apps Script behavior | `tools/google_apps_script/**` | Deployed receiver behavior is protected. |
| Environment variables and runtime paths | `src/mythic_edge_parser/app/config.py`, `.github/workflows/**`, `tools/run_repo_checks.ps1`, `tools/run_touched_file_checks.ps1` | Env and CI behavior can change runtime assumptions. |
| Workflow/authority docs | `docs/agent_constitution.md`, `docs/agent_rules.yml`, `docs/codex_module_workflow.md`, `docs/agent_threads/**`, `docs/templates/**`, `.github/pull_request_template.md`, `.github/ISSUE_TEMPLATE/**` | Workflow authority changes need review. |

Warning text must tell the user that protected-surface changes require an
explicit issue/contract or reviewer acknowledgement. It must not say that the
change is automatically wrong.

### Ordinary Allowed Paths

Ordinary paths produce no warning unless they also match a forbidden or
protected class.

Examples:

- `docs/contracts/code_hardening_protected_surface_gate.md`
- `tools/check_protected_surfaces.py`
- `tests/test_check_protected_surfaces.py`
- README or docs files outside workflow authority docs
- source files not matched by protected path classes

## Classification Precedence

Required precedence:

1. forbidden
2. protected warning
3. allowed

If a path matches both forbidden and protected categories, it is forbidden.

Every classified item should include:

- normalized path
- severity: `forbidden`, `warning`, or `allowed`
- category id
- short human-readable reason

Category ids should be stable, lowercase, and machine-readable, for example:

- `local_mtga_log`
- `runtime_status`
- `failed_posts`
- `secret_file`
- `parser_event_classes`
- `workbook_schema`
- `apps_script_behavior`

## Exit-Code Behavior

Required exit codes:

- `0`: no forbidden paths were found, even if protected warnings were found
- `1`: one or more forbidden paths were found
- `2`: usage/configuration error, such as missing `--base`, invalid base ref,
  failure to run git, or unreadable repo state

Warnings must not fail CI in the first version.

Any future escalation that makes protected warnings fail CI requires explicit
user approval and a new or amended contract.

## Report Format

The default report must be stable plain text suitable for local terminals and
GitHub Actions logs.

Minimum required fields:

- gate name: `Protected Surface Gate`
- base ref
- head ref or `HEAD`
- changed path count
- forbidden count
- protected warning count
- one line per forbidden path
- one line per protected warning path
- final result line

Recommended text shape:

```text
Protected Surface Gate
base: origin/codex/code-hardening-suite
head: HEAD
changed_paths: 3
forbidden: 1
warnings: 1

FORBIDDEN local_mtga_log data/match_logs/2026-05-14/raw.jsonl - Local MTGA logs must not be committed.
WARNING parser_state_final_reconciliation src/mythic_edge_parser/app/state.py - Protected parser state surface; issue/contract must authorize this change.

result: failed
```

When there are no matches, the report should still print a concise pass
summary.

Optional JSON output or GitHub Actions annotation output may be added if it is
covered by tests, but plain text is required.

## Local Invocation Mode

Required local example:

```bash
python3 tools/check_protected_surfaces.py --base origin/codex/code-hardening-suite
```

Windows example:

```powershell
py tools/check_protected_surfaces.py --base origin/codex/code-hardening-suite
```

Local behavior:

- compare committed branch diff against the explicit base
- print the report
- exit by the rules above
- do not inspect untracked files in the first version
- do not require network access

Codex F and Codex G should use the report as evidence before PR submission or
deployment once the tool exists.

## CI Invocation Mode

Expected first CI integration:

- add a step to `.github/workflows/repo-checks.yml`
- run on `pull_request`
- use the pull request base ref as `--base`
- fail only for forbidden files
- allow protected warnings to appear in logs

Push-event behavior may initially be skipped or run against a conservative
default if GitHub Actions base detection is ambiguous. If push-event behavior is
implemented, it must be documented in the implementation handoff.

The first CI integration must not replace tests or Ruff. It should be an
additional guardrail.

## Rollout Boundaries

In scope for the first implementation:

- path-based gate script
- focused path classification tests
- explicit base-ref comparison
- plain-text report
- forbidden failures
- protected warnings
- optional repo-check / CI integration if done conservatively

Out of scope for the first implementation:

- content-based secret scanning
- scanning local untracked files
- making protected warnings fail CI
- semantic parser/schema/workbook validation
- automatic PR template interpretation
- reading GitHub issue bodies to decide authorization
- changing parser behavior
- changing parser state final reconciliation
- changing workbook schema or webhook payload shape
- changing Apps Script behavior
- changing parser event classes
- changing match/game identity or deduplication
- changing secrets, environment variables, raw logs, generated data, runtime
  status files, failed posts, or workbook exports

## Error Behavior

The tool should fail closed for configuration errors:

- missing `--base`: exit `2`
- invalid base ref: exit `2`
- git command failure: exit `2`
- not running in a git checkout and no explicit test path list is supplied:
  exit `2`

The tool should not fail on protected warnings in the first version.

The tool should not crash on unusual path separators, repeated slashes, or
leading `./`; those should normalize.

If a classification rule is ambiguous, prefer warning over failing unless the
path is clearly forbidden by this contract.

## Side Effects

The gate should be read-only.

It must not:

- edit files
- stage files
- commit files
- delete artifacts
- rewrite `.gitignore`
- mutate runtime state
- post webhooks
- update workbook tabs
- call Apps Script
- create issues or PRs
- fetch network resources unless a future CI contract explicitly authorizes it

It may read git metadata, changed-file lists, and repository files needed for
classification.

## Dependency Order

Implementation threads should evaluate changes in this order:

1. `docs/contracts/code_hardening_protected_surface_gate.md`
2. `tools/check_protected_surfaces.py`
3. `tests/test_check_protected_surfaces.py`
4. `.github/workflows/repo-checks.yml`, only if CI integration is included
5. `tools/run_repo_checks.ps1`, only if local repo-check integration is
   included
6. `tools/run_touched_file_checks.ps1`, only if touched-file check integration
   is included
7. `.github/pull_request_template.md`, only if the implementation uncovers a
   documentation gap and the issue scope explicitly allows it
8. `docs/agent_rules.yml`, only if a separate branch-sync or rule-index change
   is explicitly authorized

Do not start with parser, workbook, webhook, Apps Script, dashboard, or runtime
behavior changes.

## Compatibility

Compatibility surfaces that must remain stable:

- explicit `--base` argument
- plain-text report
- exit code `0` for warnings-only reports
- exit code `1` for forbidden paths
- exit code `2` for usage/configuration errors
- repo-relative slash-normalized paths in output
- stable severity labels: `FORBIDDEN` and `WARNING`
- no content scanning in the first version
- no untracked-file scanning in the first version

Breaking changes that require a new or amended contract:

- making protected warnings fail CI
- adding content secret scanning
- changing from explicit `--base` to an implicit default-only mode
- failing on all parser source changes
- failing on all workflow-doc changes
- scanning untracked files by default
- changing protected path classes without updating tests
- making the gate mutate the worktree
- moving parser/workbook/App Script truth into the gate

## Tests Required

Focused tests expected for Module Implementer or Module Fixer:

- Path normalization:
  - backslashes become forward slashes
  - leading `./` is stripped
  - repeated leading slashes do not break classification
  - matching is deterministic for paths that do not exist
- Forbidden classification:
  - raw local logs fail
  - ignored `data/match_logs/**`, `data/status/**`, `data/failed_posts/**`,
    `data/runtime_logs/**`, `data/bad_events/**`, and generated data paths
    fail
  - obvious secret filenames fail
  - raw workbook export filenames fail
  - sanitized `tests/fixtures/*.log` is allowed
- Protected warning classification:
  - `events.py` warns
  - `state.py` warns
  - `models.py` warns
  - `extractors.py` warns
  - `sheet_schema.py` warns
  - `outputs.py` warns
  - `tools/google_apps_script/Code.gs` warns
  - `app/config.py` warns
  - workflow authority docs warn
- Precedence:
  - forbidden beats warning
  - allowed paths do not warn
- Exit behavior:
  - allowed-only paths exit `0`
  - warnings-only paths exit `0`
  - any forbidden path exits `1`
  - missing/invalid base exits `2`
- Report format:
  - includes base, head, changed count, forbidden count, warning count, and
    result
  - includes category id and normalized path for each finding
- Git diff integration:
  - changed-file collection uses `<base>...HEAD`
  - deleted files do not create false forbidden failures, or deletion behavior
    is explicitly tested
- CI/local integration, if implemented:
  - repo-check workflow invokes the gate with the correct base
  - PowerShell wrapper invocation works or is explicitly left out of scope

Validation commands:

```bash
python3 -m pytest -q tests/test_check_protected_surfaces.py
python3 tools/check_protected_surfaces.py --base origin/codex/code-hardening-suite
python3 -m ruff check tools tests
git diff --check
```

Before submitter opens or updates a hardening PR:

```bash
python3 -m pytest -q
python3 -m ruff check src tests tools
```

If CI integration is included:

```bash
gh pr checks <pr-number>
```

## Acceptance Criteria

- The contract clearly names the repo-workflow owning layer.
- The first gate's public CLI is defined.
- Base-branch comparison behavior is defined.
- Path normalization behavior is defined.
- Forbidden path classes are explicit.
- Protected warning path classes are explicit.
- Warnings do not fail CI in the first version.
- Exit codes are defined.
- Plain-text report shape is defined.
- Local and CI invocation modes are defined.
- The missing `docs/agent_rules.yml` branch risk is recorded.
- Tests are sufficient to prove classification, report, and exit behavior.
- The gate is read-only.
- Parser/runtime/workbook/App Script behavior remains unchanged.

## Next Workflow Action

Next role: Codex C, Module Implementer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.

Act as Codex C: Module Implementer for issue #34 and docs/contracts/code_hardening_protected_surface_gate.md.

Goal:
Compare the current repo workflow, CI scripts, and contract against the protected-surface diff gate requirements. Implement only the smallest coherent tooling and test changes needed to satisfy the contract.

Use:
- https://github.com/Tahjali11/Mythic-Edge/issues/34
- https://github.com/Tahjali11/Mythic-Edge/issues/33
- docs/agent_constitution.md
- docs/agent_threads/implementation.md
- docs/codex_module_workflow.md
- docs/contracts/code_hardening_protected_surface_gate.md
- .github/pull_request_template.md
- .github/workflows/repo-checks.yml
- tools/run_repo_checks.ps1
- tools/run_touched_file_checks.ps1
- .gitignore

Do:
- Compare current repo state against the contract before editing.
- Preserve the gate as repo-workflow tooling, not parser/workbook truth.
- Add `tools/check_protected_surfaces.py` or an equivalent minimal tool only if needed.
- Add focused tests for classification, path normalization, report shape, and exit-code behavior.
- Keep the first rollout conservative: fail only clearly forbidden committed files; warn/report ambiguous protected surfaces.
- Produce docs/implementation_handoffs/code_hardening_protected_surface_gate_comparison.md with comparison, changes made, validation run, open risks, and next recommended role.

Do not:
- Make ambiguous protected-surface warnings fail CI without explicit user approval.
- Add content secret scanning unless routed through a new contract.
- Scan untracked files by default unless the contract is amended.
- Change parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match/game identity, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, or workbook exports.
- Move parser-owned truth into the gate, workbook formulas, dashboard logic, Apps Script, webhook transport, or AI-generated interpretation.
- Target main; hardening PR work belongs on codex/code-hardening-suite.
- Stage or commit unless explicitly asked.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/34"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/33"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/code_hardening_protected_surface_gate.md"
  target_artifact: "docs/implementation_handoffs/code_hardening_protected_surface_gate_comparison.md"
  risk_tier: "Medium"
  branch: "codex/code-hardening-suite"
  validation:
    - "git diff --check"
  stop_conditions:
    - "Do not make ambiguous protected-surface warnings fail CI without explicit user approval."
    - "Do not add content secret scanning unless routed through a new contract."
    - "Do not scan untracked files by default unless the contract is amended."
    - "Do not change parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match/game identity, deduplication, secrets, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not target main; hardening PR work belongs on codex/code-hardening-suite."
```

## Handoff Packet

Role performed: Codex B, Module Contract Writer.

Source problem representation: GitHub issue #34, tracked by Code Hardening
suite tracker #33.

Contract produced: `docs/contracts/code_hardening_protected_surface_gate.md`

Tracker issue: https://github.com/Tahjali11/Mythic-Edge/issues/33

Risk tier: Medium.

Owning truth layer: repository coordination and agent workflow.

Public interface:

- `python3 tools/check_protected_surfaces.py --base <git-ref>`

Invariants:

- The gate is read-only.
- The caller passes the base ref explicitly.
- The first version inspects committed branch diffs, not untracked files.
- The first version is path-based and does not scan file contents for secrets.
- Forbidden committed artifacts fail the gate.
- Ambiguous protected-surface changes warn/report but do not fail.
- Exit codes are `0` pass or warnings-only, `1` forbidden paths, `2`
  usage/configuration error.
- Parser/runtime/workbook/App Script behavior remains unchanged.

Required tests: path normalization, forbidden classification, protected warning
classification, precedence, exit behavior, report shape, git diff integration,
and optional CI/local invocation tests listed in `Tests Required`.

Acceptance criteria: listed above.

Open questions or contract risks:

- `docs/agent_rules.yml` is referenced by issue #34 but absent on the current
  `codex/code-hardening-suite` branch.
- The first policy table is encoded in this contract rather than parsed from a
  machine-readable rule file.
- Content secret scanning is intentionally out of scope.
- Untracked file scanning is intentionally out of scope for the first version.
- Protected-surface warnings may need escalation in a future contract after the
  warning-only rollout proves stable.

Next recommended thread role: Codex C, Module Implementer.
