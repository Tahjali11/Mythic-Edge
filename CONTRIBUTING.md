# Contributing To Mythic Edge

Use `docs/codex_module_workflow.md` for module-sized changes.

## Pre-Commit Checklist

Run the smallest relevant check first, then the broader repo check before opening a pull request.

```powershell
py -m pytest -q tests
py -m ruff check src tests
```

Repo-level helper:

```powershell
.\tools\run_repo_checks.ps1
```

Coverage helper:

```powershell
.\tools\run_repo_checks.ps1 -Coverage
```

## Testing Policy

Add or update tests when changing parser behavior, shared state, event interpretation, webhook row shape, workbook-facing payloads, or runtime diagnostics.

Prefer representative MTGA logs, parser payloads, or fixture rows over toy examples.

Configuration-only changes may be verified with targeted import, lint, or workflow checks when no runtime behavior changes.

## Pull Request Policy

Every module-sized pull request should link:

- the problem issue
- the module contract
- the validation evidence
- any known repo, workbook, or deployment drift

