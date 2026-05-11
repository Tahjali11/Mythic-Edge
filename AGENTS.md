Assume I am a beginner programmer unless I explicitly say otherwise.

## Agent Constitution Entry Point

For non-trivial Codex work, first identify the thread role and use the durable rules in:

- `docs/agent_constitution.md`
- `docs/agent_threads/problem_representation.md`
- `docs/agent_threads/module_contract.md`
- `docs/agent_threads/implementation.md`
- `docs/agent_threads/contract_test.md`
- `docs/agent_threads/review.md`

These files are the portable cross-machine rule set. This `AGENTS.md` remains the root instruction entrypoint, and the `docs/agent_*` files organize the reusable constitution and role-specific rules.

Optimize for practical improvement, maintainable working code, and clearer system structure. Prefer small architectural cleanups over narrow local patches when the cleanup is still reasonably scoped and meaningfully reduces confusion, duplication, or fragility. Preserve existing behavior unless I explicitly ask for a redesign.

Explain in plain English first. When you use a technical term, define it briefly the first time unless I already used it correctly. Assume I may need help understanding imports, shared state, modules, scope, async flow, interfaces, data pipelines, and the relationship between upstream and downstream systems.

When solving a coding problem, use this order:
1. what the code is supposed to do,
2. what it is actually doing,
3. why it is failing,
4. the exact fix,
5. how to verify the fix worked.

## Working Style

- Edit files directly first unless I explicitly ask for proposal-only mode.
- Before making significant edits, inspect the relevant files first.
- Briefly state:
  - what the code is supposed to do,
  - where the likely failure point is,
  - and the minimal or cleanest viable edit plan.
- Tell me exactly what file, function, and line or section you changed.
- When helpful, show a concise diff-style summary, especially for multi-file changes.
- When multiple files must change together, explain the dependency order and edit order.
- Prefer two-pass refactors when possible:
  - first move code without changing behavior,
  - then improve behavior in a second pass.
- If a cleaner architectural cleanup is reasonably small and clearly better, prefer it over a narrow local patch.
- Flag likely breakpoints early:
  - imports,
  - missing helpers,
  - renamed functions,
  - stale references,
  - circular imports,
  - shared mutable state,
  - mismatched function signatures,
  - partially migrated code,
  - dead interfaces.

## Debugging

- Prioritize root cause over symptom patching.
- Trace the first bad value rather than guessing.
- Identify:
  - what inputs enter the system,
  - what transformations occur,
  - what output is expected,
  - where the first bad value appears.
- Distinguish clearly between:
  - bad source data,
  - bad transformation logic,
  - bad shared state,
  - bad output routing,
  - bad webhook logic,
  - bad workbook formulas or reporting logic.
- Do not use spreadsheets or formulas as error handlers when the parser, app, or script should be fixed upstream.
- If a system is partially legacy and partially refactored, label it clearly as:
  - old world,
  - new world,
  - bridge code.

## Code Quality

- Prefer the simplest maintainable solution over a more elegant but harder-to-maintain one.
- Do not introduce abstractions, helper classes, or new modules unless they clearly reduce confusion or repeated logic.
- Prefer explicit imports and clear naming over implicit behavior or magic.
- Use consistent lowercase filenames for Python modules unless there is a strong reason not to.
- Be careful with shared runtime state across modules.
- When changing shared state or interfaces, explicitly tell me what other files depend on that change.
- Call out dead code, duplicate logic, stale constants, stale imports, stale sheet references, stale webhook assumptions, and half-completed refactors.

## Validation

- Use the smallest relevant validation command first unless a broader test is actually necessary.
- Prefer focused end-to-end checks over only static reasoning when feasible.
- Do not say a fix worked unless you can point to evidence:
  - passing test,
  - successful command,
  - corrected output,
  - or a verified code path.
- After a fix, tell me:
  - what was verified,
  - what is still unverified,
  - and the next 1 to 3 best checks to run.
- If validation fails, tell me whether the likely cause is:
  - your change,
  - a pre-existing issue,
  - missing environment setup,
  - workbook drift,
  - deployment drift,
  - or an unrelated downstream dependency.

## Assumptions

- If information is missing, state your assumptions clearly.
- If the assumption is low-risk, use the safest reasonable default and continue.
- If the assumption is risky, ask before proceeding.
- If a fix is only partial, say exactly which layer is fixed and which layers are still unverified.

## Python-Specific

- Assume I may need help with file layout, imports, module boundaries, shared state ownership, and async flow.
- Make code runnable with minimal edits.
- If a helper should move to another module, say exactly why.
- When refactoring across modules, explicitly identify:
  - what moves,
  - what stays,
  - what imports change,
  - what signatures change,
  - and what order the edits should happen in.

## Apps Script and Google Sheets

- Use the actual workbook tab names I am using.
- Warn me if code still points to retired sheets, stale functions, dead menu items, mismatched headers, or old helper ranges.
- Prefer normalized upstream data over formula-heavy downstream reconstruction when the parser or script can provide cleaner outputs.
- Respect the existing workbook layout unless a schema change is clearly necessary.
- Prefer additive and reversible workbook changes over destructive ones.
- Before structural workbook changes, preserve a rollback path when possible.
- Do not delete archive, raw, debug, helper, or summary layers unless there is a clear replacement that preserves observability.

## Project Layers

Treat this project as layered:
1. MTGA raw log source
2. parser and state interpretation
3. webhook / transport layer
4. workbook landing sheets
5. helper formulas
6. dashboard / reporting tabs

Default source of truth for this project:
- raw events: MTGA log only
- event interpretation: Python parser/state layer
- final match facts: normalized MatchSummary / Match Log parser-managed fields
- final game facts: normalized GameLogRow / Game Log parser-managed fields
- webhook / Apps Script: transport and upsert layer, not truth layer
- helper tabs: support logic, not truth layer
- dashboard / reporting tabs: display layer, not truth layer

If a requested change would move truth ownership from one layer to another, say so explicitly before making the change.

When a system spans parser -> webhook -> sheet -> formulas:
- identify which layer owns the truth,
- identify which layers are transport only,
- identify which layers are display only,
- prefer fixing truth-producing layers upstream before patching downstream display layers unless I explicitly ask for a downstream-only workaround.

## Drift Handling

For workbook-connected changes, explicitly distinguish between:
- live workbook state,
- repository code state,
- deployed Apps Script state.

If they differ, label the issue clearly as:
- workbook drift,
- repo drift,
- deployment drift,
- or a combination.

If you fix one layer but not the others, say exactly which layer is now ahead and what still needs to be synced.

When workbook structure or column order has drifted:
- first determine whether the break comes from:
  - hardcoded workbook formulas,
  - Apps Script formula-reset logic,
  - header-based script lookups,
  - hidden helper tab dependencies,
  - or downstream dashboard formulas.
- state which one broke before patching it.
- when possible, update both:
  - the live workbook behavior,
  - and the repo copy of the generating script,
  in the same pass.

## Workbook Schema Changes

If changing a workbook schema, explicitly state:
- which tabs are affected,
- which columns are added, removed, moved, or repurposed,
- what formulas or scripts depend on those columns,
- and what visible workbook effect should appear afterward.

When updating the workbook directly, tell me:
- the code-side change,
- the workbook-side effect,
- and the rollback path.

## Event-Driven and Stateful Logic

- Explain the event lifecycle before changing derived outputs.
- Prefer fixing event interpretation, state ownership, and deduplication upstream before compensating in formulas.
- Be especially careful with:
  - match identity,
  - game identity,
  - winner fields,
  - play/draw fields,
  - mulligan counts,
  - deduplication keys,
  - provisional-vs-final values,
  - posted-once guards.

## Live vs Final Rows

- If a row can update live during a match and be reconciled later, explicitly distinguish between:
  - provisional live values,
  - final reconciled values.
- Do not treat provisional workbook values as final truth if the parser has a later final reconciliation path.
- If a bug affects only the live phase or only the final phase, say which one.

## Interface Changes

When changing interfaces between layers, update the full contract in one coherent pass when possible:
- parser output fields,
- webhook receiver expectations,
- destination sheet/tab and columns,
- helper/formula dependencies,
- dashboard/reporting effects,
- validation fixtures or tests.

Afterward, summarize the new contract clearly.

## Validation for This Project

- Prefer focused end-to-end checks that follow one event, one game, or one match through the full pipeline.
- Prefer representative real logs, payloads, or fixture rows over toy examples.
- For workbook changes, tell me what exact visible change should appear in:
  - the landing sheet,
  - the helper/support sheet,
  - the reporting/dashboard sheet.

## Destructive or High-Risk Changes

- Ask before deleting tabs, mass-clearing ranges, renaming many workbook elements, changing webhook payload shapes, or removing debug/archive/helper layers.
- If a risky structural change is justified, explain why it is better than the safest incremental alternative.

## Card Data

- If card data matters, prefer the approved designated card data source over memory or hardcoded assumptions.
- If multiple card identifiers exist, explicitly distinguish them before building logic around them.

## Teaching Style

- Give deeper conceptual explanations when the issue is fundamental, especially around modules, imports, shared state, async flow, interfaces, and data pipelines.
- Still give me the concrete answer and the concrete edit. Do not make me infer the solution from hints alone.

## Review Style

When reviewing code or workbook logic, do not just say it looks good. Tell me:
1. what is correct,
2. what is still broken,
3. what is highest priority to fix next,
4. the exact edit you made or recommend.

## Scope and Checkpoints

- If a problem spans multiple files and the path is clear, prefer completing the full coherent wiring pass in one go rather than stopping halfway.
- Before broad refactors, identify the smallest stable checkpoint where the system should still run.
- Keep changes easy to review, revert, and isolate.
- Do not silently expand scope beyond the stated problem without telling me.

## End-of-Task Handoff

At the end of a multi-file or multi-layer change, give a short handoff summary:
- what changed,
- what was verified,
- what is still unverified,
- what I should test next.

## Operational Safety

- Do not invent, rotate, overwrite, or delete credentials, tokens, webhook URLs, environment variables, or external connections unless I explicitly ask.
- If one is missing or broken, identify it clearly before proceeding.
- Follow repository-local instructions, scripts, and validation rules when they exist.

## Project Registry

Current project registry for Mythic Edge:

### Truth-Producing Layers
- `src/mythic_edge_parser/app/state.py`
  - owns match/game interpretation state
  - builds normalized match and game summaries from MTGA events
- `src/mythic_edge_parser/app/models.py`
  - defines normalized row shapes and summary payload structure
- `src/mythic_edge_parser/app/extractors.py`
  - extracts structured facts from raw MTGA event payloads

### Parser / Runtime Entry Points
- `main.py`
  - primary human-friendly parser entry point
- `src/mythic_edge_parser/app/runner.py`
  - main runtime loop
  - connects stream -> filtering -> state updates -> outputs
- `live_print_filtered_v11_match_summary.py`
  - compatibility wrapper entry point

### Raw and Support Data
- `data/match_logs/`
  - local raw/filtered event archives by date
- `data/oracle_data/`
  - card catalog and lookup artifacts
- `data/tier_sources/`
  - external metagame source snapshots and normalization data
- `data/runtime_logs/`, `data/failed_posts/`, `data/bad_events/`, `data/status/`
  - observability and troubleshooting artifacts

### Transport Layer
- `src/mythic_edge_parser/app/outputs.py`
  - webhook posting and outbound row transport
- `tools/google_apps_script/Code.gs`
  - Apps Script receiver/upsert logic for Google Sheets
  - transport and workbook update layer, not source of truth

### Workbook Landing Sheets
- `Match Log`
  - authoritative match-level landing sheet for parser-managed match facts
- `Game Log`
  - authoritative game-level landing sheet for parser-managed game facts
- `MTGA Match Summary Feed`
  - legacy / bridge summary landing sheet when still present
- `MTGA Raw Archive`
  - legacy / optional raw-event landing sheet when still present
- `Webhook Debug`
  - transport/debug observability layer

### Workbook Support and Display Layers
- `Helper Table`
  - helper/support layer for formulas, dropdowns, and tier buckets
  - not a truth layer
- `Tier Source Data`
  - hidden support sheet for scraped metagame source rows
  - not a truth layer
- `Dashboard`
  - reporting and analytics display layer
  - not a truth layer
- `Experiments`
  - experiment definition and comparison configuration layer
  - supports reporting, but does not override parser truth unless explicitly designed to

### Card and Tier Sync Tools
- `sync_card_catalog.py`
  - refreshes the local Arena-aware card catalog
- `validate_arena_ids.py`
  - validates Arena IDs observed in logs against the card catalog
- `sync_tier_buckets.py`
  - refreshes metagame tier source snapshots

### Workbook / Historical Repair Tools
- `backfill_game_log_from_match_logs.py`
  - replays saved local logs into normalized historical game rows

### Launcher / Operator Tools
- `tools/auto_launcher/manasight_launcher_auto.py`
  - local operator UI for starting the parser and checking health/troubleshooting artifacts

### Current Bridge-Code Areas
- `Code.gs` + live workbook formulas
  - bridge between normalized parser outputs and live reporting tabs
- legacy summary/archive tabs if still present
  - bridge from older phases of the project
- helper formulas that mirror or classify parser-managed fields
  - support layer only, not truth layer

When working in this repo, prefer updating the truth-producing layer first unless I explicitly ask for a workbook-only workaround.
