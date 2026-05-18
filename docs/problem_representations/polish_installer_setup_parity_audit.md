# Installer And Setup Polish Parity Audit

## Summary

This audit compares Manasight's installer/setup polish against Mythic Edge's
current Python setup, local validation, CI, sanitizer, and repository
presentation surfaces. Mythic Edge already exceeds Manasight in governance,
protected-surface workflow, schema snapshots, golden replay, and parser
reliability artifacts, but Manasight is cleaner on public installation,
toolchain pinning, lockfile reproducibility, CI breadth, security scanning,
dependency automation, and public-facing setup documentation.

## Source Request Or Issue

Source request: perform a parity audit for installer and setup polish between
Mythic Edge and Manasight, and add the results to the Polish and Discipline
suite.

Related suite artifact:

- `docs/problem_representations/polish_and_discipline_suite.md`

No GitHub issue has been created by this artifact.

## Source Artifacts Inspected

Manasight reference checkout:

- `Cargo.toml`
- `Cargo.lock`
- `rust-toolchain.toml`
- `Makefile`
- `deny.toml`
- `rustfmt.toml`
- `.gitleaks.toml`
- `README.md`
- `CONTRIBUTING.md`
- `CONVENTIONS.md`
- `SECURITY.md`
- `.github/dependabot.yml`
- `.github/PULL_REQUEST_TEMPLATE.md`
- `.github/workflows/ci.yml`
- `.github/workflows/smoke-test.yml`
- `.github/workflows/gitleaks.yml`
- `.github/workflows/semgrep.yml`
- parser smoke and ratchet tests under `tests/`
- sanitizer CLI and sanitizer tests under `src/bin/scrub.rs` and
  `src/sanitize.rs`

Mythic Edge current branch:

- `pyproject.toml`
- `pyrightconfig.json`
- `README.md`
- `CONTRIBUTING.md`
- `.gitignore`
- `.github/pull_request_template.md`
- `.github/workflows/repo-checks.yml`
- `src/mythic_edge_parser/bin/scrub.py`
- `src/mythic_edge_parser/sanitize.py`
- `tools/run_repo_checks.ps1`
- `tools/run_touched_file_checks.ps1`
- `tools/run_pyright_advisory.ps1`
- `tools/check_protected_surfaces.py`
- golden replay and feature-equity corpus surfaces under `src/`, `tests/`,
  and `docs/`

## Audit Scope

In scope:

- local installation and setup reproducibility
- version and dependency management
- one-command local validation
- CI coverage for tests, lint, type checking, security, dependencies, and smoke
  tests
- public sanitizer and security docs
- issue/PR/development workflow presentation
- Python analogs for Manasight's Rust setup discipline

Out of scope:

- parser behavior changes
- parser event class changes
- match/game identity
- deduplication
- workbook schema
- webhook payload shape
- Apps Script behavior
- raw log fixture import
- generated data
- production deployment
- copying Manasight code

## Top-Level Finding

Manasight's setup polish is compact and public-package oriented: `cargo add`,
MSRV, `rust-toolchain.toml`, `Cargo.lock`, `make precommit`, CI, dependency
deny rules, Gitleaks, Semgrep, Dependabot, smoke corpus tests, sanitizer docs,
and release workflows all give a new contributor a clear path.

Mythic Edge's setup is stronger as a personal production-adjacent workflow
system: it has detailed governance, protected-surface policy, a strong PR
template, schema snapshots, golden replay, feature-equity corpus reporting, and
branch/issue discipline. The missing polish is not "more governance"; it is
the ordinary engineering ergonomics that make a repo easy to install, verify,
and trust from a fresh machine.

## Parity Matrix

| Setup Surface | Manasight Reference | Mythic Edge Current State | Parity Status | Recommended Suite Item |
| --- | --- | --- | --- | --- |
| Public install path | README advertises `cargo add manasight-parser` and `Cargo.toml` dependency syntax. | README documents editable local install with `pip install -e .[dev]`; no public package install story. | Partial | Python version and lockfile policy; README/setup polish. |
| Runtime version policy | `Cargo.toml` declares `rust-version = "1.93.0"` and `rust-toolchain.toml` pins `1.93.0`. | `pyproject.toml` declares `requires-python = ">=3.11"`; CI uses Python `3.13`; Ruff targets `py311`; no `.python-version`. | Partial | Add `.python-version`; reconcile supported floor vs recommended dev version. |
| Lockfile reproducibility | `Cargo.lock` is committed. | No `uv.lock`, `pylock.toml`, or requirements lockfile observed. | Missing | Add a lockfile policy before committing a lockfile. |
| Package metadata | `Cargo.toml` has name, version, description, license, repository, readme, keywords, categories, and binary entrypoint. | `pyproject.toml` has project metadata, dependencies, optional dev deps, and script entrypoints. Repository URL is not currently declared. | Mostly covered | Add repository/project URL metadata if desired. |
| CLI entrypoints | `scrub` binary reads stdin and writes sanitized output. | `mythicedge-scrub` and compatibility `manasight-scrub` scripts exist. | Covered | Improve docs and tests around public scrub usage. |
| One-command local checks | `Makefile` provides `make precommit`, `make precommit-trivial`, `make coverage`, and `make fmt`. | `tools/run_repo_checks.ps1`, touched-file lint, and Pyright advisory scripts exist, but are Windows-first and split across commands. | Partial | Add one cross-platform validation entrypoint or documented command family. |
| Formatting and linting | `rustfmt.toml`; `cargo fmt`; Clippy lint policy in `Cargo.toml` with important restriction lints denied. | Ruff is configured for `E`, `F`, and `I`; no formatter command is documented as canonical. | Partial | Decide whether Ruff format or another formatter belongs in one-command checks. |
| Type/static analysis | Rust compiler plus Clippy provide strong default type and lint guarantees. | Pyright exists as advisory in `pyrightconfig.json` with `typeCheckingMode = "basic"`. | Partial | Implement staged Python type-discipline ladder. |
| Dependency and license checks | `deny.toml` and CI `cargo deny` check advisories, licenses, bans, and sources. | No Python dependency/license CI observed. | Missing | Evaluate `pip-audit`, `pip-licenses`, GitHub dependency review, or equivalent. |
| Secret scanning | `.gitleaks.toml` plus Gitleaks workflow. | Protected-surface policy exists; no `.gitleaks.toml` or Gitleaks workflow observed on this branch. | Missing/partial | Add Gitleaks or repo-local secret scanner workflow after contract. |
| Static security scanning | Semgrep workflow with Rust rules. | No Semgrep workflow observed. | Missing | Add Semgrep Python workflow if useful and low-noise. |
| Dependabot | Weekly Cargo and GitHub Actions Dependabot config. | No `.github/dependabot.yml` observed. | Missing | Add Dependabot for `pip`/Python ecosystem and GitHub Actions. |
| CI checks | CI runs format, Clippy, tests, no-default-features tests, and cargo deny on Ubuntu. | CI runs Windows tests, protected-surface gate on PRs, and Ruff. | Partial | Expand CI lanes while preserving advisory vs required boundaries. |
| Smoke/corpus tests | Smoke workflow downloads a corpus, runs real-log parser smoke, compares to `smoke-baseline.json`, uploads reports, and can auto-open baseline update PRs. | Golden replay and feature-equity corpus ratchet exist; no public/full-corpus CI workflow or root `smoke-baseline.json` equivalent observed. | Partial but strong foundation | Add report-only smoke workflow over committed sanitized fixtures first. |
| Sanitizer documentation | README documents sanitizer behavior, compression/hash helpers, and CLI usage. | Sanitizer CLI exists, but README does not yet present it as a public privacy boundary. | Partial | Add public sanitizer docs and usage examples. |
| Sanitizer test depth | Manasight has extensive sanitizer unit tests and optional corpus scrub test. | Mythic Edge has sanitizer tests and golden fixture privacy checks; optional corpus scrub parity should be reviewed. | Partial | Add sanitizer parity contract if public fixture sharing grows. |
| Security policy | `SECURITY.md` exists with private vulnerability reporting guidance. | No `SECURITY.md` observed. | Missing | Add security policy suited to a personal project. |
| Contribution docs | `CONTRIBUTING.md`, `CONVENTIONS.md`, code of conduct, issue templates, PR template. | `CONTRIBUTING.md`, module workflow issue template, strong PR template, AGENTS/governance docs. No `SECURITY.md` or code of conduct observed. | Partial/covered+ | Keep Mythic workflow docs, add conventional public-facing docs selectively. |
| PR template | Simple checklist for tests, Clippy, fmt, tests, docs. | Strong protected-surface, drift, contract, validation, and lifecycle template. | Exceeds | No parity gap; only add setup/polish checklist items if helpful. |
| Issue templates | Bug and feature request templates. | Module workflow issue template exists. | Different strengths | Optional ordinary bug/feature templates; current module template is stronger for Codex workflow. |
| Release/publish workflow | Release and publish-crate workflows exist. | No release or package publish workflow observed. | Missing/defer | Defer unless Mythic Edge is packaged for repeat local installs or public distribution. |
| Cross-platform posture | Cargo/Rust setup is naturally cross-platform; CI uses Ubuntu. | README and helper scripts are Windows-first; CI is Windows-only. | Partial | Add macOS/Linux setup docs before adding broad CI. |
| Local application setup | Manasight parser is a library crate, not a local desktop app installer. | Mythic Edge has an auto launcher and local operator scripts. | Mythic-specific strength | Future installer polish can exceed Manasight by packaging the launcher. |

## Mythic Edge Strengths To Preserve

- Stronger protected-surface and truth-ownership policy than Manasight.
- Stronger PR template for parser/workbook/webhook/App Script safety.
- Golden replay harness already gives sanitized expected-output replay
  coverage.
- Feature-equity corpus ratchet already gives a count-only regression path over
  committed golden replay manifests.
- Schema snapshots protect parser event classes, payload keys, workbook row
  keys, runtime export rows, and Apps Script repo parity.
- Local launcher/operator tooling is a Mythic-specific strength that Manasight
  does not need as a library crate.

These should not be replaced by Manasight's simpler pattern. The right move is
to add Manasight-style setup clarity underneath Mythic Edge's existing
governance.

## Recommended Polish Modules

### Module 1: Python Version And Lockfile Policy

Priority: high.

Reason:

This is the Python analog to Manasight's `rust-version`,
`rust-toolchain.toml`, and `Cargo.lock`.

Expected outputs:

- `.python-version`
- documented supported Python floor
- documented recommended development Python version
- decision on `uv.lock` or an equivalent lockfile
- Windows and macOS setup commands
- clear separation between parser runtime deps and dev/workflow deps

Stop conditions:

- do not make `uv` the only supported path without explicit approval
- do not narrow the Python support floor without contract approval
- do not commit machine-local virtual environment files

### Module 2: One-Command Local Validation

Priority: high.

Reason:

This is the Python analog to Manasight's `make precommit`.

Expected outputs:

- a canonical command for routine local validation
- a focused command for changed files or small edits
- a broader command for submitter/deployer readiness
- documented Windows and macOS usage

Candidate implementation shapes:

- keep PowerShell scripts and add macOS/Linux shell equivalents
- add a Python `tools/validate.py` wrapper
- add a `justfile` if the project wants an external command runner

Recommended direction:

Prefer a Python wrapper first because Python already exists in the project
toolchain and works across Windows/macOS/Linux.

### Module 3: CI Security, Dependency, And Smoke Expansion

Priority: medium-high.

Reason:

This is the Python analog to Manasight's CI, `cargo deny`, Gitleaks, Semgrep,
Dependabot, and smoke corpus workflow.

Expected outputs:

- Python dependency/advisory check
- license check or documented license policy
- Gitleaks or equivalent secret scanning
- Semgrep Python scan if signal-to-noise is acceptable
- Dependabot for Python package metadata and GitHub Actions
- report-only smoke workflow before any failing real-log gate

Stop conditions:

- do not make noisy new checks required before they are proven stable
- do not commit raw local logs or private corpus data
- do not auto-refresh baselines without review policy

### Module 4: Public Sanitizer And Security Presentation

Priority: medium.

Reason:

Mythic Edge already has the core scrub CLI. The gap is documentation and public
trust polish.

Expected outputs:

- README sanitizer section
- explicit `mythicedge-scrub` usage examples
- `SECURITY.md`
- private data handling and raw-log sharing warnings
- optional sanitizer parity tests if future contracts authorize them

Stop conditions:

- do not claim sanitizer completeness beyond tested patterns
- do not encourage sharing raw logs
- do not change sanitizer behavior in a docs-only pass

### Module 5: Setup Presentation And Release Readiness

Priority: medium/defer.

Reason:

Manasight is a published parser library. Mythic Edge is currently a personal
local application/pipeline. It does not need crate-style release polish yet,
but it does need a clean "new machine setup" story.

Expected outputs:

- README setup refresh
- optional `docs/setup.md`
- local machine bootstrap commands
- laptop/desktop handoff guidance
- later packaging decision for launcher/installer

Stop conditions:

- do not add package publishing workflows unless the project intentionally
  becomes distributable
- do not add installer behavior that touches credentials, webhook URLs, or live
  workbook state

## Recommended Type-Discipline Modules Related To Setup

The main type-discipline ladder belongs in
`docs/problem_representations/polish_and_discipline_suite.md`. For setup
parity, the relevant type-discipline additions are:

- Pyright advisory reporting should be included in one-command validation.
- Targeted Pyright strictness should be introduced per module, not globally.
- Public CLI boundaries should have typed argument/return contracts.
- Setup scripts should avoid untyped shell-only logic where a Python wrapper
  can produce structured output.
- CI should distinguish advisory type reports from required merge gates until a
  contract escalates them.

## Recommended Ordering

1. Python version and lockfile policy.
2. One-command local validation.
3. Public sanitizer and security presentation.
4. CI security, dependency, and smoke expansion.
5. Setup presentation and release-readiness polish.
6. Type-discipline ladder modules, beginning with new parser surfaces and CLI
   boundaries.

This ordering gives the project a stable local setup before adding more CI
lanes. It also avoids forcing Pyright or smoke reports into failing gates before
their noise level is known.

## Risks

- Dependency tool churn could make local setup harder rather than easier.
- New CI jobs may fail for environmental reasons unrelated to parser quality.
- Security scanners can produce false positives unless allowlists are
  reviewed.
- A lockfile can drift if it is not updated intentionally.
- Smoke tests can leak private data if fixture policy is bypassed.
- Public sanitizer docs could create false confidence if they imply the scrubber
  is complete for every future Player.log shape.
- Over-tight typing can break tolerant parser behavior if raw evidence and
  normalized parser-owned payloads are not kept separate.

## Recommended Next Workflow Action

Next role:

- Codex A to create a GitHub tracker and child issues, or
- Codex B to write the first contract:
  `docs/contracts/polish_python_version_and_lockfile_policy.md`

Recommended first contract:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex B: Module Contract Writer for the Polish and Discipline suite.

Module:
Python version and uv lockfile support

Source artifacts:
- docs/problem_representations/polish_and_discipline_suite.md
- docs/problem_representations/polish_installer_setup_parity_audit.md

Task:
Create docs/contracts/polish_python_version_and_lockfile_policy.md.

Define the contract for the Python analog to Manasight's `rust-version`,
`rust-toolchain.toml`, and `Cargo.lock`. The contract should decide the
supported Python runtime floor, recommended development Python version,
`.python-version` contents, `uv`/lockfile policy, Windows and macOS install
commands, dependency group boundaries, and validation expectations.

Read:
- AGENTS.md
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/codex_module_workflow.md
- docs/problem_representations/polish_and_discipline_suite.md
- docs/problem_representations/polish_installer_setup_parity_audit.md
- pyproject.toml
- pyrightconfig.json
- README.md
- .github/workflows/repo-checks.yml

Do not implement code.
Do not add `.python-version`, `uv.lock`, CI changes, or setup scripts in this
thread.
Do not change parser behavior, parser state final reconciliation, workbook
schema, webhook payload shape, Apps Script behavior, parser event classes,
match/game identity, deduplication, secrets, raw logs, generated data, runtime
status files, failed posts, workbook exports, or production behavior.
```

```yaml
workflow_handoff:
  issue: "recommended new tracker: [polish] Setup polish and Python type-discipline suite"
  tracker: "N/A"
  completed_thread: "A"
  next_thread: "A or B"
  source_artifact: "Manasight setup files and Mythic Edge setup surfaces"
  target_artifact: "GitHub tracker/child issues or docs/contracts/polish_python_version_and_lockfile_policy.md"
  risk_tier: "Medium"
  branch: "codex/polish-and-discipline-suite"
  validation:
    - "git diff --check"
  stop_conditions:
    - "Do not change parser behavior without issue/contract authorization."
    - "Do not commit raw logs, secrets, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not make uv the only supported setup path without explicit approval."
    - "Do not make new CI/security/type checks required until their contract defines advisory vs gate behavior."
```
