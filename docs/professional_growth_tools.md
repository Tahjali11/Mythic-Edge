# Professional Growth Tools

This note tracks the live Google Sheet sections that were added to support
competitive improvement work.

The dashboard now includes five coaching-oriented tools in a lower block of
the `Dashboard` sheet.

## Sheet Layout

- `Dashboard!A210:K272`
  The current home for the five tools.

## Tools

### 1. Matchup Prep Report

- Purpose:
  Show the matchup-facing numbers that matter most before a session.
- Main signals:
  - match win rate
  - game 1 win rate
  - postboard game win rate
  - on-play and on-draw game win rate
  - average mulligans
  - pilot error rate
- Data source:
  - `Match Log`
  - `Game Log`

### 2. Mulligan Review Tool

- Purpose:
  Show whether mulligans are costing percentage points overall and by matchup.
- Main signals:
  - win rate by mulligan band
  - matchup-level average mulligans
  - seven-card keep rate
  - game win rate by matchup after mulligan pressure
- Data source:
  - `Game Log`

### 3. Sideboarding Notebook

- Purpose:
  Summarize postboard performance in a way that supports sideboard planning,
  even before exact in/out card tracking exists.
- Main signals:
  - postboard games by matchup
  - postboard win rate
  - game 3 frequency and win rate
  - average postboard mulligans
  - postboard performance by deck tier
- Data source:
  - `Game Log`

### 4. Session Quality Tracker

- Purpose:
  Give a first-pass view of performance over time.
- Current limitation:
  - this uses play date as a session proxy
  - it is not yet a true session model because the sheet does not currently
    store full match start/end timestamps as visible columns
- Main signals:
  - match count by day
  - games by day
  - daily match win rate
  - daily game win rate
  - daily pilot error rate
  - weekday pattern
- Data source:
  - `Match Log`

### 5. Opening Hand Analyzer

- Purpose:
  Provide the bridge from opening-hand capture to card-level win-rate study.
- Current status:
  - opening-hand size analytics are live now
  - card-level opener analytics are wired, but they only become useful once
    `Game Log -> Opening Hand` begins filling with resolved card names
- Main signals:
  - win rate by opening hand size
  - card-level opener counts
  - card-level opener wins
  - card-level opener win rate
  - optional opponent-archetype filter
- Data source:
  - `Game Log`

## Future Upgrade Path

The next parser-facing upgrades that would make these tools substantially
stronger are:

1. `Opening Hand` card names on more rows
2. `Mulliganed Away` card tracking
3. visible match start/end timestamps in the workbook
4. exact sideboard change tracking
