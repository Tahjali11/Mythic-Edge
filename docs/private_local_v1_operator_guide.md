# Private Local V1 Operator Guide

This guide is the detailed private-local-v1 launch guide for Mythic Edge.

Private-local-v1 means a private Windows setup for one local operator. It is a
local app and analytics support path, not a public release, production deploy,
slim package, installer, upgrade flow, or uninstall flow.

## Quick Terms

- Parser: the Python code that interprets MTGA log events and owns
  parser-managed facts.
- SQLite: a small local database file. Mythic Edge uses it for local analytics
  storage.
- Managed full checkout: the current package mode where the installed app root
  contains a full Mythic Edge checkout under `<install_root>\app`.
- Local app: the FastAPI backend and React/Vite frontend used as the local
  operator UI.
- Match Journal: human notes, labels, and review context. It does not become
  parser truth or analytics truth.
- Player.log: MTGA's local log file. It is private local evidence and must not
  be committed.

## Current Release Profile

Current private-local-v1 metadata:

- release profile: `private_local_v1`
- package mode: `managed_full_checkout`
- default release ref: `codex/analytics-foundation`
- default install root: `%LOCALAPPDATA%\MythicEdge\`
- app checkout root: `<install_root>\app`
- generated data root: `<install_root>\data`
- backend URL: `http://127.0.0.1:8765`
- frontend URL: `http://127.0.0.1:5173`

The release ref is the branch or ref the setup helper uses for a managed app
checkout. The current default remains `codex/analytics-foundation`; this guide
does not create a release tag or release branch.

## Local Folder Layout

The private-local-v1 install root is symbolic here. Do not paste or publish
machine-specific local paths.

```text
%LOCALAPPDATA%\MythicEdge\
  app\
  data\
    config\
      install_manifest.json
    db\
      mythic_edge.sqlite3
    logs\
    imports\
    jobs\
    diagnostics\
      setup_report.json
    exports\
    ai_review\
      sources\
      packets\
      reports\
```

What each major folder means:

- `app\`: the managed full checkout used by the private-local-v1 app.
- `data\`: generated and private local app state.
- `config\`: local setup metadata such as `install_manifest.json`.
- `db\`: local SQLite databases.
- `logs\`: local app logs.
- `imports\`: local import working area.
- `jobs\`: local import job metadata.
- `diagnostics\`: local setup and readiness reports.
- `exports\`: reserved local output area.
- `ai_review\`: reserved folders only. They do not authorize OpenAI runtime,
  model-provider behavior, AI coaching, hidden-card inference, or gameplay
  advice.

## Setup Command Shapes

Run these from the repo root in Windows PowerShell.

Check readiness without creating private-local-v1 folders or databases:

```powershell
powershell -ExecutionPolicy Bypass -File tools\dev_app\setup_private_local_v1.ps1 -Check -JsonReport
```

Run a proof flow without opening the browser and stop after verification:

```powershell
powershell -ExecutionPolicy Bypass -File tools\dev_app\setup_private_local_v1.ps1 -Proof -NoOpen -StopAfterVerify -JsonReport
```

Install and initialize the local SQLite database only when you intentionally
want to create or update the private-local-v1 install root:

```powershell
powershell -ExecutionPolicy Bypass -File tools\dev_app\setup_private_local_v1.ps1 -Install -InitializeSqlite -JsonReport
```

Safety notes:

- `-Check` is the safest first command because it reports readiness.
- `-Proof` is for controlled validation and should still be treated as an app
  launch proof.
- `-Install -InitializeSqlite` can create generated local app state under the
  install root.
- This guide does not authorize deleting, moving, overwriting, cleaning,
  resetting, upgrading, or uninstalling local folders.

## Launch Shape

The local app uses loopback addresses, which means it listens on the local
machine only.

- backend host and port: `127.0.0.1:8765`
- frontend host and port: `127.0.0.1:5173`
- backend URL: `http://127.0.0.1:8765`
- frontend URL: `http://127.0.0.1:5173`

The backend is a FastAPI app. FastAPI is a Python web framework used here to
serve local status, analytics, import, and Match Journal endpoints.

The frontend is a React/Vite app. React builds the browser UI, and Vite is the
local frontend development/build tool.

## Local Analytics And SQLite

SQLite stores parser-normalized analytics facts locally. It does not parse raw
Player.log data, replace the parser, or override parser-managed facts.

The current symbolic database path is:

```text
<install_root>\data\db\mythic_edge.sqlite3
```

SQLite can support match history, game history, opening hand views, mulligan
views, play/draw and postboard splits, gameplay-action review, opponent-card
observation review, import quality, and related confidence or drift warnings.

Do not store raw Player.log payloads or raw saved-event lines in SQLite.

## Manual JSONL Import

Manual JSONL import is the local historical import path. It lets the operator
choose approved local JSONL input and import parser-normalized facts into the
local analytics database.

Important boundary:

- local JSONL input is private local evidence;
- import quality can report provenance, confidence, finality, drift, and
  degradation;
- legacy or imported fields must not become parser truth;
- the UI must not expose raw payloads, raw paths, raw hashes, temporary paths,
  or private artifacts.

## Live Player.log Mode

Live Player.log mode is the path for future or current live local capture
surfaces. It must preserve parser truth ownership.

Expected boundary:

- MTGA emits Player.log evidence;
- parser/state interprets that evidence;
- parser-owned facts may be captured into SQLite;
- diagnostics can report watcher status, truncation, rotation, duplication, or
  degraded evidence.

Live mode must not store raw Player.log payloads in SQLite, and docs must not
turn watcher status into production readiness.

## Analytics Views

Curated analytics views are product surfaces over local SQLite facts. They are
not arbitrary SQL consoles and are not truth owners.

Current and intended review areas include:

- match and game history
- opening hands and mulligans
- play/draw and postboard splits
- early turns and gameplay actions
- opponent-card observations
- import quality and evidence warnings

Analytics may summarize and compare parser-produced facts. It must not
reinterpret raw Player.log data, invent match or game identity, or override
parser final reconciliation.

## Match Journal

Match Journal owns human review context:

- matchup labels
- archetype labels
- match notes
- game notes
- sideboarding notes
- review flags
- experiment labels
- display-only correction proposals

Those entries are useful for review, but they do not become parser truth,
analytics truth, workbook truth, hidden-card truth, AI truth, gameplay advice,
or best-line truth.

## Google Sheets And Workbook Surfaces

Google Sheets, webhook posting, and Apps Script remain downstream or legacy
transport/display surfaces. They are not the primary private-local-v1 operator
path.

Do not use workbook formulas or Apps Script behavior to repair parser-managed
facts. Fix parser-owned facts upstream under a scoped contract.

## Privacy And Never-Commit Rules

Keep generated and private local artifacts out of the repo.

Do not commit:

- MTGA log files
- private JSONL import artifacts
- generated SQLite databases or sidecar files
- local app logs or job state
- workbook exports
- real `.env*` files
- credentials or tokens
- generated app-data files
- machine-local paths or private payload examples

The repo-root `.env.example` file is a blank template. Real environment files
are local only.

## Safe Troubleshooting

Start with report-only checks and symbolic paths.

Good first checks:

```powershell
git status --short --branch --untracked-files=all
powershell -ExecutionPolicy Bypass -File tools\dev_app\setup_private_local_v1.ps1 -Check -JsonReport
```

When reporting an issue, prefer:

- command shape
- symbolic install path such as `<install_root>\data`
- setup status codes
- validation command result
- screenshots that do not reveal private payloads

Avoid:

- raw local paths
- raw Player.log excerpts
- raw JSONL lines
- database contents
- stack traces containing private paths or values
- secrets, credentials, webhook URLs, provider keys, or environment values

## Explicit Non-Claims

Private-local-v1 currently does not claim:

- public release readiness
- production readiness
- a v1.0 tag
- a release branch
- slim-package readiness
- installer readiness
- upgrade tooling
- uninstall tooling
- destructive cleanup tooling
- all-repo scanner cleanliness
- Pyright as a required failing gate
- live workbook readiness
- deployed Apps Script readiness
- Google Sheets sync readiness for this local-app path
- OpenAI/model-provider runtime integration
- AI coaching or strategic certainty
- hidden-card inference
- archetype truth
- player-mistake truth
- gameplay advice
- best-line truth
- Line Tracer truth

Each of those needs separate issue and contract authority before it can become
operator guidance.
