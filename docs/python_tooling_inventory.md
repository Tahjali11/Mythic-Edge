# Python Tooling Inventory

This document describes the current Python setup for Mythic Edge. It is a
human-readable inventory, not a lock file and not dependency authority.

The authoritative dependency configuration is `pyproject.toml`. If this guide
and `pyproject.toml` disagree, update this guide to match `pyproject.toml`
rather than treating this guide as a second source of truth.

## Scope

This inventory covers local Python setup, validation commands, repo-local
quality tools, and deferred tooling candidates.

It does not change dependencies, CI gates, parser behavior, analytics behavior,
SQLite schema, local app behavior, workbook or webhook behavior, Apps Script,
AI behavior, secrets policy, raw log handling, generated artifacts, or local
machine artifacts.

## Current Python Expectations

- Project package: `mythic-edge-parser`
- Supported Python declaration: `requires-python = ">=3.11"`
- Ruff target: Python 3.11 (`target-version = "py311"`)
- Pyright target: Python 3.11 (`"pythonVersion": "3.11"`)
- GitHub Actions runner: `windows-latest`
- GitHub Actions Python: `3.13`
- Local Windows commands generally use the Python launcher: `py`
- macOS or Linux commands generally use `python3`

Recommended Windows setup from the repo root:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install --upgrade pip
py -m pip install -e ".[dev]"
```

Recommended macOS or Linux setup from the repo root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -e ".[dev]"
```

For parser runtime only:

```powershell
py -m pip install -e .
```

For local app/backend work without the full dev group:

```powershell
py -m pip install -e ".[app]"
```

## Runtime Dependencies

The core runtime dependencies are the packages listed under
`[project].dependencies` in `pyproject.toml`.

| Package | Current bound | Why it exists |
| --- | --- | --- |
| `beautifulsoup4` | `>=4.14,<5` | HTML parsing support for tier/metagame and related helper flows. |
| `requests` | `>=2,<3` | HTTP client support for repo-local integrations and sync helpers. |

The package also declares these console scripts:

| Script | Entry point |
| --- | --- |
| `mythicedge-scrub` | `mythic_edge_parser.bin.scrub:main` |
| `manasight-scrub` | `mythic_edge_parser.bin.scrub:main` |

## App And Backend Dependencies

The local app/backend dependencies live in the optional `app` group. They are
local development support and do not make the FastAPI backend parser truth,
analytics truth, workbook truth, or production behavior.

| Package | Current bound | Why it exists |
| --- | --- | --- |
| `fastapi` | `>=0.115,<1` | Local loopback backend and app route support. |
| `python-multipart` | `>=0.0.9,<1` | Browser JSONL upload form parsing for FastAPI routes. |
| `uvicorn` | `>=0.30,<1` | Local ASGI server support for the developer app launcher. |

The `dev` group also includes these app/backend packages so committed tests can
exercise the local app without a separate install step.

## Dev And Test Dependencies

The `dev` optional dependency group is the standard setup for Mythic Edge
development and validation.

| Package | Current bound | Why it exists |
| --- | --- | --- |
| `fastapi` | `>=0.115,<1` | Local backend tests and app factory coverage. |
| `httpx` | `>=0.27,<1` | FastAPI/Starlette test-client support. |
| `pytest` | `>=8,<9` | Focused and full test runs. |
| `pytest-cov` | `>=5,<6` | Optional coverage reporting. |
| `pyright` | `>=1.1,<2` | Advisory type-check report support. |
| `python-multipart` | `>=0.0.9,<1` | Upload-route tests and multipart parsing support. |
| `ruff` | `>=0.6,<1` | Lint and import-order checks. |
| `uvicorn` | `>=0.30,<1` | Local backend launcher checks. |

## Validation Commands

Common focused commands:

```powershell
py -m pytest -q tests
py -m pytest --cov=src/mythic_edge_parser --cov-report=term-missing tests
py -m ruff check src tests tools
```

Repo helper scripts:

```powershell
.\tools\run_repo_checks.ps1
.\tools\run_repo_checks.ps1 -Coverage
.\tools\run_touched_file_checks.ps1 <changed-python-file> <changed-test-file>
```

`tools/run_repo_checks.ps1` currently runs tests, or coverage tests with
`-Coverage`, then Ruff over `src` and `tests`. CI runs Ruff over `src`, `tests`,
and `tools`.

Validation selection:

```powershell
py tools\select_validation.py --base origin/<base-branch>
```

Use the selector as guidance. It recommends focused tests, required guardrails,
and advisory checks based on changed paths, but it does not replace issue or
contract-specific validation.

## Hardening, Security, And Docs Tools

These tools are repo-local Python support surfaces. They provide validation,
advisory reports, or governance consistency checks; they do not own parser
truth, workbook truth, merge readiness, deployment authority, or credential
policy.

| Tool | Purpose |
| --- | --- |
| `tools/check_agent_docs.py` | Checks consistency of governance docs, role docs, templates, and workflow references. |
| `tools/check_protected_surfaces.py` | Flags protected or forbidden path changes against a base ref. |
| `tools/check_secret_patterns.py` | Scans for secrets, private markers, raw log markers, and local artifact markers. |
| `tools/check_surface_authorization.py` | Compares protected-surface changes against supplied issue, contract, and handoff authorization files. |
| `tools/select_validation.py` | Recommends validation commands for changed repo paths. |
| `tools/run_pyright_advisory_report.py` | Runs Pyright and prints a normalized advisory report. |
| `tools/run_hardening_orchestrator.py` | Coordinates selected hardening checks without replacing their individual authority. |
| `tools/generate_hardening_report.py` | Generates deterministic hardening status Markdown from repo-local and operator-supplied evidence. |

Useful guardrail commands:

```powershell
py tools\check_agent_docs.py
py tools\check_protected_surfaces.py --base origin/<base-branch>
py tools\check_secret_patterns.py --all
py tools\check_secret_patterns.py --base origin/<base-branch>
```

`--all` secret scanning is advisory/report-oriented for the whole repo. For
module reviews, also consider a path-scoped scan over touched files when the
current issue or contract asks for it.

## CI Shape

The current GitHub Actions workflow is `.github/workflows/repo-checks.yml`.

It runs on `push` and `pull_request`, using:

- `windows-latest`
- Python `3.13`
- `py -m pip install -e .[dev]`
- `py -m pytest -q tests`
- `py tools/check_protected_surfaces.py --base origin/${{ github.base_ref }}`
  on pull requests
- `py -m ruff check src tests tools`

CI does not currently run Pyright as a required failing gate. CI also does not
install the deferred optional groups from stale PR #65 because those groups do
not exist in the active `pyproject.toml`.

## Advisory Pyright Posture

Pyright is active as an advisory type-checking tool.

Current posture:

- `pyright` is included in the `dev` optional dependency group.
- `pyrightconfig.json` includes `src` and `tests`.
- `pyrightconfig.json` uses `typeCheckingMode = "basic"`.
- Zero Pyright findings is not required.
- Pyright is not a required/failing CI gate.
- Pyright output should be reviewed through the normalized advisory helper when
  possible.

Preferred report command:

```powershell
py tools\run_pyright_advisory_report.py
```

The Windows shortcut also exists:

```powershell
powershell -ExecutionPolicy Bypass -File tools\run_pyright_advisory.ps1
```

That shortcut runs raw Pyright and can throw when Pyright reports findings. For
workflow handoffs and reviews, prefer `tools/run_pyright_advisory_report.py`
because it separates type findings, local resolver noise, and tooling/config
blockers.

## Deferred Tooling Candidates

Stale PR #65 named several extra optional dependency groups that are not active
in the current `pyproject.toml`: `codex`, `hardening`, `docs`, `typing`,
`packaging`, and `security`.

Those names should be treated as non-authoritative historical source material.
Do not use install commands such as:

```powershell
py -m pip install -e ".[dev,codex,hardening,docs,typing,packaging,security]"
```

unless a future issue updates `pyproject.toml` to define those groups.

Deferred candidates for future issues:

| Candidate | Why it is deferred |
| --- | --- |
| `pre-commit` | Useful only after the repo adopts committed hook configuration. |
| `tox` or `nox` | Useful when the project needs repeatable multi-environment test sessions. |
| `pytest-xdist` | Useful if the test suite becomes slow enough to need parallel execution. |
| `mypy` | Redundant while the repo standard is advisory Pyright. |
| `types-requests` and `types-beautifulsoup4` | May reduce type noise later, but are not active dependency metadata today. |
| `PyYAML` | Only needed if future tooling parses YAML outside the standard library and current dependencies. |
| `hypothesis` | Useful for property testing, but not active dependency metadata today. |
| `reportlab` | Useful for PDF generation workflows, but not active dependency metadata today. |
| `build` | Useful for package artifact checks, but not active dependency metadata today. |
| `pip-audit` | Useful for dependency vulnerability audits, but not active dependency metadata today. |
| failing Pyright gate | Deferred because Pyright is currently advisory and zero findings is not required. |
| additional CI gates | Deferred until a scoped issue or contract authorizes gate changes. |

## Maintenance Notes

- Keep this guide aligned with `pyproject.toml`, `pyrightconfig.json`,
  `.github/workflows/repo-checks.yml`, and repo-local tools.
- Keep install commands limited to optional dependency groups that actually
  exist.
- Do not document one-off local packages as required project setup.
- Do not commit virtual environments, package caches, generated reports,
  SQLite database files, raw logs, failed posts, runtime status files, workbook
  exports, credentials, webhook URLs, or machine-local artifacts.
