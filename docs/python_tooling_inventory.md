# Python Tooling Inventory

This document lists the Python packages that are useful for working on Mythic Edge locally. It is an environment
inventory, not a lock file. The authoritative machine-readable dependency configuration is `pyproject.toml`.

## Serious Codex Setup Commands

These commands install Mythic Edge in editable mode with the optional tool groups used for development, Codex
workflow, code hardening, documentation, type checking, packaging, and dependency audits.

Run them from the repo root when setting up or refreshing a local machine.

### Windows PowerShell

```powershell
cd "$HOME\Desktop\MTG Resources\MythicEdge"
py -m pip install -e ".[dev,codex,hardening,docs,typing,packaging,security]"
```

### macOS Terminal

Use the path where the repo is cloned on the Mac:

```bash
cd "/path/to/MythicEdge"
python3 -m pip install -e ".[dev,codex,hardening,docs,typing,packaging,security]"
```

For the cleanest Mac setup, use a virtual environment first:

```bash
cd "/path/to/MythicEdge"
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev,codex,hardening,docs,typing,packaging,security]"
```

### Repo-Root Install Command

When already inside the repo root, the install command is:

```powershell
py -m pip install -e ".[dev,codex,hardening,docs,typing,packaging,security]"
```

## Required Runtime Packages

These are needed by the parser or runtime support code.

| Import / tool | PyPI package | Current source | Purpose |
| --- | --- | --- | --- |
| `bs4` | `beautifulsoup4` | `pyproject.toml` runtime dependency | HTML parsing for tier/metagame sync helpers. |
| `requests` | `requests` | `pyproject.toml` runtime dependency | HTTP calls for webhook posting, card catalog refresh, tier sync, and backfill helpers. |

## Required Development And Validation Packages

These support the standard local validation path.

| Tool | PyPI package | Current source | Purpose |
| --- | --- | --- | --- |
| `pytest` | `pytest` | `pyproject.toml` dev dependency | Test runner for focused and full test suites. |
| coverage via pytest | `pytest-cov` | `pyproject.toml` dev dependency | Coverage reporting when coverage-sensitive checks are needed. |
| `ruff` | `ruff` | `pyproject.toml` dev dependency | Linting and import-order checks. |
| `pyright` | `pyright` | `pyproject.toml` dev dependency | Advisory type checking through `pyrightconfig.json`. |

## Optional Tooling Declared In `pyproject.toml`

These are useful for local Codex work, code hardening, documentation, type checking, packaging, and dependency
auditing. They are optional project tooling dependencies, not parser runtime dependencies.

| Extra group | Import / tool | PyPI package | Purpose |
| --- | --- | --- | --- |
| `codex` | `yaml` | `PyYAML` | Parses YAML files such as Codex skill metadata and `docs/agent_rules.yml`. |
| `hardening` | property tests | `hypothesis` | Property/fuzz testing for shared parser utilities such as `api_common.py`. |
| `docs` | `reportlab` | `reportlab` | Builds PDF versions of Markdown docs. |

## Type-Checking Support Packages

These packages do not change runtime behavior. They provide type information that can make Pyright output clearer.

| Extra group | Package | Purpose |
| --- | --- | --- |
| `typing` | `types-requests` | Type stubs for `requests`. |
| `typing` | `types-beautifulsoup4` | Type stubs for Beautiful Soup. |
| `typing` | `types-PyYAML` | Type stubs for PyYAML. |

## Packaging And Supply-Chain Utilities

These are useful local tools, but they are not currently required by CI.

| Extra group | Tool | PyPI package | Purpose |
| --- | --- | --- | --- |
| `packaging` | package builder | `build` | Verifies Python package metadata and builds local distributions when needed. |
| `security` | dependency audit | `pip-audit` | Checks installed or declared Python dependencies for known vulnerabilities. |

## Deferred Candidates

These may be useful later, but should not be adopted until the repo has a concrete workflow that needs them.

| Tool | Why defer |
| --- | --- |
| `pre-commit` | Useful only after the repo has committed hook configuration. |
| `tox` or `nox` | Useful when the project needs repeatable multi-environment test sessions. |
| `pytest-xdist` | Useful if the test suite becomes slow enough to need parallel execution. |
| `mypy` | Redundant while the project standard is Pyright advisory checking. |

## Notes For Future Workflow Threads

- If a package becomes required for tests or CI, keep it in `pyproject.toml` in the appropriate optional dependency
  group instead of relying on this document alone.
- If a package is only needed for a one-off local workflow, keep it documented here and avoid expanding project
  requirements.
- Do not commit local package caches, virtual environments, generated metadata, or environment-specific files.
