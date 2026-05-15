# Mythic Edge Future Enhancement Ideas

This document parks long-horizon ideas for Mythic Edge after the parser audit,
code hardening, Player.log evidence ledger, deterministic analytics, and an
initial AI-assisted coaching layer are in place.

Default framing: Mythic Edge is a personal hobby and craft project. These ideas
are about making the tool more useful, resilient, and professionally built for
personal MTG improvement. They are not a monetization roadmap.

## Revisit Trigger

Revisit this document after:

1. The code hardening suite is complete and integrated.
2. The Player.log evidence ledger / drift protection suite is implemented.
3. A deterministic local analytics foundation exists.
4. A first AI-assisted coaching workflow exists and is clearly labeled as
   inference, explanation, or recommendation.

## 1. Recommendation Ledger

Record every coaching recommendation as a durable object instead of letting AI
advice disappear into chat history.

Potential fields:

- recommendation id
- timestamp
- source match, deck, matchup, format, or experiment context
- evidence used
- analytics used
- strategy-corpus sources used
- recommendation text
- confidence label
- value-source labels for supporting facts
- whether the player accepted, rejected, or deferred the recommendation
- outcome after follow-through
- later review label: useful, not useful, inconclusive, or superseded

Purpose:

- Make the coach accountable.
- Separate useful advice from persuasive noise.
- Preserve the reasoning trail behind important deckbuilding or gameplay
  choices.

Non-goal:

- Do not let recommendation history become parser truth.

## 2. Personal Skill Model

Track the player's recurring strengths, leaks, and improvement areas over time.

Potential dimensions:

- mulligan discipline
- opening-hand keep quality
- sideboarding effectiveness
- game 1 versus post-board adaptation
- play/draw performance
- matchup-specific weaknesses
- overboarding and underboarding patterns
- card inclusion and exclusion mistakes
- performance after deck changes
- performance after coaching focus changes

Purpose:

- Turn raw match history into a personal improvement map.
- Help answer: "What should I practice next?"

Non-goal:

- Do not treat small samples as stable personality or skill conclusions.

## 3. Experiment Engine

Make deckbuilding and testing hypotheses explicit.

Example shape:

```text
Hypothesis: +2 Cut Down improves low-curve matchups without hurting slower matchups too much.
Deck version: Golgari V12
Test window: 30 matches
Primary metric: post-board game win rate versus low-curve decks
Secondary metric: dead-card rate versus slower decks
Decision rule: revisit after at least 20 relevant games
Confidence: medium until the sample is large enough
```

Potential capabilities:

- define experiment hypotheses
- link deck versions to test windows
- define success metrics before looking at results
- track fair versus unfair comparison windows
- mark samples as too small, stale, excluded, or review-only
- route inconclusive experiments back into the testing queue

Purpose:

- Make deck iteration less vibes-based.
- Preserve why a card or shell was tested.

Non-goal:

- Do not overstate experiment results when the matchup/sample split is weak.

## 4. Coaching Review Workflow

Add a recurring review layer that helps turn sessions into lessons.

Review prompts the tool could support:

- What did I learn today?
- Which recommendation should I trust less now?
- Which recommendation became stronger?
- Which matchup needs more data?
- Which deck change is still inconclusive?
- What should I focus on next session?
- Did my actual play follow the plan I said I wanted to test?

Purpose:

- Make the coach a practice partner, not only a report generator.
- Close the loop between recommendation, action, and result.

Non-goal:

- Do not replace the player's judgment or notes.

## 5. Strategy Corpus Improvements

Build a curated, versioned strategy corpus that the AI-assisted layer can cite
instead of freewheeling from general memory.

Possible source classes:

- evergreen theory
- format-specific metagame analysis
- pro or high-level player articles
- matchup guides
- sideboard guides
- personal notes
- retired or stale sources

Possible metadata:

- source title
- author
- date
- format or deck relevance
- trust tier
- freshness
- concepts covered
- archetypes covered
- known limitations
- whether the source is evergreen or meta-dependent

Purpose:

- Improve AI explanation quality.
- Let the coach distinguish personal evidence from external strategic theory.

Non-goal:

- Do not treat strategy articles as parser truth or as always-current meta truth.

## 6. Deckbuilding Lab

Create a structured reasoning bench for card inclusions, exclusions, and
anti-meta plans.

Potential workflows:

- compare two cards for the same slot
- evaluate sideboard slots against expected matchups
- reason about low-curve, control, midrange, or combo pressure points
- identify whether a card is underperforming or merely appearing in bad contexts
- generate a focused test plan for a deck change
- flag when a card conclusion is low-sample or matchup-skewed
- separate game 1 value from post-board value

Purpose:

- Support deeper deckbuilding without pretending to simulate all of Magic.
- Help the player reason from personal data, curated strategy context, and
  clearly labeled uncertainty.

Non-goal:

- Do not build a full Magic rules simulator as part of this lab.

## 7. Operator Polish

Make the local tool pleasant, understandable, and recoverable.

Possible improvements:

- one-command startup
- local status dashboard
- "what changed since last session?" report
- clear parser health state
- branch and GitHub session health checks
- local artifact inventory
- backup and restore workflow
- simple troubleshooting panels
- clear separation between repo state, live workbook state, and deployed Apps
  Script state

Purpose:

- Reduce friction.
- Make the project easier to resume after time away.
- Keep local complexity visible instead of mysterious.

Non-goal:

- Do not turn operator polish into production deployment automation without a
  separate issue and safety review.

## Suggested Future Order

After analytics and AI-assisted coaching v1, the strongest next sequence is:

1. Recommendation Ledger
2. Personal Skill Model
3. Experiment Engine
4. Coaching Review Workflow
5. Strategy Corpus Improvements
6. Deckbuilding Lab
7. Operator Polish

Reason: the recommendation ledger makes coaching accountable first. The skill
model and experiment engine then give the coach better personal context. The
strategy corpus and deckbuilding lab improve recommendation quality. Operator
polish makes the whole system easier to live with over time.
