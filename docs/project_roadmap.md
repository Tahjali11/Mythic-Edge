# Mythic Edge Project Roadmap

This document is the durable answer source for the question: "What is the next
step?"

Use it with current repo, issue, branch, and PR state. If this roadmap conflicts
with an active issue, accepted contract, or explicit user instruction, follow
the current artifact and record the conflict.

## Current Strategic Goal

Make Mythic Edge locally usable: import real historical games, store them safely,
and view useful analytics without relying on Google Sheets.

Mythic Edge remains a personal MTG Arena data pipeline. Its core value is
turning MTGA outputs into reliable, reviewable match data that helps improve
play.

## Completed Foundation

The following project layers are treated as established foundations for the next
phase. Fresh threads should still verify current branch, issue, PR, and CI state
before acting.

1. Parser reliability and feature parity foundation
   - Parser modules, parser contracts, Manasight feature-equity checks, draft
     parser support, diagnostics, golden replay, and parser regression coverage.

2. Code and repo hardening foundation
   - Protected-surface checks, secret/private-marker scanning, schema snapshots,
     validation selectors, advisory Pyright reporting, and hardening reports.

3. Player.log evidence ledger and drift protection foundation
   - Provenance, confidence, finality, drift, degradation, evidence tiers,
     runtime status exposure, schema snapshots, and validation wiring.

4. Local analytics data foundation
   - SQLite schema, migration loading, parser-normalized replay ingest,
     gameplay-action ingest, opponent-card-observation ingest, field-evidence
     ingest, deterministic views, replay/view validation, and legacy JSONL
     adapter work.

These foundations do not make analytics, Google Sheets, UI state, or AI output
the owner of parser truth.

## Roadmap Order

### 1. Local Developer App Foundation

Goal: make Mythic Edge usable without navigating through repo folders or
hand-running Python commands.

Planned slices:

- backend setup/status skeleton
- React/Vite setup/status page
- Windows developer bootstrapper or launcher
- app-owned generated folder under `%LOCALAPPDATA%\MythicEdgeDev\`
- safe config and diagnostics views

Boundary:

- the app is an access and orchestration surface, not parser truth, analytics
  truth, workbook truth, AI truth, or deploy readiness
- no destructive UI actions in the first version

### 2. Manual Historical Import Loop

Goal: make previously saved local JSONL artifacts usable through the local app.

The first useful loop should let the user:

- select a local legacy JSONL artifact
- run the read-only adapter/import path
- ingest parser-normalized facts into SQLite
- see import quality and provenance warnings
- avoid committing raw logs, private JSONL artifacts, or generated SQLite files

Manual import should come before live Player.log writes because fixed files are
easier to validate than actively written logs.

### 3. Curated Analytics Views

Goal: make stored analytics facts visible and useful.

Initial read-only views:

- match history
- game history
- opening hands
- mulligans
- play/draw splits
- first turns and gameplay actions
- opponent-card observations
- import quality, confidence, finality, and drift warnings

These views should be curated product surfaces, not generic database browsing.

### 4. Match Journal And Cockpit Unification

Goal: bring human notes and review labels into the same local product surface
without blurring truth ownership.

The Match Journal should own:

- matchup and archetype labels
- match notes
- game notes
- sideboarding notes
- review flags
- experiment labels
- display-only correction proposals

Parser/state still owns parser-managed match/game/card facts. Analytics may join
against journal labels later, but journal entries do not become parser truth.

### 5. Live Player.log Mode

Goal: move from manual historical import to live local capture only after the
manual path is proven.

Recommended sequence:

1. live watcher status page
2. live watcher process-control safeguards
3. live parser-owned fact writes to SQLite
4. diagnostics for log truncation, rotation, duplication, and degraded evidence

Live mode must preserve parser truth ownership and must not store raw Player.log
payloads in SQLite.

### 6. Analytics Intelligence Layer

Goal: turn stable local facts into deterministic, non-AI analysis.

Candidate modules:

- opening-hand performance
- mulligan outcomes
- first-three-turn line analysis
- play/draw and game 1/post-board splits
- matchup and archetype splits
- sideboarding effectiveness
- card performance by context
- sample-size and confidence warnings

Line Tracer belongs in this phase after opening-hand, mulligan, and gameplay
action facts are visible and trusted.

### 7. Polish And Professional Discipline

Goal: make the project easier to install, run, trust, and hand to another
developer.

Candidate work:

- one-command local setup and validation
- Python and dependency lock/version policy
- Windows installer/bootstrapper polish
- later macOS setup analog
- CI and security scan maturity
- type-discipline improvement ladder
- corpus parity and corpus expansion roadmap
- repo organization cleanup
- onboarding documentation
- engineering maturity index
- release/versioning policy

This phase should improve maintainability and reliability without refactoring for
style alone or changing protected behavior without a scoped issue and contract.

### 8. AI-Assisted Coaching Layer

Goal: use AI to summarize, compare, explain, and propose hypotheses from
parser-produced facts, deterministic analytics, confidence labels, and curated
strategy context.

AI may:

- summarize trends
- explain deterministic analytics
- propose hypotheses
- draft matchup notes or sideboard-guide text for human review

AI must not own truth for:

- match result
- game result
- play/draw
- mulligan count
- opening hand
- card actions
- deck submission
- workbook schema
- parser-managed fields
- gameplay correctness
- hidden-card inference

## How To Answer "What's The Next Step?"

1. Inspect current state:
   - `git status --short --branch`
   - active tracker issues and PRs
   - current integration or staging branch health
   - current contracts, handoffs, and review reports

2. Find the earliest unfinished roadmap phase.

3. Recommend the next workflow role:
   - Use Codex G if the phase is implemented but not integrated.
   - Use Codex A if the next phase needs a new problem representation or
     tracker.
   - Use Codex B if a problem representation exists but there is no contract.
   - Use Codex C/D/E/F according to the normal module workflow when
     implementation is already scoped.

4. Preserve truth ownership:
   - Parser/state owns event interpretation and normalized match/game facts.
   - Evidence ledger owns evidence, provenance, confidence, finality, and drift
     diagnostics.
   - Analytics reads downstream facts and provenance.
   - Match Journal owns human notes and labels.
   - Local app/UI surfaces orchestrate and display; they do not own truth.
   - AI coaching reads analytics and curated context, but remains inference and
     recommendation only.

## Current Strategic Recommendation

After the Player.log evidence ledger / drift protection suite is complete and integrated, prioritize the local
analytics foundation before building AI-assisted coaching or UI-heavy product layers.

Reason: analytics and coaching become useful only when normalized parser facts, provenance labels, and replayable
history can be queried consistently. The local analytics foundation should turn parser-normalized outputs into durable
SQLite facts and deterministic views without making analytics, Google Sheets, or AI the owner of parser truth.

Expected next tracker:

```text
Local Analytics Foundation
```

Expected first child issue:

```text
Codex A: Problem representation for local gameplay fact warehouse foundation
```

Current problem representation:

```text
docs/problem_representations/local_analytics_foundation.md
```

## Operational Note

Branch cleanup, local worktree reconciliation, and issue/PR lifecycle hygiene
are required before handoff or integration, but they are operational
prerequisites rather than roadmap phases.
