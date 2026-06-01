# Validation Matrix

Status: non-authoritative selector-backed reference.

Executable changed-path validation authority remains
`tools/select_validation.py`. Local bundle planning and execution authority
remains `tools/run_hardening_orchestrator.py`. This document is a human and
Codex planning aid only. It is not runtime selector config, CI config, merge
readiness, deploy readiness, tracker completion, or protected-surface
authorization.

When in doubt, run:

```bash
python3 tools/select_validation.py --base <git-ref>
```

For explicit path-scoped review:

```bash
printf '%s\n' <repo-relative-paths> | python3 tools/select_validation.py --base <git-ref> --paths-from-stdin
```

## Priority Vocabulary

| priority | meaning |
| --- | --- |
| `required` | Directly relevant checks that should run for the changed surface before review unless skipped with a documented reason. |
| `recommended` | Adjacent or broader checks that improve confidence when coupling, protected warnings, or unmapped paths increase risk. |
| `advisory` | Diagnostic checks that may report findings without becoming blocking by themselves. |

Pyright is advisory in this repo unless a later issue and contract explicitly
change that policy.

## Selector-Backed Matrix

| internal project area | path family examples | expected required checks | expected recommended checks | expected advisory checks | notes |
| --- | --- | --- | --- | --- | --- |
| Parser | `src/mythic_edge_parser/events.py`, `src/mythic_edge_parser/router.py`, `src/mythic_edge_parser/parsers/**`, parser-owned `src/mythic_edge_parser/app/*.py`, parser fixtures | focused parser tests, Ruff for Python changes, protected-surface gate, secret/private-marker scan, `git diff --check` | full pytest when protected parser categories overlap or a source path lacks a focused mapping | Pyright advisory for source changes | Parser and state remain truth owners for match/game facts. |
| Corpus / Provenance | evidence-ledger modules, diagnostics, drift, golden replay, feature-equity, sanitized fixtures, evidence reports | focused evidence, diagnostics, drift, replay, fixture, or schema snapshot tests where mapped; safety scans; `git diff --check` | broader replay or diagnostics checks when coupling is unclear | Pyright advisory for source changes | No raw private Player.log excerpts or local diagnostics artifacts. |
| Analytics | analytics migration loader, `analytics_migrations/**`, ingest modules, legacy JSONL adapter, derived SQL views, analytics tests | focused analytics migration/schema/ingest/view/import tests; Ruff for Python changes; safety scans; `git diff --check` | generated SQLite artifact scan when analytics implementation or tests change | Pyright advisory for source changes | Analytics consumes parser-normalized facts; it does not reinterpret raw logs or own parser truth. |
| Local App / UI | `src/mythic_edge_parser/local_app/**`, `tools/dev_app/**`, `frontend/**` | local app backend/config/import/history tests for Python surfaces; launcher tests for dev-app tools; frontend typecheck/test/build for frontend source | generated/private artifact scan when local app or frontend tests may create local outputs | Pyright advisory for Python source changes | Local app and UI orchestrate local workflows; they do not own parser or analytics truth. |
| Workbook / Transport | sheet schema, sheet exports, outputs, transforms, Apps Script | sheet/export/output/schema snapshot tests; safety scans; `git diff --check` | Apps Script parity or broader tests when transport surfaces overlap | Pyright advisory for source changes | Workbook, webhook, and Apps Script changes require explicit contract authority. |
| Quality / Governance | `AGENTS.md`, agent docs, ADRs, templates, selector, hardening tools, orchestrator, validation matrix docs | focused tool tests, agent-docs checker for governance docs, Ruff for Python tools, safety scans, `git diff --check` | orchestrator tests when selector/orchestrator interaction changes | Pyright advisory for Python tooling | Validation tools report evidence; they do not decide merge, deploy, or tracker completion. |
| Generated / Local Artifacts | `docs/local_artifacts_manifest.json`, `tools/check_local_environment.py`, repo-local `data/**`, `.env*`, SQLite sidecars, frontend build output | local environment checker tests, protected-surface gate, secret/private-marker scan, `git diff --check` | clean-clone and clean-install transition reports when artifact policy changes | N/A unless source tooling changes | Do not commit private/generated/local artifacts. CT-227-001 remains adjacent scanner coverage debt. |
| Future AI Integration | future AI/advisor docs only unless separately contracted | docs/governance checks and safety scans for docs-only boundary work | route implementation questions back to a new issue and contract | N/A | Naming this area does not authorize model-provider calls, credentials, AI coaching, hidden-card inference, or AI-owned truth. |

## Hardening Orchestrator Relationship

Use `tools/run_hardening_orchestrator.py` when a workflow needs a local bundle
plan or run. The orchestrator may invoke the selector, but it does not read
this document and does not decide validation truth, merge readiness, deploy
readiness, issue closure, or tracker completion.

Common local planning command:

```bash
python3 tools/run_hardening_orchestrator.py --base <git-ref> --profile plan
```

Common quick local run:

```bash
python3 tools/run_hardening_orchestrator.py --base <git-ref> --profile quick --run
```

## Protected And Local Artifact Notes

For non-empty changed-path sets, the selector should recommend:

- `python3 tools/check_protected_surfaces.py --base <git-ref>`
- `python3 tools/check_secret_patterns.py --base <git-ref>`
- `git diff --check`

Protected-surface warnings should route to explicit authorization review. They
do not prove a change is safe by themselves.

Local artifact and secret-like changes should stay report-only unless a later
contract changes enforcement. Real secrets, raw logs, generated databases,
runtime status artifacts, failed posts, and workbook exports must not be
committed.
