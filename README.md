# Mythic Edge

Mythic Edge is a private local MTG Arena analytics and review app.

It turns Arena log evidence into parser-normalized match, game, card, and
review data that can be explored locally. The current private-local-v1 path is
local-app-first: a Windows local app, a local SQLite database, manual historical
JSONL import, live Player.log readiness, curated analytics views, and Match
Journal review notes.

For the detailed private-local-v1 setup and launch path, start here:

- [Private Local V1 Operator Guide](docs/private_local_v1_operator_guide.md)

## Current Shape

```text
MTGA Player.log or approved local import input
  -> parser and parser-normalized facts
  -> local SQLite analytics storage
  -> local app backend and frontend
  -> analytics views and Match Journal review surfaces
```

Important terms:

- Parser: the Python code that interprets MTGA log events.
- Parser-normalized facts: match, game, card, and evidence values after the
  parser/state layer has shaped them into project data models.
- SQLite: a small local database file used here for local analytics storage.
- Local app: the private Windows backend and browser UI used as the
  private-local-v1 front door.
- Match Journal: human notes, labels, and review context attached to matches or
  games.

## Truth Boundaries

The parser/state layer owns parser-managed facts such as match identity, game
identity, deduplication, game result, play/draw, mulligans, opening hand data,
gameplay actions, and final reconciliation.

SQLite, analytics views, the local app, Match Journal, workbook surfaces, and
future AI surfaces are downstream or supporting layers. They may store,
display, summarize, label, or review parser-produced facts, but they do not
become parser truth.

## Private-Local-V1 Path

Private-local-v1 is the current private Windows operator path. It is not a
public release, not production readiness, not a slim package, and not an
installer.

Current private-local-v1 setup facts:

- package mode: `managed_full_checkout`
- default release ref: `codex/analytics-foundation`
- default install root: `%LOCALAPPDATA%\MythicEdge\`
- managed app checkout: `<install_root>\app`
- generated local data root: `<install_root>\data`
- local analytics database: `<install_root>\data\db\mythic_edge.sqlite3`
- frontend URL: `http://127.0.0.1:5173`
- backend URL: `http://127.0.0.1:8765`

Use the operator guide for command details and safety boundaries before running
install or proof commands.

## Local App Surfaces

The private local app is the intended front door for this phase.

It currently covers or supports:

- setup and readiness status
- manual historical JSONL import
- import-quality reporting
- SQLite-backed match and game history
- opening hand, mulligan, play/draw, postboard, gameplay-action, and
  opponent-observation views
- Match Journal cockpit and write controls
- live Player.log watcher status and diagnostics readiness

These surfaces are local development and private-operator support. They do not
change parser behavior, workbook behavior, Google Sheets behavior, AI behavior,
or production behavior.

## Google Sheets And Legacy Transport

Google Sheets, the webhook receiver, and Apps Script remain downstream or
legacy transport/display surfaces. They are still important to the broader
project history, but they are not the primary private-local-v1 operator path.

Workbook and Apps Script behavior should only change under a scoped contract.
Workbook formulas must not replace parser-owned truth.

## Local Data And Privacy

Generated and private local data must stay local unless a later scoped contract
explicitly authorizes otherwise.

Do not commit local databases, MTGA log files, imported JSONL artifacts, runtime
logs, workbook exports, credentials, environment files, or other machine-local
operator artifacts.

The repo keeps a blank `.env.example` template. Real `.env*` files are local
only.

## Development

Contributor and Codex workflow instructions live in:

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/`

For Python development:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -e ".[dev,app]"
py -m pytest
py -m ruff check src tests tools
```

For frontend development:

```powershell
npm --prefix frontend ci
npm --prefix frontend run typecheck
npm --prefix frontend run build
```

For repo validation helpers:

```powershell
.\tools\run_repo_checks.ps1
.\tools\run_touched_file_checks.ps1 <path-to-python-file>
```

Use the smallest relevant validation command first, then expand only when the
scope requires it.

## Current Non-Claims

Mythic Edge does not currently claim:

- public release readiness
- production readiness
- a v1.0 tag or release branch
- a slim package or standalone installer
- upgrade or uninstall tooling
- all-repo scanner cleanliness
- Pyright as a required failing gate
- live workbook or deployed Apps Script readiness
- OpenAI/model-provider runtime integration
- AI coaching, hidden-card inference, gameplay advice, or best-line truth

Those are future scopes and require separate contract authority.
