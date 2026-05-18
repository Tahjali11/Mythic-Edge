# Polish And Discipline Suite Problem Representation

## Summary

Mythic Edge should grow a dedicated polish and type-discipline suite that
adapts the strongest setup, CI, sanitizer, and type-safety patterns from
Manasight into Python-native equivalents. The goal is not to redesign parser
behavior, but to make the project easier to install, safer to validate, and
harder to accidentally weaken as parser and analytics scope expands.

## Source Request Or Issue

Source request: local Codex request to create a new "Polish and Discipline"
branch and define issues for:

1. supported Python version, `.python-version`, and `uv`/lockfile support
2. one-command local checks
3. CI for tests, lint, dependency/license checks, Gitleaks, Semgrep,
   Dependabot, and smoke tests
4. public-facing sanitizer CLI, security policy, and PR template polish
5. a ten-point ladder for stronger Python type discipline

## Tracker

Recommended new tracker issue:

```text
[polish] Setup polish and Python type-discipline suite
```

No tracker has been created by this artifact.

## Related Audit Artifacts

- `docs/problem_representations/polish_installer_setup_parity_audit.md`
  compares Manasight's installer/setup polish against Mythic Edge and maps the
  parity gaps into this suite's child modules.

## What The Project Is Supposed To Do

Mythic Edge should be installable and verifiable on a new local machine with
clear Python-version expectations, deterministic dependency setup, and one
obvious validation path. It should also make parser-owned event shapes, payload
contracts, and downstream export surfaces progressively more explicit through
Python typing, advisory static analysis, snapshots, golden fixtures, and corpus
regression checks.

## What It Is Actually Doing

Current observed setup and discipline state:

- `pyproject.toml` declares `requires-python = ">=3.11"`.
- CI currently installs Python `3.13`.
- Ruff targets Python `py311`.
- No `.python-version` file is present.
- No `uv.lock`, `pylock.toml`, or requirements lockfile is present.
- `tools/run_repo_checks.ps1` provides a Windows local check path.
- No cross-platform single command currently appears to own the full local
  validation story.
- `.github/workflows/repo-checks.yml` runs tests, protected-surface checks on
  PRs, and Ruff on Windows.
- No `SECURITY.md` is present.
- A public scrub CLI exists through the `mythicedge-scrub` project script and
  `src/mythic_edge_parser/bin/scrub.py`.
- The PR template already includes strong workflow, protected-surface, drift,
  and validation sections.
- Parser events use dataclasses, enums, protocols, and a `GameEvent` union, but
  event payloads still commonly use broad `dict[str, Any]`.
- `pyrightconfig.json` uses `typeCheckingMode = "basic"`.

## Why This Matters

This work matters because Mythic Edge is moving from a parser prototype into a
professional-grade personal data platform. As the project adds draft support,
drift protection, analytics, and eventual AI-assisted coaching, weak setup and
loose types become force multipliers for confusion:

- a laptop may run different Python or dependency versions than the desktop
- Codex threads may use different validation commands
- CI may miss dependency, secret, or security regressions
- raw log sanitizer expectations may be under-documented
- broad payload dictionaries may hide missing keys until runtime
- analytics may depend on parser-owned fields whose shape is not explicit

The intended improvement is boring repeatability: one setup story, one
validation story, explicit safety gates, and a gradual path toward richer
Python type guarantees.

## Project Layer

Primary layer:

- repository coordination and developer tooling

Secondary layers:

- parser and state interpretation
- Player.log evidence and drift protection
- future analytics foundation
- GitHub CI and security hygiene

Truth ownership must not change. Parser/state remains the truth-producing layer
for event interpretation and normalized match/game/card facts. Tooling,
typing, CI, documentation, and external scanners are validation and safety
layers only.

## First Bad Value Or First Inspection Order

No single bad runtime value is known. The first inspection order should be:

1. `pyproject.toml`
2. `pyrightconfig.json`
3. `.github/workflows/repo-checks.yml`
4. existing local validation scripts under `tools/`
5. current README development/setup instructions
6. project script entrypoints, especially `mythicedge-scrub`
7. `.github/pull_request_template.md`
8. existing tests around schema snapshots, golden replay, feature-equity corpus,
   protected-surface checks, and sanitizer behavior
9. `src/mythic_edge_parser/events.py`
10. representative parser modules under `src/mythic_edge_parser/parsers/`

## Suggested Issue Queue

### Issue 1: Python Version And Lockfile Policy

Suggested title:

```text
[polish] Python version and uv lockfile support
```

Goal:

- define the supported Python floor and the recommended local Python version
- add `.python-version`
- decide whether `uv.lock` should be committed now or introduced after a
  contract
- document install commands for Windows and macOS
- keep parser runtime dependencies separate from development/workflow tooling

Likely decisions:

- preserve `requires-python = ">=3.11"` unless a contract narrows it
- treat Python `3.13` as the current CI/recommended development version if
  confirmed
- use `uv` as a deterministic setup path without making it the only supported
  path unless explicitly approved

### Issue 2: One-Command Local Checks

Suggested title:

```text
[polish] One-command local validation entrypoint
```

Goal:

- provide a single obvious local command for routine validation
- preserve `tools/run_repo_checks.ps1` as a Windows convenience path
- consider a cross-platform Python validation wrapper or `justfile`
- route focused checks through the existing smallest-relevant-validation policy

The command should make it easy to run:

- focused tests
- full tests
- Ruff
- protected-surface check when a base ref is available
- secret/private-marker scan when available
- schema/golden/corpus checks when relevant
- Pyright advisory reporting

### Issue 3: CI Security, Dependency, And Smoke Expansion

Suggested title:

```text
[polish] CI security, dependency, license, Dependabot, and smoke checks
```

Goal:

- expand CI beyond tests/Ruff/protected-surface checks
- add dependency and license checks suitable for Python
- add Gitleaks and Semgrep workflows or documented equivalents
- add Dependabot configuration for Python and GitHub Actions
- add smoke-test workflow structure without committing raw local logs

Candidate Python analogs to evaluate:

- dependency/license review: `pip-audit`, `pip-licenses`, or GitHub dependency
  review
- secret scanning: Gitleaks plus the repo-local secret/private-marker scanner
- static security scanning: Semgrep Python rules
- smoke testing: committed sanitized fixtures, golden replay, feature-equity
  corpus, or an opt-in private local corpus path

### Issue 4: Public Sanitizer And Repository Presentation Polish

Suggested title:

```text
[polish] Public sanitizer CLI, security policy, and PR template polish
```

Goal:

- document the existing `mythicedge-scrub` CLI as a public-facing local privacy
  boundary
- add or update a `SECURITY.md`
- review README installation, sanitizer, contribution, and validation sections
- review PR template language for the new setup/type-discipline suite
- avoid publishing raw Player.log data or machine-local paths

This issue should not change sanitizer behavior unless a later contract
explicitly authorizes it.

### Issue 5: Python Type-Discipline Ladder

Suggested title:

```text
[discipline] Python type-discipline ladder for parser payloads
```

Goal:

Build a staged Python analog to Rust's compile-time guarantees without trying
to port the project to Rust or over-refactor stable parser behavior.

Recommended ten-point ladder:

1. Keep raw MTGA JSON as raw evidence, usually `dict[str, Any]`.
2. Convert raw JSON into parser-owned typed payloads at module boundaries.
3. Use `TypedDict` for known dictionary payloads that remain dictionary-shaped.
4. Use `Literal` for event kinds, payload type discriminators, and stable
   string enums.
5. Use `Enum` for controlled source, confidence, finality, and drift labels.
6. Use `dataclass(frozen=True, slots=True)` for durable normalized records
   where mutation would be risky.
7. Use `Protocol` for parser interfaces and output adapters.
8. Move Pyright strictness gradually from broad advisory to targeted stricter
   modules.
9. Protect externally visible dictionary shapes with schema snapshots.
10. Protect real behavior with golden replay, corpus regression, and drift
    reports.

Early candidate surfaces:

- new draft parser payloads
- `events.py` event kind and payload typing
- GRE `GameState` normalized payload sections
- workbook/webhook-facing row keys
- evidence-ledger value-source labels
- analytics input records once analytics work begins

## Scope

In scope:

- planning a dedicated setup polish and Python type-discipline suite
- defining likely child issues
- identifying current repo gaps and existing strengths
- preserving current parser truth ownership
- preserving docs-first or contract-first workflow before risky changes

Out of scope:

- changing parser behavior
- changing parser state final reconciliation
- changing parser event class names or event kind values without a contract
- changing workbook schema
- changing webhook payload shape
- changing Apps Script behavior
- changing match/game identity or deduplication
- committing raw logs, secrets, generated data, runtime status files, failed
  posts, or workbook exports
- making Pyright a failing gate without a contract
- making `uv` the only supported install path without a contract
- adding public corpus data without sanitizer and fixture policy review

## Risks And Likely Breakpoints

- Python version drift: `requires-python`, Ruff target version, CI version, and
  `.python-version` could disagree.
- Lockfile drift: a committed lockfile could improve reproducibility but create
  maintenance churn if ownership is unclear.
- Tooling sprawl: adding `uv`, Gitleaks, Semgrep, dependency audit, license
  audit, Pyright, Ruff, snapshots, and smoke tests without a selector could
  make validation feel heavier rather than clearer.
- CI false confidence: passing tests do not prove real-log replay quality.
- Smoke fixture risk: real Player.log data must not enter the repo unless
  sanitized and explicitly approved.
- Type overreach: replacing broad parser dictionaries too aggressively could
  change tolerant parsing behavior.
- Pyright escalation risk: moving from advisory to required too soon could
  block unrelated parser work.
- Public sanitizer presentation risk: docs should not imply raw logs are safe
  to publish before sanitizer guarantees are contract-tested.

## Validation Evidence Needed

For this planning artifact:

```powershell
git diff --check
```

For future implementation issues, likely checks include:

```powershell
py -m pytest -q tests
py -m ruff check src tests tools
.\tools\run_repo_checks.ps1
.\tools\run_pyright_advisory.ps1
```

When implemented on branches containing the newer hardening tools, also run the
appropriate secret/private-marker scanner, protected-surface gate, validation
selector, schema snapshot tests, golden replay, and feature-equity corpus
checks.

## Open Questions

- Should the recommended local Python version be `3.13`, while the supported
  runtime floor remains `>=3.11`?
- Should `uv.lock` be committed immediately, or should lockfile support first
  be documented as an optional setup path?
- Should one-command checks be owned by a Python script, a `justfile`, a
  Makefile, PowerShell scripts, or a combination?
- Should CI remain Windows-first, or add Linux/macOS jobs for portability?
- Which dependency/license tool is the best fit for this repo?
- Should Gitleaks/Semgrep be GitHub Actions only, local optional tools, or both?
- Which parser module should be the first strict typing pilot?
- Should Pyright strictness remain global basic plus targeted strict modules,
  or should a future contract introduce gradual package-wide strictness?

## Next Workflow Action

Recommended next role:

- Codex A if the next step is to create the GitHub tracker and child issues.
- Codex B if the next step is to write the first module contract, probably for
  Python version and lockfile policy.

Pasteable Codex B prompt for the first child module:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex B: Module Contract Writer for the Polish and Discipline suite
child module:

Python version and uv lockfile support

Source artifact:
docs/problem_representations/polish_and_discipline_suite.md

Task:
Create docs/contracts/polish_python_version_and_lockfile_policy.md.

Define the contract for a clear supported Python version policy, `.python-version`,
and uv/lockfile support. Distinguish required parser runtime dependencies from
development/workflow dependencies. Preserve current parser behavior and do not
implement files yet.

Read:
- AGENTS.md
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/codex_module_workflow.md
- docs/problem_representations/polish_and_discipline_suite.md
- pyproject.toml
- pyrightconfig.json
- README.md
- .github/workflows/repo-checks.yml

The contract should define:
- supported Python runtime floor
- recommended development Python version
- `.python-version` contents and rationale
- whether `uv.lock` or another lockfile should be committed
- Windows and macOS install expectations
- how optional dev/workflow dependencies should be installed
- validation commands
- protected surfaces
- out-of-scope behavior changes
- acceptance criteria
- next Codex C implementation handoff expectations

Do not implement code.
Do not add `.python-version`, `uv.lock`, or CI changes in this thread.
Do not change parser behavior, parser state final reconciliation, workbook schema,
webhook payload shape, Apps Script behavior, parser event classes, match/game
identity, deduplication, secrets, raw logs, generated data, runtime status files,
failed posts, workbook exports, or production behavior.
```

```yaml
workflow_handoff:
  issue: "recommended new tracker: [polish] Setup polish and Python type-discipline suite"
  tracker: "N/A"
  completed_thread: "A"
  next_thread: "A or B"
  source_artifact: "local user request"
  target_artifact: "GitHub tracker/child issues or docs/contracts/polish_python_version_and_lockfile_policy.md"
  risk_tier: "Medium"
  branch: "codex/polish-and-discipline-suite"
  validation:
    - "git diff --check"
  stop_conditions:
    - "Do not change parser behavior without issue/contract authorization."
    - "Do not make Pyright a failing gate without a contract."
    - "Do not commit raw logs, secrets, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not make uv the only supported setup path without explicit approval."
```
