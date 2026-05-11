# Mythic Edge Agent Constitution

This document is the durable rulebook for Codex threads working on Mythic Edge.

Use it when a thread needs shared behavior rules that survive across machines, GitHub issues, pull requests, and local checkouts.

## Authority Order

When instructions conflict, follow this order:

1. system and developer instructions from the active Codex session
2. explicit user instructions in the current conversation
3. repository `AGENTS.md`
4. this constitution
5. role-specific files in `docs/agent_threads/`
6. workflow templates in `docs/templates/`
7. older docs, comments, and examples

If a lower-priority document appears to contradict a higher-priority one, say so plainly and follow the higher-priority instruction.

## Core Purpose

Mythic Edge is a personal MTG Arena data pipeline. Its job is to turn raw MTGA logs into reliable match, game, card, and workbook-facing facts.

Agents should optimize for:

- maintainable working code
- clear system structure
- beginner-friendly explanations
- evidence-backed fixes
- small coherent changes
- safe GitHub collaboration
- strong boundaries between truth-producing and display layers

## Project Truth Layers

Use this ownership model before changing behavior:

1. MTGA raw log source
   - source of raw events only
2. parser and state interpretation
   - source of truth for event interpretation
   - owns normalized match and game facts
3. webhook / transport layer
   - moves parser-produced rows
   - does not own truth
4. workbook landing sheets
   - receive parser-managed facts
   - should not reconstruct truth that parser can provide
5. helper formulas
   - support display and classification
   - do not own truth
6. dashboard / reporting tabs
   - display and analysis layer
   - do not own truth

If a proposed change moves truth from one layer to another, stop and call that out before implementation.

## Thread Roles

Every non-trivial Codex thread should declare one role:

- problem representation
- module contract
- implementation
- contract test
- review

If the role is unclear, infer the safest role from the request. Prefer problem representation or contract work before implementation when the behavior is ambiguous.

Thread rules live in:

- `docs/agent_threads/problem_representation.md`
- `docs/agent_threads/module_contract.md`
- `docs/agent_threads/implementation.md`
- `docs/agent_threads/contract_test.md`
- `docs/agent_threads/review.md`

## Workflow Gates

Problem representation must happen before module contract work.

Module contract work must happen before broad implementation.

Implementation must reference the contract it is satisfying.

Contract testing must compare implementation behavior against the contract, not against assumptions from the implementation thread.

Review should focus on concrete bugs, missed contract obligations, missing tests, stale references, drift, and unsafe behavior.

## GitHub Workflow

Use GitHub issues for problem representations when work is more than a tiny local fix.

Use pull requests for implementation changes.

Use these labels when applicable:

- `workflow:problem`
- `workflow:contract`
- `workflow:implementation`
- `workflow:contract-test`
- `layer:parser`
- `layer:webhook`
- `layer:workbook`
- `layer:dashboard`

Default branch names:

- `codex/problem-<short-name>`
- `codex/contract-<short-name>`
- `codex/impl-<short-name>`
- `codex/test-<short-name>`

Use private repositories unless the user explicitly says otherwise.

## Safety Rules

Never commit real secrets.

Treat these as sensitive:

- webhook URLs
- API keys
- tokens
- credentials
- local MTGA logs
- failed posts
- runtime status files
- raw workbook exports
- personal local paths when avoidable

Do not invent, rotate, overwrite, or delete credentials unless the user explicitly asks.

Do not delete local logs, archive layers, debug layers, helper tabs, workbook tabs, or generated data unless the user explicitly approves the deletion and the rollback path is clear.

## Cross-Machine Rules

The repo must work from a clean clone.

Do not depend on ignored local folders such as:

- `data/match_logs/`
- `data/runtime_logs/`
- `data/status/`
- `data/failed_posts/`
- `data/bad_events/`
- `data/oracle_data/`

If a test or tool needs generated data, it should either:

- create it in a temporary directory
- use a committed fixture
- skip with an explicit reason when the data is intentionally local-only

Local machine setup belongs in docs or `.env.example`, not in committed secrets.

## Code Change Rules

Inspect relevant files before editing.

Prefer small coherent wiring passes over half-migrations.

Keep parser truth upstream. Do not patch workbook formulas when parser logic owns the fact.

Be careful with:

- imports
- shared runtime state
- renamed functions
- stale module names
- workbook tab names
- webhook row shape
- provisional live values
- final reconciled values
- deduplication keys
- match and game identity

Do not silently expand scope. If a cleanup is useful but not required, name it before doing it.

## Validation Rules

Use the smallest relevant validation first.

Common commands:

```powershell
py -m pytest -q tests
py -m ruff check src tests
```

Repo-level command:

```powershell
.\tools\run_repo_checks.ps1
```

Coverage command:

```powershell
.\tools\run_repo_checks.ps1 -Coverage
```

For narrow Python changes:

```powershell
.\tools\run_touched_file_checks.ps1 <changed-python-file> <changed-test-file>
```

Do not say a fix worked unless there is evidence from a test, command, corrected output, or verified code path.

## Communication Rules

Explain in plain English first.

When using a technical term, define it briefly the first time unless the user already used it correctly.

Use this debugging order:

1. what the code is supposed to do
2. what it is actually doing
3. why it is failing
4. the exact fix
5. how to verify the fix worked

At handoff, say:

- what changed
- what was verified
- what is still unverified
- what the user should test next

## Drift Rules

For workbook-connected changes, always distinguish:

- repository code state
- live workbook state
- deployed Apps Script state

If they differ, label the issue:

- repo drift
- workbook drift
- deployment drift
- combined drift

Fixing one layer does not mean the whole pipeline is fixed. Say which layer is now ahead and what still needs syncing.

## AI And Analytics Boundary

OpenAI or other model-backed analytics may summarize, explain, classify, and propose hypotheses from parser-produced facts.

They must not become the source of truth for:

- match result
- game result
- play/draw
- mulligan count
- opening hand
- card action facts
- webhook row identity
- workbook schema

For AI-backed modules, send the smallest normalized payload needed. Do not send raw logs unless the task is explicitly parser debugging and the privacy tradeoff is understood.

## Done Definition

A non-trivial change is done when:

- the role artifact exists
- the implementation or recommendation references the relevant artifact
- tests or validation evidence are recorded
- secrets and local-only files are not committed
- GitHub Actions are expected to pass or any failure is explained
- remaining drift or unverified layers are named

