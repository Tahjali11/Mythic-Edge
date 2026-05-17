# Mythic Edge Analytics Suite Roadmap

This document preserves the long-range module map for the eventual Mythic Edge
analytics suite.

It is intentionally future-facing. The current project order remains:

1. Parser module audit suite.
2. Code hardening and repo-wide hardening.
3. Player.log evidence ledger / drift protection.
4. Local deterministic analytics.
5. AI-assisted coaching.

The analytics suite should begin only after the parser layer, hardening layers,
and Player.log drift/evidence work are stable enough that analytics can consume
parser-managed facts with source, confidence, and finality metadata.

## Purpose

The analytics foundation is the deterministic layer between parser truth and
AI-assisted coaching.

Plain English:

- the parser says what happened
- the evidence ledger says how the project knows it
- analytics calculates patterns from those facts
- AI may later explain or propose hypotheses from analytics outputs

Analytics must consume parser truth. It must not create parser truth.

## Ownership Boundary

Analytics may own:

- aggregate metrics
- filters
- cohorts
- sample-size warnings
- trend summaries
- matchup summaries
- card-performance summaries
- sideboarding-performance summaries
- AI-coaching handoff packets

Analytics must not own:

- match result
- game result
- play/draw
- mulligan count
- opening hand facts
- card-action facts
- submitted deck facts
- parser event identity
- workbook schema
- webhook payload shape
- Apps Script behavior
- Player.log drift truth

Those facts remain owned by parser/state and evidence-ledger layers.

## Data Storage Direction

Recommended storage split:

- SQLite: canonical local analytics store.
- JSON or JSONL: transparent reports, fixtures, snapshots, and AI handoff
  packets.
- Parquet: optional future batch export format for larger analytical datasets.
- Google Sheets: collaboration, display, annotation, and review layer only.

The first serious analytics implementation should prefer SQLite for durable
local state and JSON/Markdown for inspectable report output.

## Suite Structure

The full analytics suite can be understood as 26 logical modules. These do not
all need to become separate Python packages immediately, but they should be
considered separate responsibilities.

### A. Foundation Modules

#### 1. Analytics Input Contract

Defines what analytics may read from parser outputs, evidence-ledger metadata,
fixtures, and human annotations.

Key questions:

- Which parser-managed rows and JSON artifacts are valid inputs?
- Which fields are required?
- Which confidence and finality labels are required before a metric can be
  clean?
- Which inputs are excluded by default?

#### 2. Analytics Data Models

Defines typed shapes for analytics-owned concepts.

Likely concepts:

- match fact input
- game fact input
- card observation
- opening hand observation
- deck version
- matchup label
- metric result
- sample-size warning
- analytics report

#### 3. Local Analytics Store

Provides durable local storage for analytics inputs, normalized dimensions,
derived metrics, and rebuild metadata.

Recommended first implementation:

- SQLite database under an ignored local data path.
- Schema migrations managed deliberately.
- No committed personal gameplay database.

#### 4. Ingestion Pipeline

Loads parser outputs and evidence metadata into analytics tables.

Required behavior:

- preserve parser-owned values without rewriting them
- attach confidence/provenance metadata
- avoid duplicate match/game ingestion
- allow rebuilds from saved parser artifacts

#### 5. Data Quality And Provenance Filter

Applies value-source, confidence, finality, drift, and conflict rules before
analytics are calculated.

Core responsibility:

- prevent inferred, unknown, conflicted, or degraded facts from silently
  appearing as clean analytics truth

#### 6. Sample Size Policy

Centralizes thresholds for reporting strength.

Possible labels:

- too small
- exploratory
- directional
- decision-grade
- stale
- mixed confidence

The exact thresholds should be contract-defined before metrics claim practical
strategic value.

#### 7. Metric Registry

Catalogs analytics metrics and their requirements.

Each metric should define:

- metric ID
- input fields
- required confidence level
- filters applied
- output shape
- sample-size policy
- caveat policy
- validation tests

#### 8. Analytics Report Schema

Defines the common output shape for analytics reports.

Every report should include:

- report ID
- generated timestamp
- source parser/evidence snapshot
- filters
- sample size
- confidence/caveat summary
- metric results
- excluded data counts
- follow-up questions

#### 9. Analytics Snapshot Tests

Protect expected metric outputs from accidental behavior changes.

These should use sanitized or synthetic fixtures and should not commit private
gameplay logs.

#### 10. Analytics Replay Harness

Rebuilds analytics from known fixture inputs or saved parser outputs.

Purpose:

- prove that analytics are reproducible
- detect accidental metric drift
- support future backfills

### B. Core Performance Modules

#### 11. Matchup Performance

Calculates match and game performance by matchup, archetype label, deck label,
queue, format, rank, and time window.

This should be the first user-useful analytics module.

#### 12. Game 1 Versus Post-Board Performance

Separates pre-board and sideboarded games.

This is central to sideboarding lessons and tournament preparation.

#### 13. Play/Draw Performance

Calculates play/draw splits overall and by matchup, queue, format, and deck
version.

#### 14. Mulligan Outcomes

Calculates performance by mulligan count, matchup, play/draw, game number, and
deck version.

#### 15. Opening Hand Analytics

Analyzes opening hand size, exact-card availability when known, unresolved-card
status, and keep/mulligan outcomes.

Opening-hand metrics must be confidence-aware because unresolved cards can
make card-level conclusions misleading.

#### 16. Card Performance

Calculates card-level metrics such as seen, opened, cast, mulliganed away, and
post-board performance.

Card metrics should carry sample-size warnings and should distinguish
correlation from recommendation.

#### 17. Sideboarding Effectiveness

Measures post-board improvement, sideboarding lifecycle evidence, submitted
deck changes when available, package-level effects, and matchup-specific
deltas.

This module should not fabricate exact sideboard deltas from later gameplay
actions alone.

#### 18. Deck Version Comparison

Compares deck shells, deck versions, card swaps, sideboard plans, and test
periods over time.

This is the main bridge between experimentation and measured improvement.

#### 19. Queue, Rank, And Format Context

Prevents misleading mixes of ranked ladder, unranked testing, events, Limited,
and special queues.

This module owns analytics grouping and filtering only. It does not own parser
queue truth.

#### 20. Trend Over Time

Calculates rolling windows and time-based trends.

Useful windows may include:

- last 10 matches
- last 50 games
- current week
- current deck version
- post-change period

### C. Higher-Level Interpretation Modules

#### 21. Leak Detection

Finds recurring underperformance patterns.

Examples:

- poor on-the-draw performance against low-curve decks
- post-board decline in a specific matchup
- losses after mulliganing to six
- repeated weakness in a deck version

#### 22. Pressure Point Analysis

Identifies where a matchup appears to be decided.

Potential pressure points:

- early turns
- mulligan pressure
- post-board games
- key card packages
- play/draw sensitivity
- opening hand patterns

This module should produce hypotheses, not final strategic truth.

#### 23. Card Inclusion And Exclusion Comparator

Compares candidate cards or packages across controlled filters.

Required caveat:

- card inclusion results are observational unless backed by careful experiment
  design

#### 24. Sideboard Plan Evaluation

Tracks whether sideboarded games improved after known sideboarding choices.

This module should support, but not replace, human sideboard-guide judgment.

#### 25. Human Annotation Layer

Stores user-owned review labels.

Examples:

- pilot error
- bad keep
- missed lethal
- sideboard uncertainty
- opponent misplay
- matchup label correction
- needs review

These annotations may enrich analytics, but they must not overwrite
parser-managed facts.

#### 26. AI Coaching Handoff Builder

Builds structured packets for future AI-assisted coaching.

The packet should include:

- relevant metrics
- source filters
- sample size
- confidence/caveat labels
- excluded data counts
- human annotations
- specific questions for the coach to reason about

AI output remains inference, enrichment, explanation, or recommendation. It
does not own parser truth or deterministic analytics calculations.

## Recommended First Build Slice

The first analytics foundation suite should implement only the pieces needed to
make the project useful without overbuilding.

Recommended first 10 modules:

1. Analytics Input Contract.
2. Analytics Data Models.
3. Local Analytics Store.
4. Ingestion Pipeline.
5. Data Quality And Provenance Filter.
6. Sample Size Policy.
7. Metric Registry.
8. Analytics Report Schema.
9. Matchup Performance.
10. Game 1 Versus Post-Board Performance.

Recommended second wave:

1. Play/Draw Performance.
2. Mulligan Outcomes.
3. Opening Hand Analytics.
4. Card Performance.
5. Sideboarding Effectiveness.
6. Deck Version Comparison.

Recommended later wave:

1. Queue, Rank, And Format Context.
2. Trend Over Time.
3. Leak Detection.
4. Pressure Point Analysis.
5. Card Inclusion And Exclusion Comparator.
6. Sideboard Plan Evaluation.
7. Human Annotation Layer.
8. AI Coaching Handoff Builder.

## Initial Contract Candidates

Future Codex workflow should probably start with these issues:

1. `[analytics] Analytics foundation problem representation`
2. `[analytics] Analytics input and output contract`
3. `[analytics] Local analytics store contract`
4. `[analytics] Sample size and confidence policy`
5. `[analytics] Matchup performance first pass`
6. `[analytics] Game 1 versus post-board performance first pass`

## Validation Direction

Early analytics validation should prove:

- parser-owned facts are read but not rewritten
- low-confidence facts are excluded or labeled according to policy
- sample-size warnings appear when required
- deterministic metrics reproduce expected values from fixtures
- analytics reports include caveats and excluded-data counts
- no workbook schema or webhook payload shape changes occur
- no raw logs, local gameplay databases, secrets, runtime status files, failed
  posts, generated data, or workbook exports are committed

## Non-Goals

This roadmap does not:

- implement analytics modules
- choose final database schema
- add OpenAI API integration
- create a coaching feature
- change parser behavior
- change parser state final reconciliation
- change workbook schema
- change webhook payload shape
- change Apps Script behavior
- commit personal gameplay history

## Guiding Principle

Centralize boring rules before building exciting analyses.

If sample-size policy, confidence labels, report shapes, deck versions, and
provenance rules are shared from the beginning, every later metric becomes
easier to trust.
