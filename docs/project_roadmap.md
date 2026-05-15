# Mythic Edge Project Roadmap

This document is the durable answer source for the question: "What is the next step?"

Use it with current repo, issue, branch, and PR state. If this roadmap conflicts with an active issue, accepted
contract, or explicit user instruction, follow the current artifact and record the conflict.

## Roadmap Order

1. Parser module audit suite
   - Goal: establish contracts, reviews, and focused validation for parser modules.
   - Status note: treated as the completed foundation for the next phases, but verify branch and PR state when using
     this document from a fresh machine.

2. Code hardening suite
   - Goal: improve resilience around tests, advisory typing, protected-surface checks, dependency setup, and drift
     budget tooling.
   - Next-step rule: if hardening work is still in progress, finish and integrate it before starting a major new
     product layer.

3. Player.log evidence ledger / drift protection suite
   - Goal: protect the parser and downstream tools against MTGA `Player.log` drift as much as possible.
   - The ledger is a QA/provenance layer, not a second parser and not a workbook workaround.
   - It should answer:
     - what log evidence supports each parser-managed fact
     - whether expected evidence is still present
     - whether a field disappeared, changed shape, or conflicts with another field
     - whether downstream tools should treat a value as observed, derived, inferred, unknown, conflict, or
       legacy-enriched
     - what focused issue should be opened when drift is detected

4. Local analytics foundation
   - Goal: produce deterministic, non-AI analytics from normalized parser outputs and ledger/provenance metadata.
   - Good first analytics surfaces:
     - matchup performance
     - game 1 vs post-board performance
     - play/draw splits
     - mulligan outcomes
     - opening hand patterns
     - sideboarding effectiveness
     - card inclusion/exclusion performance
     - sample-size and confidence warnings

5. AI-assisted coaching layer
   - Goal: use AI to summarize, compare, explain, and propose hypotheses from parser-produced facts, deterministic
     analytics, confidence labels, and curated strategy-corpus excerpts.
   - AI must not own parser truth for match result, game result, play/draw, mulligan count, opening hand, card
     actions, deck submission, webhook row identity, workbook schema, or parser-managed fields.

## How To Answer "What's The Next Step?"

1. Inspect current state:
   - `git status --short --branch`
   - active tracker issues and PRs
   - current integration branch health
   - current contracts, handoffs, and review reports

2. Find the earliest unfinished roadmap phase.

3. Recommend the next workflow role:
   - Use Codex G if the phase is implemented but not integrated.
   - Use Codex A if the next phase needs a new problem representation or tracker.
   - Use Codex B if a problem representation exists but there is no contract.
   - Use Codex C/D/E/F according to the normal module workflow when implementation is already scoped.

4. Preserve truth ownership:
   - Parser/state owns event interpretation and normalized match/game facts.
   - Ledger owns evidence/provenance and drift diagnostics.
   - Analytics reads downstream facts and provenance.
   - AI coaching reads analytics and curated strategy context, but remains inference/recommendation only.

## Current Strategic Recommendation

After the code hardening suite is complete and integrated, prioritize the Player.log evidence ledger / drift protection
suite before building major analytics tools.

Reason: analytics and coaching are only as trustworthy as the parser facts they consume. The ledger gives future
analytics a way to know not only what happened, but how the project knows it and how confident downstream tools should
be.

## Long-Horizon Idea Parking Lot

For ideas beyond the current roadmap, see `docs/future_enhancement_ideas.md`.

Expected next tracker after code hardening:

```text
Player.log Evidence Ledger / Drift Protection Suite
```

Expected first child issue:

```text
Codex A: Problem representation for Player.log evidence ledger and parser drift protection
```
