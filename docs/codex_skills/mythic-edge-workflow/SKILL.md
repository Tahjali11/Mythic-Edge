---
name: mythic-edge-workflow
description: Use for Mythic Edge repo work involving Codex A-G workflow roles, parser audits, code hardening, GitHub issues/PRs, branch handoffs, protected surfaces, parser truth ownership, Player.log evidence, workbook/webhook boundaries, or AI analytics boundaries.
---

# Mythic Edge Workflow

## Purpose

Use this skill to orient Codex on Mythic Edge work without requiring the user to paste the full constitution every time.

The repo remains the authority. This skill is a routing and inspection guide, not a replacement for repo docs, GitHub issues, contracts, ADRs, or tests.

## First Steps

1. Resolve the repo root before reading or editing files.
   - Find the clone root by locating `AGENTS.md` and `pyproject.toml`.
   - On Windows, a common local parent is `%USERPROFILE%\Desktop\MTG Resources`.
   - On macOS or Linux, use the local clone path chosen on that machine.
2. Inspect current state before acting:
   - `git status --short --branch`
   - `git fetch --prune` when branch, issue, or PR freshness matters
   - `gh issue view ...` or `gh pr view ...` when the user references GitHub state
3. Read repo-local guidance before non-trivial work:
   - `AGENTS.md`
   - `docs/agent_rules.yml` when present on the current branch
   - `docs/agent_constitution.md`
   - `docs/codex_module_workflow.md`
   - the relevant role file in `docs/agent_threads/`
   - the relevant template in `docs/templates/`
   - accepted ADRs in `docs/decisions/` when relevant
4. If a required workflow doc is missing on the active branch, check whether it exists on `origin/main` or the intended integration branch before treating it as deleted.

## Role Routing

Use the Mythic Edge workflow roles unless the user asks for a simple direct answer.

- Codex A / Thinker: problem representation, scope, risk tier, first inspection order, GitHub issue creation. Do not implement code.
- Codex B / Module Contract Writer: create or update `docs/contracts/*.md`. Do not implement behavior changes.
- Codex C / Module Implementer: compare code to contract, make narrow implementation/test changes, write `docs/implementation_handoffs/*.md`.
- Codex D / Module Fixer: fix concrete review, test, or CI findings only.
- Codex E / Module Reviewer: review against issue, contract, handoff, diff, and tests; lead with findings.
- Codex F / Module Submitter: stage only reviewed files, commit, push, and open/update a draft PR.
- Codex G / Integration Deployer: merge/integration readiness, tracker updates, issue closure, and final branch sync after explicit user request.
- Codex H / Constitutional Lawyer: synthesize constitution feedback packets into amendment proposals and watch lists. Do not directly rewrite the constitution.

Normal path:

```text
A -> B -> C -> E -> F -> G
```

Use D only for concrete fix targets after review, contract-test, or CI evidence.

Use H only after major suites, before major governance changes, after serious workflow failures, or when the user explicitly asks for constitution feedback synthesis.

## Branch Rules

Verify branch policy from the active issue or tracker.

Common defaults:

- Parser module audit work targets `codex/parser-module-audit-suite`.
- Code hardening work targets `codex/code-hardening-suite`.
- Repo-wide hardening work targets `codex/repo-wide-hardening-run`.
- Do not target `main` unless the user explicitly approves that target.
- If an integration branch is stale relative to `main`, call out the branch-sync risk before implementation.

## Protected Surfaces

Stop or require an explicit issue/contract before changing:

- parser behavior outside approved scope
- parser state final reconciliation
- parser event classes
- match identity
- game identity
- deduplication
- workbook schema
- webhook payload shape
- Apps Script behavior
- secrets, credentials, API keys, tokens, webhook URLs, or environment variable contracts
- raw local logs
- generated card/tier data
- runtime status files
- local retry queues
- workbook exports

Treat AI analytics, workbook formulas, dashboards, webhook transport, and Apps Script as downstream consumers unless a contract explicitly changes truth ownership.

## Artifact Rules

Every non-trivial workflow thread should produce a durable artifact:

- GitHub issue for Codex A
- `docs/contracts/*.md` for Codex B
- `docs/implementation_handoffs/*.md` for Codex C or D
- `docs/contract_test_reports/*.md` or PR review for Codex E
- draft PR for Codex F
- merge/close/tracker comments for Codex G

End workflow threads with:

- role performed
- source artifact used
- artifact produced or changed
- files changed
- validation run
- remaining risk or unverified layers
- next recommended role
- pasteable next-thread prompt when useful
- `workflow_handoff` block when the workflow continues

## Validation

Use the smallest relevant check first. Common commands:

```powershell
py -m pytest -q tests\test_api_common.py
py -m pytest -q tests
py -m ruff check src tests tools
py tools\run_pyright_advisory_report.py
py tools\check_protected_surfaces.py --base origin/main
py tools\check_agent_docs.py
py tools\check_secret_patterns.py --all
py tools\select_validation.py --base origin/main
git diff --check
```

Cross-platform equivalents usually replace `py` with `python3`.

Do not claim success without command output, CI evidence, corrected output, or a verified code path.

When Pyright is advisory, record findings without requiring zero errors unless a later contract escalates it.

## GitHub Hygiene

Use GitHub issues for problem representations and draft PRs for implementation work.

Before staging or submitting:

- inspect `git status`
- identify unrelated or untracked changes
- stage only intended files
- avoid raw logs, generated data, secrets, runtime status, local retry queues, workbook exports, and local-only artifacts
- link the issue and tracker
- report target branch, validation, and remaining risk

Prefer an explicit GitHub CLI path if `gh` is installed but missing from the shell `PATH`.

## Installing Repo-Owned Skills

From the repo root:

```powershell
py tools\install_codex_skills.py --all
```

On macOS or Linux:

```bash
python3 tools/install_codex_skills.py --all
```

The installer copies repo-owned skills into `$CODEX_HOME/skills` when `CODEX_HOME` is set, otherwise into the current user's `.codex/skills` directory.
