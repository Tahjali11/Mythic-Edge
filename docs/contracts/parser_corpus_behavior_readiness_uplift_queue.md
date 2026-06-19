# Parser Corpus Behavior Readiness Uplift Queue Contract

## Module

Parser corpus behavior-readiness uplift queue under tracker #158.

Plain English: after issue #462, Mythic Edge can see that the corpus parity map
is classification-complete but not parser-behavior-ready. This contract sorts
the 26 not-parser-behavior-ready rows into safe future work classes so the team
can choose the next child issue without starting #388 too early, promoting
blocked rows by default, changing parser behavior in a planning pass, or
claiming readiness from taxonomy coverage.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/475
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
- Related parser-evidence pipeline tracker:
  https://github.com/Tahjali11/Mythic-Edge/issues/388
- Parent private-evidence gate: https://github.com/Tahjali11/Mythic-Edge/issues/434
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/462
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/474
- Previous merge commit: `4c108c598a2a7ca554a8ecc61cceff1120a688ac`
- Base branch inspected: `main`
- Contract branch: `codex/parser-corpus-behavior-readiness-uplift-queue-475`
- Risk tier: High
- Status: contract only

Required agent docs:

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`

Related authority:

- `docs/contracts/parser_corpus_readiness_metrics.md`
- `docs/implementation_handoffs/parser_corpus_readiness_metrics_comparison.md`
- `docs/contract_test_reports/parser_corpus_readiness_metrics.md`
- `docs/contracts/parser_corpus_parity_expansion.md`
- `docs/contracts/parser_corpus_parity_residual_gap_readiness_review.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`
- issue #388 and child issues #381 through #387, as deferred pipeline context
  only

## Purpose

Define a safe ordering and classification policy for future work that may move
some not-ready corpus families toward parser-behavior readiness.

This contract does not authorize implementation, fixture creation, parser
changes, private evidence execution, manifest promotion, tracker closure, or
pipeline activation. It is the queue map that future Codex A/B threads should
use when selecting the next child issue.

## Observed Current Behavior

Observed on `main` at
`4c108c598a2a7ca554a8ecc61cceff1120a688ac`:

- Issue #475 is open.
- Tracker #158 remains open.
- Related parser-evidence pipeline tracker #388 remains open and deferred.
- Parent private-evidence issue #434 remains open.
- Issue #462 is complete after PR #474.
- The corpus parity CLI reports:

```text
Corpus parity report: partial_coverage_map_ready (45 families; committed=6, synthetic=14, report_only=19, blocked=6 [private=2, external=4], missing=0, parser_behavior_ready=no)
```

Derived readiness metrics:

```yaml
classification_complete: true
parser_behavior_ready: false
parser_behavior_ready_family_count: 19
total_scenario_families: 45
committed_parser_behavior_families: 5
synthetic_parser_behavior_families: 14
report_only_families: 19
blocked_families: 6
blocked_private_evidence_families: 2
blocked_external_boundary_families: 4
pipeline_activation_ready_for_issue_388: false
readiness_verdict: "classification_complete_not_behavior_ready"
```

The 26 not-parser-behavior-ready rows are:

- `manifest.metadata`
- `session.ledger_metadata`
- `core_gameplay.draft_with_games`
- `log_runtime.rotation`
- `log_runtime.unknown_entry`
- `connection.firewall_or_network_drop`
- `timer.inactivity_timeout`
- `deck_api.deck_summary`
- `deck_api.deck_upsert`
- `deck_api.store_pack_inbox_or_crafting`
- `gameplay_stress.opponent_auto_concede`
- `gameplay_stress.conjure`
- `gameplay_stress.spellbook`
- `gameplay_stress.companion_or_large_deck`
- `gameplay_stress.action_attribution`
- `gameplay_stress.event_ordering`
- `drift_debug.recycle_or_rollback`
- `drift_debug.missing_message_type`
- `drift_debug.rename_or_rotation_collision`
- `drift_debug.phantom_or_deck_origin`
- `mythic_edge.evidence_ledger_provenance`
- `mythic_edge.confidence_finality_degradation`
- `mythic_edge.workbook_row_coverage`
- `mythic_edge.live_diagnostics`
- `mythic_edge.private_log_report_only_drift`
- `mythic_edge.analytics_readiness_labels`

## Scope Decision

This contract is a queue and policy artifact only.

Codex B may:

- classify not-ready rows;
- recommend future child issue order;
- define gates for parser-behavior fixture work, private-evidence work, and
  external-boundary work;
- define #388 / #381 activation gates;
- route the queue to review.

Codex B must not:

- implement code;
- edit the corpus manifest or session ledger;
- promote any report-only, blocked-private, or blocked-external row;
- create fixtures;
- run private/live checks;
- start #388 or #381;
- claim behavior readiness, release readiness, production behavior, analytics
  truth, AI truth, coaching truth, or tracker completion.

## Owning Layer

Owning layer: Corpus / Provenance.

This contract owns only future-work classification and queue order for corpus
readiness uplift. It does not own parser behavior, parser correctness, fixture
truth, private evidence, external evidence, analytics truth, release readiness,
deploy readiness, production behavior, or tracker completion.

## Internal Project Area

Primary: Corpus / Provenance.

Supporting: Quality / Governance for workflow sequencing, protected-surface
checks, and review discipline.

This slice is not a Parser behavior module, parser-evidence pipeline module,
private evidence execution module, analytics module, AI module, coaching
module, CI gate, merge gate, deploy gate, readiness gate, or production module.

## Truth Owner

Truth owner for current readiness metrics:

- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`
- `docs/contracts/parser_corpus_readiness_metrics.md`

Truth owner for current corpus status rows:

- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`

Truth boundary:

- Corpus parity may classify which rows are candidates for future behavior
  uplift.
- Parser modules own event interpretation and parser behavior.
- Golden replay owns committed fixture execution after a later contract
  authorizes a fixture.
- Private evidence remains local and approval-gated under #434 and related
  private-evidence contracts.
- Public external taxonomy remains category reference only.
- Analytics, workbook, Google Sheets, Apps Script, webhook transport, local app,
  Match Journal, overlay, AI/model-provider behavior, coaching, CI, merge,
  deploy, production, and tracker lifecycle remain downstream or out of scope.

## Bridge-Code Status

`not_bridge_code`

This contract creates no bridge code and authorizes no data flow changes. It is
a queue policy document for future scoped issues.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/parser_corpus_behavior_readiness_uplift_queue.md`

Optional future review artifact:

- `docs/contract_test_reports/parser_corpus_behavior_readiness_uplift_queue.md`

Files read for context but not modified by this contract:

- `docs/contracts/parser_corpus_readiness_metrics.md`
- `docs/implementation_handoffs/parser_corpus_readiness_metrics_comparison.md`
- `docs/contract_test_reports/parser_corpus_readiness_metrics.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`
- relevant row-specific contracts under `docs/contracts/`

Not owned by this contract:

- parser modules;
- parser event classes;
- parser state final reconciliation;
- router semantics;
- diagnostics, golden replay, feature-equity, drift, evidence-ledger, or
  analytics behavior;
- corpus manifest or session-ledger status changes;
- fixtures or expected outputs;
- private/local artifacts;
- external corpus contents;
- workbook schema, webhook payload shape, Apps Script behavior, Google Sheets
  sync, output transport, runtime status files, failed posts, workbook exports,
  generated data, CI gates, merge readiness, deploy readiness, production
  behavior, or tracker completion.

## Public Interface

No runtime public API is added.

The public artifact is the queue classification below. Future Codex A/B
threads may depend on these row classes when selecting the next child issue,
but they must still inspect live GitHub/repo state before acting.

## Row Classes

### Class A: Non-Behavior Governance / Provenance Rows

These rows should not be forced into parser-behavior fixtures. They describe
corpus metadata, provenance metadata, workbook-facing evidence boundaries,
diagnostics/report boundaries, or analytics labels.

| Row | Current status | Queue decision |
| --- | --- | --- |
| `manifest.metadata` | `covered_report_only` | Keep report-only. |
| `session.ledger_metadata` | `covered_committed` without `parser_behavior_verified` | Keep committed metadata; consider metric carve-out, not behavior fixture. |
| `mythic_edge.evidence_ledger_provenance` | `covered_report_only` | Keep report-only. |
| `mythic_edge.confidence_finality_degradation` | `covered_report_only` | Keep report-only. |
| `mythic_edge.workbook_row_coverage` | `covered_report_only` | Keep report-only. |
| `mythic_edge.live_diagnostics` | `covered_report_only` | Keep report-only unless a later private/live diagnostics evidence issue is explicitly approved. |
| `mythic_edge.analytics_readiness_labels` | `covered_report_only` | Keep report-only. |

Recommended action:

1. Create a future metric-semantics issue if #388's "all 45 families" start
   condition should exclude non-behavior governance/provenance rows.
2. Do not create parser fixtures for these rows just to satisfy a metric.
3. Do not claim these rows block parser behavior in the same way as gameplay,
   deck API, log-runtime, or drift behavior rows.

### Class B: Safe Synthetic / Committed Behavior Candidate Rows

These rows are plausible future parser-behavior fixture or golden-replay
candidates, subject to their own child issue and contract. They must use
Mythic Edge-owned synthetic or sanitized committed evidence only.

| Row | Current status | Recommended route |
| --- | --- | --- |
| `core_gameplay.draft_with_games` | `covered_report_only` | High-priority competitive-core child issue; likely sanitized/synthetic completed draft match fixture plan. |
| `deck_api.deck_summary` | `covered_report_only` | Deck API behavior fixture child issue if existing parser support can be verified. |
| `deck_api.deck_upsert` | `covered_report_only` | Deck API behavior fixture child issue if existing parser support can be verified. |
| `gameplay_stress.opponent_auto_concede` | `covered_report_only` | Reduced synthetic game-end/no-action fixture model; avoid intent claims. |
| `gameplay_stress.companion_or_large_deck` | `covered_report_only` | Reduced synthetic deck-shape fixture model; avoid decklist truth and legality claims. |
| `gameplay_stress.action_attribution` | `covered_report_only` | Synthetic/replay behavior coverage only after action-fact expectations are narrowed. |
| `gameplay_stress.event_ordering` | `covered_report_only` | Synthetic/replay behavior coverage only after ordering expectations are narrowed. |
| `drift_debug.missing_message_type` | `covered_report_only` | Synthetic parser/drift fixture candidate; avoid reconstructing missing GameState. |

Recommended action:

1. Prefer competitive-core rows first.
2. Start with `core_gameplay.draft_with_games` unless the user selects a
   different priority.
3. Use Codex A for one narrow child issue at a time.
4. Use Codex B contracts before any fixture, parser, or metadata change.

### Class C: Behavior Candidate Rows Requiring Extra Framing

These rows may become behavior candidates, but they need a smaller prerequisite
or careful problem representation before any implementation route.

| Row | Current status | Required framing |
| --- | --- | --- |
| `log_runtime.rotation` | `covered_report_only` | Decide whether this is parser behavior, stream/tailer behavior, or local runtime behavior before fixture work. |
| `log_runtime.unknown_entry` | `covered_report_only` | Decide whether existing unknown-entry routing tests already prove behavior or whether a sanitized/synthetic fixture is needed. |
| `deck_api.store_pack_inbox_or_crafting` | `covered_report_only` | Split store, pack, inbox, and crafting surfaces or keep as a report-only blind-spot boundary. |
| `drift_debug.rename_or_rotation_collision` | `covered_report_only` | Decide whether synthetic collision evidence can prove behavior without live file-system truth. |
| `drift_debug.phantom_or_deck_origin` | `covered_report_only` | Keep deck-origin and hidden-card non-claims explicit before any fixture route. |

Recommended action:

1. Do not bundle these into a broad uplift PR.
2. Use Codex A to frame each row or split row before Codex B contracts.
3. Prefer report-only preservation when a parser-behavior fixture would imply
   file-system truth, hidden-card truth, deck-origin truth, or production
   behavior.

### Class D: Blocked Private-Evidence Rows

These rows require explicit private-evidence approval and must stay gated by
#434 and later local-only contracts.

| Row | Current status | Required gate |
| --- | --- | --- |
| `connection.firewall_or_network_drop` | `blocked_private_evidence` | Requires explicit private/firewall/network evidence authorization. |
| `mythic_edge.private_log_report_only_drift` | `blocked_private_evidence` | Requires explicit private-log drift execution authorization. |

Recommended action:

1. Do not run private checks in Codex A/B/C/E without explicit user approval.
2. Do not promote these rows by default.
3. Preserve local-only offset-window and redaction rules from the private
   evidence contracts.
4. Do not treat private evidence rows as prerequisites for the next safe
   synthetic behavior child unless the user explicitly chooses that path.

### Class E: Blocked External-Boundary Rows

These rows remain blocked by external-reference boundaries or external evidence
needs. Public taxonomy can name them; it does not prove Mythic Edge support.

| Row | Current status | Required gate |
| --- | --- | --- |
| `timer.inactivity_timeout` | `blocked_external_boundary` | Needs owned synthetic reduced model or approved evidence plan; no live timeout checks by default. |
| `gameplay_stress.conjure` | `blocked_external_boundary` | Needs generated-card evidence boundary; no hidden-card or decklist truth. |
| `gameplay_stress.spellbook` | `blocked_external_boundary` | Needs option-list/generated-card evidence boundary; no hidden option truth. |
| `drift_debug.recycle_or_rollback` | `blocked_external_boundary` | Needs parser-evidence pipeline output or reduced synthetic drift model. |

Recommended action:

1. Keep these rows blocked unless a later contract selects a safe evidence
   generation path.
2. Do not claim parser support from adjacent coverage, public taxonomy, or
   report-only boundaries.
3. Consider these after the safer Class B queue unless the user explicitly
   prioritizes them.

## Recommended Future Issue Order

Default order, unless the user explicitly chooses otherwise:

1. Codex E review of this queue contract.
2. Codex A child issue for readiness-metric applicability semantics:
   distinguish non-behavior governance/provenance rows from behavior-applicable
   rows without weakening #388.
3. Codex A child issue for `core_gameplay.draft_with_games` behavior uplift.
4. Codex A child issue for `gameplay_stress.opponent_auto_concede` reduced
   behavior uplift.
5. Codex A child issue for deck API behavior uplift, starting with
   `deck_api.deck_summary` or `deck_api.deck_upsert`.
6. Codex A child issue for action attribution / event ordering fixture
   strategy, either split or explicitly paired.
7. Codex A child issue for missing-message-type / unknown-entry behavior
   clarification.
8. Revisit Class C row split decisions.
9. Revisit Class E external-boundary rows.
10. Revisit Class D private-evidence rows only with explicit approval.
11. Revisit #388 / #381 activation only after metrics and user approval agree.

This order is intentionally conservative. It prioritizes rows that are most
likely to produce safe, owned, reviewable parser-behavior evidence without
private/live data.

## #388 / #381 Activation Gates

Issue #388 and child issue #381 remain deferred by default.

They may start only when at least one of these conditions is met:

1. `pipeline_activation_ready_for_issue_388` is `true` in the repo-owned corpus
   parity report, after any approved metric-applicability amendments; or
2. the user explicitly reorders the lane and provides approval to start #388 or
   #381 despite the metric being false.

Neither `classification_complete: true` nor `missing: 0` is enough.

If a future metric-applicability issue excludes non-behavior governance rows
from the denominator, it must preserve the private-evidence, external-boundary,
and report-only non-claims and must not silently start #388.

## Inputs

Allowed inputs:

- committed corpus manifest metadata;
- committed session-ledger metadata;
- existing corpus parity report matrix and readiness metrics;
- existing corpus contracts and handoffs;
- GitHub issue metadata for #158, #388, #381 through #387, #434, #462, and
  #475;
- public external taxonomy only through already committed summary/category
  references.

Forbidden inputs:

- private Player.log files;
- UTC_Log files;
- raw log lines;
- private app-data contents;
- private smoke outputs;
- live MTGA checks;
- Alchemy, Conjure, Spellbook, firewall, network, packet, OS/router, or
  private smoke checks;
- exact private paths;
- raw hashes;
- runtime logs;
- generated/private/runtime artifacts;
- SQLite files;
- workbook exports;
- secrets, credentials, tokens, API keys, or webhook URLs;
- decklists, card choices, private strategy notes, or private reports;
- Manasight raw logs, `.log.gz` files, raw session payloads, compressed corpus
  files, hash lists, byte-size lists, capture-date row lists, parser source,
  or external corpus contents.

## Outputs

Allowed output for this contract:

- the queue contract file;
- a workflow handoff to Codex E for contract review;
- optional future review report.

Forbidden output:

- changed parser code;
- changed report code;
- changed tests;
- changed manifest or session-ledger status;
- new fixtures;
- private evidence artifacts;
- generated data;
- runtime artifacts;
- readiness claims;
- #388 or #381 activation;
- tracker closure.

## Required Guarantees

- The queue must preserve #462 readiness metric semantics.
- The queue must not promote rows or authorize implementation.
- Non-behavior governance/provenance rows must be visible and must not be
  forced into fake parser fixtures.
- Report-only rows must not become parser-behavior-ready without dedicated
  evidence.
- Private-evidence rows must remain gated by explicit approval and local-only
  contracts.
- External-boundary rows must remain blocked until owned evidence or a reduced
  synthetic model is separately contracted.
- Competitive-core prioritization must remain advisory and not become release,
  deploy, production, analytics, AI, coaching, or tracker-completion truth.

## Unknowns

- Whether #388 should keep "all 45 families" as its start condition or switch
  to a behavior-applicable denominator after a later metric-semantics issue.
- Whether `session.ledger_metadata` should remain permanently excluded from
  parser-behavior readiness metrics.
- Whether `mythic_edge.live_diagnostics` should always remain report-only or
  eventually receive a private/local evidence path.
- Whether `log_runtime.rotation` belongs in parser behavior, local runtime
  behavior, or a separate stream/tailer readiness queue.
- Whether Conjure and Spellbook should share a generated-card prerequisite.

## Suspected Gaps

- The readiness metric correctly exposes 19/45 parser-behavior-ready families,
  but it does not yet distinguish "not applicable to behavior" from "not ready
  behavior target."
- Several report-only rows are intentionally non-behavior support concepts.
  Treating them as fixture targets could create misleading evidence.
- Several behavior-like report-only rows need narrow expected-fact models
  before fixture work can be honest.
- Private and external rows still require evidence policy decisions outside
  this contract.

## Invariants

- `parser_behavior_ready` remains false at the observed base.
- `pipeline_activation_ready_for_issue_388` remains false at the observed base.
- #388 and #381 remain deferred unless their start gate is explicitly met or
  the user explicitly reorders the lane.
- #434 remains the parent gate for private-evidence rows.
- Corpus reports remain review metadata, not parser truth or readiness truth.
- No raw/private/external corpus evidence is committed by this contract.

## Error Behavior

If a future child issue tries to implement multiple row classes at once, route
back to Codex A/B for scope reduction.

If a future implementation would promote private-evidence or external-boundary
rows without explicit approval and a dedicated contract, stop.

If a future implementation would create fixtures for non-behavior governance
rows only to satisfy a metric, stop and create a metric-semantics issue.

If a future workflow starts #388 or #381 while
`pipeline_activation_ready_for_issue_388` is false and without explicit user
approval, stop and route to the user.

If any proposed work requires private/live data, stop and record the blocked
condition. Do not run private/live checks without explicit approval.

## Side Effects

Contract pass side effect:

- adds `docs/contracts/parser_corpus_behavior_readiness_uplift_queue.md`

No runtime side effects are authorized.

## Dependency Order

1. Review and accept this queue contract.
2. Decide whether a metric-semantics child issue should clarify non-behavior
   rows before behavior uplift.
3. Create exactly one narrow Codex A child issue for the selected next row or
   row family.
4. Write a Codex B contract for that child issue.
5. Only then consider Codex C implementation.

## Compatibility

This contract is compatible with the current corpus report because it does not
change schemas, coverage statuses, report fields, or fixture metadata.

It deliberately avoids new status vocabulary. Future metric-semantics work may
add derived metrics, but it must preserve current report consumers and
non-claims.

## Tests Required

For this contract-only pass:

```bash
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py
python3 tools/check_agent_docs.py
python3 -m ruff check src tests tools
git diff --check
```

Path-scoped checks:

```bash
printf '%s\n' docs/contracts/parser_corpus_behavior_readiness_uplift_queue.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' docs/contracts/parser_corpus_behavior_readiness_uplift_queue.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
```

No private/live checks are allowed.

## Acceptance Criteria

- `docs/contracts/parser_corpus_behavior_readiness_uplift_queue.md` exists.
- The contract classifies all 26 not-parser-behavior-ready rows.
- The contract distinguishes non-behavior governance rows from behavior
  candidates.
- The contract identifies private-evidence and external-boundary gates.
- The contract recommends a future child-issue order.
- The contract keeps #388 and #381 deferred by default.
- The contract preserves parser truth, private evidence, analytics, AI,
  coaching, readiness, and production non-claims.

## Next Workflow Action

Recommended next role: Codex E: Module Reviewer.

Pasteable Codex E prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer for issue #475.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/475

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/158

Related pipeline tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/388

Parent private-evidence issue:
https://github.com/Tahjali11/Mythic-Edge/issues/434

Previous completed issue:
https://github.com/Tahjali11/Mythic-Edge/issues/462

Previous completed PR:
https://github.com/Tahjali11/Mythic-Edge/pull/474

Previous merge commit:
4c108c598a2a7ca554a8ecc61cceff1120a688ac

Base branch:
main

Contract:
docs/contracts/parser_corpus_behavior_readiness_uplift_queue.md

Goal:
Review the behavior-readiness uplift queue contract. Verify that it preserves #462 readiness semantics, classifies all 26 not-parser-behavior-ready rows, keeps #388/#381 deferred, avoids implementation authorization, and does not promote report-only, private-evidence, or external-boundary rows by default.

Review:
- docs/contracts/parser_corpus_behavior_readiness_uplift_queue.md
- docs/contracts/parser_corpus_readiness_metrics.md
- docs/implementation_handoffs/parser_corpus_readiness_metrics_comparison.md
- docs/contract_test_reports/parser_corpus_readiness_metrics.md
- tests/fixtures/parser_corpus/corpus_manifest.v1.json
- tests/fixtures/parser_corpus/session_ledger.v1.json
- src/mythic_edge_parser/app/corpus_parity_report.py
- tests/test_corpus_parity_report.py
- issue #475
- issue #388 and #381 only as deferred pipeline context

Lead with findings. If no issues are found, say so and record residual risks.

Do not implement code. Do not open a PR unless explicitly instructed. Do not close #158, #388, #434, or #475. Do not start #388 or #381. Do not change corpus statuses, parser behavior, fixtures, tests, workbook/webhook/App Script behavior, analytics truth, AI truth, coaching truth, release readiness, production behavior, or tracker lifecycle. Do not run private Player.log, UTC_Log, app-data, live MTGA, Alchemy, network, packet, OS/router, firewall/drop, or private smoke checks.
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/475"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  related_pipeline_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  parent_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/462"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/474"
  previous_merge_commit: "4c108c598a2a7ca554a8ecc61cceff1120a688ac"
  completed_thread: "B"
  next_thread: "E"
  source_artifact: "GitHub issue #475"
  target_artifact: "docs/contracts/parser_corpus_behavior_readiness_uplift_queue.md"
  verdict: "behavior_readiness_uplift_queue_contract_ready_for_review"
  risk_tier: "High"
  branch: "codex/parser-corpus-behavior-readiness-uplift-queue-475"
  base_branch: "main"
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  recommended_after_review:
    - "Codex A child issue for readiness-metric applicability semantics"
    - "Codex A child issue for core_gameplay.draft_with_games behavior uplift"
  validation:
    - "PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json"
    - "PYTHONPATH=src python3 -m pytest -q tests/test_corpus_parity_report.py"
    - "python3 tools/check_agent_docs.py"
    - "python3 -m ruff check src tests tools"
    - "git diff --check"
    - "path-scoped secret/private-marker scan"
    - "path-scoped protected-surface scan"
  stop_conditions:
    - "Do not close tracker #158 without explicit lifecycle approval."
    - "Do not close tracker #388 or parent #434."
    - "Do not promote blocked or report-only rows by default."
    - "Do not start #388 or #381 unless the readiness metric says the start condition is met or the user explicitly reorders the lane."
    - "Do not claim parser support, full corpus parity, private smoke success, release readiness, production behavior, analytics truth, AI truth, coaching truth, or tracker completion."
```
