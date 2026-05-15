# Code Hardening Seed ADRs Contract

Source issue: https://github.com/Tahjali11/Mythic-Edge/issues/64

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/33

Branch target: `codex/code-hardening-suite`

Previous hardening context:

- Issue #60 / PR #61 added parser event schema snapshot tests and merged into
  `codex/code-hardening-suite` at
  `8016d82e292c43c3348e94d67189a60c86897448`.
- Issue #62 / PR #63 added ADR policy governance and merged into
  `codex/code-hardening-suite` at
  `774076bcdaa00af100ac43375b54140bab07e50e`.
- Issue #62 is closed.
- Tracker #33 remains open.
- `docs/decisions/README.md` and `docs/decisions/ADR_TEMPLATE.md` exist.
- No numbered ADRs exist yet.

Agent docs read:

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/decisions/README.md`
- `docs/decisions/ADR_TEMPLATE.md`
- `docs/agent_threads/problem_representation.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/problem_representation.md`
- `docs/templates/module_contract.md`
- `docs/templates/workflow_handoff.md`
- `.github/pull_request_template.md`

Hardening contracts read:

- `docs/contracts/code_hardening_adr_policy.md`
- `docs/contracts/code_hardening_protected_surface_gate.md`
- `docs/contracts/code_hardening_pr_drift_budget.md`
- `docs/contracts/code_hardening_parser_event_schema_snapshots.md`

Remote parser-audit and evidence-ledger artifacts inspected from `origin/main`
because they are absent from the current hardening branch:

- `origin/main:docs/contracts/parser_models.md`
- `origin/main:docs/contracts/parser_state.md`
- `origin/main:docs/contracts/parser_outputs.md`
- `origin/main:docs/contracts/parser_sheet_schema.md`
- `origin/main:docs/contracts/parser_sheet_exports.md`
- `origin/main:docs/problem_representations/player_log_evidence_ledger.md`
- `origin/main:docs/contracts/player_log_evidence_ledger.md`

This contract defines the exact seed Architecture Decision Records, or ADRs,
to create in the next implementation thread. It is a contract artifact only.
It does not create ADR files, implement policy changes, change runtime
behavior, open a PR, target `main`, or mark tracker #33 complete.

## Module

Seed architecture decision records.

The seed ADRs should turn already-established Mythic Edge project decisions
into stable, citable decision records:

- parser/state owns truth
- local deterministic scoring decides while LLMs explain
- `Player.log` is observable evidence that can drift
- protected surfaces and schema changes require explicit authorization

Plain English: the seed ADRs should write down the rules the project is
already using. They should not create new runtime behavior or loosen review
requirements.

## Owning Layer

Repository governance, ADR documentation, workflow policy, and code-hardening
documentation.

Truth boundary:

- ADRs record durable project decisions.
- ADRs do not own parser truth, workbook truth, webhook truth, Apps Script
  behavior, production deployment state, or live workbook state.
- Parser and state remain the source of truth for event interpretation and
  normalized match/game facts.
- Issues and module contracts remain required for scoped implementation work.
- Accepted ADRs are durable precedent, not automatic permission to change
  protected runtime surfaces.

## Files Owned By This Contract

- `docs/contracts/code_hardening_seed_adrs.md`

Expected future implementation files owned by this contract:

- `docs/decisions/ADR-0001-parser-owns-truth.md`
- `docs/decisions/ADR-0002-local-deterministic-scorer-decides-llm-explains.md`
- `docs/decisions/ADR-0003-player-log-drift-policy.md`
- `docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md`
- `docs/decisions/README.md`, index section only
- `docs/implementation_handoffs/code_hardening_seed_adrs_comparison.md`

Optional future review artifact:

- `docs/contract_test_reports/code_hardening_seed_adrs.md`

Files referenced but not owned:

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/decisions/ADR_TEMPLATE.md`
- `.github/pull_request_template.md`
- hardening contracts listed above
- parser-audit and evidence-ledger artifacts on `origin/main`
- `src/mythic_edge_parser/app/analytics_sidecar.py`
- `tests/test_analytics_sidecar.py`
- `docs/Mythic_Edge_Deep_Dive_Guide.md`

## Observed Current State

Observed on `codex/code-hardening-suite` during this contract pass:

- Current HEAD is
  `774076bcdaa00af100ac43375b54140bab07e50e`.
- `docs/decisions/README.md` says no numbered ADRs exist yet.
- `docs/decisions/ADR_TEMPLATE.md` exists and does not consume a number.
- `tests/test_event_schema_snapshots.py` and
  `tests/fixtures/schema_snapshots/` exist from PR #61.
- `docs/contracts/parser_api_common.md` exists locally.
- The parser audit contracts for models, state, outputs, sheet schema, and
  sheet exports are absent locally but present on `origin/main` and
  `origin/codex/parser-module-audit-suite`.
- The Player.log evidence-ledger problem representation and contract are
  absent locally but present on `origin/main` and
  `origin/codex/parser-module-audit-suite`.
- Pre-existing local worktree changes are present outside this contract pass.
  Codex C/F must inspect status and avoid absorbing unrelated files.

## Branch And Source Document Caveats

The current hardening branch is allowed to reference source artifacts that
live on `origin/main` or `origin/codex/parser-module-audit-suite` without
copying those artifacts into the hardening branch.

Required caveats:

- Codex C may use `git show origin/main:<path>` or
  `git show origin/codex/parser-module-audit-suite:<path>` to read missing
  source artifacts.
- `origin/main` is the preferred source when both remote refs contain the
  same parser-audit or evidence-ledger artifact, because PR #56 merged the
  parser module audit suite into `main`.
- If `origin/main` and `origin/codex/parser-module-audit-suite` differ for a
  cited artifact, Codex C must record the difference in the implementation
  handoff and avoid resolving it inside the seed-ADR implementation.
- This issue does not authorize syncing, merging, or rebasing
  `codex/code-hardening-suite` with `main`.
- This issue does not authorize copying parser-audit contracts or
  evidence-ledger docs into the hardening branch.
- Seed ADRs may cite remote source documents with a remote-ref prefix, for
  example `origin/main:docs/contracts/parser_models.md`, when the file is
  absent locally.
- ADRs must be clear that remote source documents are citations and context,
  not new hardening-branch files.

## ADR Status Requirement

All four seed ADR files must use:

```text
Status: Accepted
```

Interpretation:

- The decisions being recorded are already established by existing repo
  governance, hardening contracts, parser-audit contracts, and tracker issues.
- The status becomes effective only after the seed ADR PR is reviewed and
  merged into the approved branch.
- While the PR is open, reviewers may still request wording changes or route
  back to Codex B if the contract is wrong or ambiguous.

If Codex C believes any seed ADR should instead be `Proposed`, it must stop
and route back to Codex B before writing the ADR files.

## Shared ADR Requirements

Every seed ADR must follow `docs/decisions/ADR_TEMPLATE.md` and include:

- Title
- Status
- Date
- Decision owners / workflow role
- Related issues
- Related PRs
- Related contracts, handoffs, or review reports
- Related ADRs
- Context
- Decision
- Scope
- Non-Goals
- Alternatives considered
- Consequences
- Truth ownership impact
- Protected surfaces touched
- Validation or review evidence
- Supersedes
- Superseded by
- Follow-ups
- Notes

Required shared values:

- Date: use the implementation date in `YYYY-MM-DD` form.
- Decision owners / workflow role: `Codex C: Module Implementer / comparison thread`, with source contract
  `docs/contracts/code_hardening_seed_adrs.md`.
- Related issues must include issue #64 and tracker #33.
- Related contracts must include this contract and
  `docs/contracts/code_hardening_adr_policy.md`.
- Related ADRs must be `None` for ADR-0001 and may cite earlier seed ADRs
  when a later ADR depends on them.
- Supersedes: `None`.
- Superseded by: `None`.
- Validation or review evidence must state that runtime tests are not
  applicable for docs-only ADR creation, unless Codex C touches code.

Every seed ADR must explicitly state that it does not authorize:

- parser behavior changes
- parser state final reconciliation changes
- workbook schema changes
- webhook payload shape changes
- Apps Script behavior changes
- parser event class changes
- event `kind` value changes
- parser payload shape changes
- match identity changes
- game identity changes
- deduplication changes
- secrets, credential, token, API key, or webhook URL changes
- environment variable contract changes
- committing raw logs
- generated card/tier data changes
- runtime status file changes
- failed-post changes
- workbook export changes
- production deployment behavior changes
- merge-to-main policy changes

## Seed ADR 0001

### File

```text
docs/decisions/ADR-0001-parser-owns-truth.md
```

### Title

```text
# ADR-0001: Parser Owns Truth
```

### Required Status

```text
Status: Accepted
```

### Required Citations

Related issues:

- https://github.com/Tahjali11/Mythic-Edge/issues/1
- https://github.com/Tahjali11/Mythic-Edge/issues/5
- https://github.com/Tahjali11/Mythic-Edge/issues/33
- https://github.com/Tahjali11/Mythic-Edge/issues/62
- https://github.com/Tahjali11/Mythic-Edge/issues/64

Related PRs:

- https://github.com/Tahjali11/Mythic-Edge/pull/56
- https://github.com/Tahjali11/Mythic-Edge/pull/63

Related contracts, handoffs, or review reports:

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/decisions/README.md`
- `docs/contracts/code_hardening_adr_policy.md`
- `docs/contracts/code_hardening_seed_adrs.md`
- `origin/main:docs/contracts/parser_models.md`
- `origin/main:docs/contracts/parser_state.md`
- `origin/main:docs/contracts/parser_outputs.md`
- `origin/main:docs/contracts/parser_sheet_schema.md`
- `origin/main:docs/contracts/parser_sheet_exports.md`

### Required Decision Statement

ADR-0001 must state all of the following:

- Parser and state interpretation own MTGA event interpretation and
  normalized match/game facts.
- `state.py` owns live parser state, final reconciliation, changed-field
  detection, and in-memory match/game truth.
- `models.py` owns normalized match/game row shapes and serializer behavior.
- `sheet_schema.py` owns Python-side sync-field and workbook-facing schema
  vocabulary.
- `outputs.py`, webhook transport, Apps Script, workbook landing sheets,
  helper tabs, dashboards, and AI interpretation consume parser-produced
  facts; they do not reconstruct or override parser truth.
- Workbook formulas, helper tabs, dashboards, Apps Script, webhook transport,
  and AI-generated interpretation must not become truth owners for match
  result, game result, play/draw, mulligan count, opening hand, card actions,
  deck submission, row identity, workbook schema, or parser-managed fields.
- Any proposed move of truth ownership requires a new issue, module contract,
  review, and validation. If it would supersede this ADR, it also requires an
  ADR amendment or supersession path.

### Required Non-Goals

ADR-0001 must state that it does not:

- change parser behavior
- change parser state final reconciliation
- change workbook schema
- change webhook payload shape
- change Apps Script behavior
- change parser event classes or payload shapes
- change match/game identity or deduplication
- use dashboards, formulas, Apps Script, webhooks, or AI as parser truth
- define every module-level contract for parser code
- replace issue-specific problem representations or module contracts

### Protected Surfaces Explicitly Not Touched

ADR-0001 must explicitly list:

- parser behavior
- parser state final reconciliation
- workbook schema
- webhook payload shape
- Apps Script behavior
- parser event classes
- event `kind` values
- parser payload shapes
- match identity
- game identity
- deduplication
- secrets and environment variables
- raw logs and local/private artifacts
- generated data
- runtime status files
- failed posts
- workbook exports
- production deployment behavior
- merge-to-main policy

## Seed ADR 0002

### File

```text
docs/decisions/ADR-0002-local-deterministic-scorer-decides-llm-explains.md
```

### Title

```text
# ADR-0002: Local Deterministic Scorer Decides, LLM Explains
```

### Required Status

```text
Status: Accepted
```

### Required Citations

Related issues:

- https://github.com/Tahjali11/Mythic-Edge/issues/33
- https://github.com/Tahjali11/Mythic-Edge/issues/47
- https://github.com/Tahjali11/Mythic-Edge/issues/62
- https://github.com/Tahjali11/Mythic-Edge/issues/64

Related PRs:

- https://github.com/Tahjali11/Mythic-Edge/pull/63

Related contracts, handoffs, or review reports:

- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/decisions/README.md`
- `docs/contracts/code_hardening_adr_policy.md`
- `docs/contracts/code_hardening_seed_adrs.md`
- `src/mythic_edge_parser/app/analytics_sidecar.py`
- `tests/test_analytics_sidecar.py`
- `docs/Mythic_Edge_Deep_Dive_Guide.md`

Citation caveat:

- `analytics_sidecar.py`, `tests/test_analytics_sidecar.py`, and
  `docs/Mythic_Edge_Deep_Dive_Guide.md` are current context only. ADR-0002
  must not make them an implementation contract for future LLM or coaching
  work.

### Required Decision Statement

ADR-0002 must state all of the following:

- For future coaching, analytics, scoring, ranking, filtering, and
  confidence-aware calculations, deterministic local code owns decisions.
- Deterministic local code means repo-owned logic that can be inspected,
  tested, reviewed, rerun, and validated without relying on an LLM response.
- LLMs may summarize, classify, explain, compare alternatives, and propose
  hypotheses from parser-produced facts, deterministic analytics, confidence
  labels, and curated strategy context.
- LLM output must be labeled as inference, enrichment, recommendation,
  explanation, or hypothesis.
- LLM output must not become the truth owner for match result, game result,
  play/draw, mulligan count, opening hand, card actions, deck submission, row
  identity, workbook schema, or parser-managed fields.
- Strategy/coaching layers should carry deterministic evidence and uncertainty
  when available, including sample size, confidence warnings, and source
  labels.
- Any OpenAI, LLM, coaching, or model-backed analytics implementation requires
  its own issue, module contract, validation plan, and privacy boundary review.

### Required Non-Goals

ADR-0002 must state that it does not:

- implement OpenAI API integration
- send raw logs to any LLM
- add coaching modules
- change analytics sidecar behavior
- change parser-managed fields
- treat LLM guesses as professional-level strategic truth
- bypass future analytics or coaching module contracts
- define prompt text, model choice, token policy, API keys, or deployment
  behavior
- authorize workbook formulas or dashboards to own analytics truth

### Protected Surfaces Explicitly Not Touched

ADR-0002 must explicitly list:

- parser behavior
- parser-managed fields
- workbook schema
- webhook payload shape
- Apps Script behavior
- secrets, API keys, tokens, credentials, webhook URLs, and environment
  variables
- raw local logs
- generated data
- runtime status files
- failed posts
- workbook exports
- production deployment behavior
- merge-to-main policy

## Seed ADR 0003

### File

```text
docs/decisions/ADR-0003-player-log-drift-policy.md
```

### Title

```text
# ADR-0003: Player.log Drift Policy
```

### Required Status

```text
Status: Accepted
```

### Required Citations

Related issues:

- https://github.com/Tahjali11/Mythic-Edge/issues/11
- https://github.com/Tahjali11/Mythic-Edge/issues/33
- https://github.com/Tahjali11/Mythic-Edge/issues/47
- https://github.com/Tahjali11/Mythic-Edge/issues/60
- https://github.com/Tahjali11/Mythic-Edge/issues/62
- https://github.com/Tahjali11/Mythic-Edge/issues/64

Related PRs:

- https://github.com/Tahjali11/Mythic-Edge/pull/12
- https://github.com/Tahjali11/Mythic-Edge/pull/61
- https://github.com/Tahjali11/Mythic-Edge/pull/63

Related contracts, handoffs, or review reports:

- `docs/contracts/code_hardening_adr_policy.md`
- `docs/contracts/code_hardening_seed_adrs.md`
- `docs/contracts/code_hardening_parser_event_schema_snapshots.md`
- `tests/test_event_schema_snapshots.py`
- `tests/fixtures/schema_snapshots/`
- `origin/main:docs/problem_representations/player_log_evidence_ledger.md`
- `origin/main:docs/contracts/player_log_evidence_ledger.md`

### Required Decision Statement

ADR-0003 must state all of the following:

- MTGA `Player.log` is the project's ultimate local observable evidence
  source, but it is not absolute game truth.
- The real game state lives inside Arena. Mythic Edge can only parse what
  Arena emits.
- Arena may remove, rename, reorder, redact, or reshape log fields without
  notice.
- The parser should prioritize accuracy, explicit uncertainty, and safe
  degradation over filling missing facts with confident guesses.
- Current observed log behavior can be used as a golden baseline for tests,
  schema snapshots, and drift detection, but not as a guarantee from Wizards.
- Drift detection should distinguish parser evidence drift from webhook
  transport failure, workbook drift, deployed Apps Script drift, local artifact
  drift, and AI/analytics interpretation.
- Future ledger and drift work should use the evidence-ledger vocabulary for
  value-source labels, confidence labels, finality labels, drift flags,
  invariant checks, and degradation behavior unless a later issue, contract,
  or ADR supersedes it.
- Local private Player.log files may inform local drift reports, but committed
  fixtures must be sanitized.

Required vocabulary:

- value-source labels: `observed`, `derived`, `inferred`, `unknown`,
  `conflict`, `legacy_enriched`
- confidence labels: high, medium, low, unavailable, or the exact labels
  defined by the evidence-ledger contract if Codex C finds stricter wording
- finality labels: provisional, final, immutable, unknown, or the exact labels
  defined by the evidence-ledger contract if Codex C finds stricter wording
- drift flags: no drift, missing evidence, schema changed, conflict, degraded,
  or the exact labels defined by the evidence-ledger contract if Codex C finds
  stricter wording

### Required Non-Goals

ADR-0003 must state that it does not:

- implement the evidence ledger
- implement drift reports
- commit raw local logs
- change parser behavior
- change workbook or webhook schema
- automatically create GitHub issues from drift reports
- hide uncertainty from downstream analytics
- treat inferred or legacy-enriched values as observed truth
- define every raw log signal or parser field mapping
- replace the Player.log evidence-ledger contract

### Protected Surfaces Explicitly Not Touched

ADR-0003 must explicitly list:

- parser behavior
- parser state final reconciliation
- workbook schema
- webhook payload shape
- Apps Script behavior
- parser event classes
- event `kind` values
- parser payload shapes
- match identity
- game identity
- deduplication
- raw logs and local/private artifacts
- generated data
- runtime status files
- failed posts
- workbook exports
- production deployment behavior
- merge-to-main policy

## Seed ADR 0004

### File

```text
docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md
```

### Title

```text
# ADR-0004: Protected Surfaces And Schema-Change Policy
```

### Required Status

```text
Status: Accepted
```

### Required Citations

Related issues:

- https://github.com/Tahjali11/Mythic-Edge/issues/33
- https://github.com/Tahjali11/Mythic-Edge/issues/34
- https://github.com/Tahjali11/Mythic-Edge/issues/39
- https://github.com/Tahjali11/Mythic-Edge/issues/60
- https://github.com/Tahjali11/Mythic-Edge/issues/62
- https://github.com/Tahjali11/Mythic-Edge/issues/64

Related PRs:

- https://github.com/Tahjali11/Mythic-Edge/pull/37
- https://github.com/Tahjali11/Mythic-Edge/pull/42
- https://github.com/Tahjali11/Mythic-Edge/pull/61
- https://github.com/Tahjali11/Mythic-Edge/pull/63

Related contracts, handoffs, or review reports:

- `docs/agent_rules.yml`
- `docs/contracts/code_hardening_protected_surface_gate.md`
- `docs/contracts/code_hardening_pr_drift_budget.md`
- `docs/contracts/code_hardening_parser_event_schema_snapshots.md`
- `docs/contracts/code_hardening_adr_policy.md`
- `docs/contracts/code_hardening_seed_adrs.md`
- `tools/check_protected_surfaces.py`
- `.github/pull_request_template.md`
- `tests/test_event_schema_snapshots.py`
- `tests/fixtures/schema_snapshots/`

### Required Decision Statement

ADR-0004 must state all of the following:

- Protected surfaces require explicit issue, contract, review, and validation
  authority before semantic change.
- Protected-surface gate warnings are review signals, not automatic
  authorization and not automatic rejection.
- Clearly forbidden local, generated, private, credential, raw log, failed
  post, runtime status, and workbook export artifacts must not be committed.
- Schema shape changes require explicit scoped authorization.
- Event class changes, event `kind` changes, parser payload changes,
  workbook-facing row-key changes, sync-field changes, runtime family changes,
  webhook payload changes, Apps Script behavior changes, match/game identity
  changes, deduplication changes, and production deployment changes require
  explicit scoped authorization.
- Snapshot updates are contract-visible changes and must not be auto-updated
  by Codex without issue, contract, and review approval.
- PR drift budgets should disclose whether a change creates `No drift`,
  `Authorized drift`, `Residual drift`, or `N/A` for each protected category.
- Passing tests are necessary but not sufficient for protected-surface
  readiness. The issue, contract, review, and drift budget must agree.

### Required Non-Goals

ADR-0004 must state that it does not:

- change any protected surface by itself
- bypass the protected-surface gate
- bypass issue/contract/review workflow
- weaken secret or local artifact rules
- merge to `main` or production branches without explicit approval
- auto-update snapshots without approval
- make protected warnings fail CI without a future issue and contract
- replace module contracts for schema or runtime changes
- authorize live workbook or deployed Apps Script changes

### Protected Surfaces Explicitly Not Touched

ADR-0004 must explicitly list:

- parser behavior
- parser state final reconciliation
- workbook schema
- webhook payload shape
- Apps Script behavior
- parser event classes
- event `kind` values
- parser payload shapes
- match identity
- game identity
- deduplication
- sync field names
- runtime family names
- runtime `event_type` values
- runtime `scope` values
- secrets and environment variables
- raw logs and local/private artifacts
- generated data
- runtime status files
- failed posts
- workbook exports
- production deployment behavior
- merge-to-main policy

## README Index Update

Codex C must update only the ADR index section of:

```text
docs/decisions/README.md
```

Required change:

- Replace `No numbered ADRs exist yet.` with a sorted index of the four seed
  ADRs.

Required format:

```markdown
## ADR Index

| ADR | Status | Decision |
| --- | --- | --- |
| [ADR-0001: Parser Owns Truth](ADR-0001-parser-owns-truth.md) | Accepted | Parser/state owns event interpretation and normalized match/game facts. |
| [ADR-0002: Local Deterministic Scorer Decides, LLM Explains](ADR-0002-local-deterministic-scorer-decides-llm-explains.md) | Accepted | Deterministic local code owns scoring and LLMs explain or propose hypotheses. |
| [ADR-0003: Player.log Drift Policy](ADR-0003-player-log-drift-policy.md) | Accepted | Player.log is observable evidence that can drift; parser resilience must expose uncertainty. |
| [ADR-0004: Protected Surfaces And Schema-Change Policy](ADR-0004-protected-surfaces-and-schema-change-policy.md) | Accepted | Protected surfaces and schema changes require explicit issue, contract, review, and validation authority. |
```

README update limits:

- Do not rewrite the ADR authority model.
- Do not add seed ADR content into the README beyond the index summary.
- Do not remove the existing ADR policy sections.
- Keep the index sorted by ADR number.

## Out Of Scope

This issue does not authorize:

- creating ADR files in Codex B
- adding seed ADRs beyond the four named in this contract
- implementing policy changes beyond documentation of existing decisions
- changing code or tests
- changing parser behavior
- changing parser state final reconciliation
- changing workbook schema
- changing webhook payload shape
- changing Apps Script behavior
- changing parser event classes
- changing event `kind` values
- changing parser payload shapes
- changing match identity
- changing game identity
- changing deduplication
- changing secrets, credentials, tokens, API keys, or webhook URLs
- changing environment variable contracts
- committing raw local logs
- changing generated card/tier data
- changing runtime status files
- changing failed posts
- changing workbook exports
- changing production deployment behavior
- changing merge-to-main policy
- syncing or merging `main` into `codex/code-hardening-suite`
- copying parser-audit or evidence-ledger docs into the hardening branch
- committing unrelated local docs such as `docs/project_roadmap.md` or
  `docs/python_tooling_inventory.md`
- opening a PR from the contract writer pass
- marking tracker #33 complete

## Validation Requirements

Contract-writer validation:

```powershell
git diff --check
```

Because this contract is a new untracked file during Codex B, also validate
the new file directly:

```powershell
git diff --no-index --check -- NUL docs\contracts\code_hardening_seed_adrs.md
```

Minimum Codex C validation:

```powershell
git diff --check
py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite
rg -n "ADR-0001|ADR-0002|ADR-0003|ADR-0004" docs\decisions\README.md docs\decisions\ADR-0001-parser-owns-truth.md docs\decisions\ADR-0002-local-deterministic-scorer-decides-llm-explains.md docs\decisions\ADR-0003-player-log-drift-policy.md docs\decisions\ADR-0004-protected-surfaces-and-schema-change-policy.md
rg -n "Status: Accepted|Related issues|Related PRs|Related contracts|Decision|Non-Goals|Protected Surfaces Touched|Supersedes|Superseded By" docs\decisions\ADR-000*.md
```

Docs-only interpretation:

- Full parser tests are not required if Codex C changes only Markdown ADR
  files, the ADR README index, and the implementation handoff.
- Codex C/E/F must explicitly record that parser tests were skipped because no
  runtime code changed.
- If Codex C touches Python, tests, CI, executable tools, parser files,
  workbook schema, webhook code, Apps Script, secrets, local artifacts, or any
  protected runtime surface, it must stop and route back unless a new or
  amended contract authorizes that scope.

Recommended manual review checks:

- Exactly four numbered ADR files exist.
- The four numbered ADR filenames match this contract exactly.
- No additional numbered ADRs exist.
- Each seed ADR has `Status: Accepted`.
- Each seed ADR cites issue #64, tracker #33, this contract, and the ADR
  policy contract.
- Each seed ADR includes its required issue, PR, and source-artifact
  citations.
- Each seed ADR includes required decision statements and non-goals.
- Each seed ADR explicitly states protected surfaces not touched.
- `docs/decisions/README.md` index includes all four ADRs in numeric order.
- No raw logs, secrets, generated data, runtime status files, failed posts, or
  workbook exports are included.

## Acceptance Criteria

- `docs/contracts/code_hardening_seed_adrs.md` exists.
- The contract defines exactly four seed ADR files.
- The contract requires `Status: Accepted` for each seed ADR.
- The contract defines required citations for each seed ADR.
- The contract defines required decision statements for each seed ADR.
- The contract defines required non-goals for each seed ADR.
- The contract defines protected surfaces each ADR must explicitly not touch.
- The contract records branch/source-document caveats for artifacts absent
  from the hardening branch but present on `origin/main` or
  `origin/codex/parser-module-audit-suite`.
- The contract defines `docs/decisions/README.md` index update expectations.
- The contract defines validation requirements.
- The contract routes next work to Codex C: Module Implementer / comparison
  thread.
- The contract does not create ADR files or implement policy changes.

## Handoff Packet

Role performed: Codex B: Module Contract Writer.

Source problem representation: https://github.com/Tahjali11/Mythic-Edge/issues/64

Tracker issue: https://github.com/Tahjali11/Mythic-Edge/issues/33

Contract produced:
`docs/contracts/code_hardening_seed_adrs.md`

Risk tier: Medium for repository governance. Escalate to High if
implementation loosens parser truth ownership, authorizes protected-surface
changes by implication, weakens local artifact safety, introduces LLM truth
ownership, or changes runtime behavior.

Owning truth layer: repository governance, ADR documentation, workflow policy,
and code-hardening documentation.

Public interface:

- `docs/decisions/ADR-0001-parser-owns-truth.md`
- `docs/decisions/ADR-0002-local-deterministic-scorer-decides-llm-explains.md`
- `docs/decisions/ADR-0003-player-log-drift-policy.md`
- `docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md`
- `docs/decisions/README.md` ADR index

Invariants:

- Exactly four seed ADRs are in scope.
- Seed ADRs record existing durable policy; they do not implement behavior.
- ADRs do not authorize protected-surface changes by implication.
- Parser/state truth ownership remains unchanged.
- Remote source docs may be cited without syncing or copying them.
- Hardening work targets `codex/code-hardening-suite`, not `main`.
- Tracker #33 remains open.

Required validation: listed above.

Acceptance criteria: listed above.

Open questions or contract risks:

- ADR-0002 should remain policy-level and must not overfit to the current
  analytics sidecar implementation.
- ADR-0003 must cite remote evidence-ledger docs without importing them into
  the hardening branch.
- ADR-0004 combines protected-surface and schema-change policy for the seed
  pass; future golden fixture or drift detector policy may still need later
  ADRs.
- Existing local worktree changes outside this contract must be inspected and
  excluded by Codex C/F.

Next recommended thread role: Codex C: Module Implementer / comparison thread.

Pasteable next-thread prompt:

```text
Use $mythic-edge-workflow.
Use the Mythic Edge agent constitution.

Act as Codex C: Module Implementer / comparison thread for the Code Hardening child issue: Seed architecture decision records.

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/33

Child issue:
https://github.com/Tahjali11/Mythic-Edge/issues/64

Branch target:
codex/code-hardening-suite

Use:
- AGENTS.md
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/codex_module_workflow.md
- docs/decisions/README.md
- docs/decisions/ADR_TEMPLATE.md
- docs/agent_threads/implementation.md
- docs/contracts/code_hardening_seed_adrs.md
- docs/contracts/code_hardening_adr_policy.md
- docs/contracts/code_hardening_protected_surface_gate.md
- docs/contracts/code_hardening_pr_drift_budget.md
- docs/contracts/code_hardening_parser_event_schema_snapshots.md
- .github/pull_request_template.md
- issue #33
- issue #64
- remote source artifacts from origin/main or origin/codex/parser-module-audit-suite when absent locally, especially parser_models, parser_state, parser_outputs, parser_sheet_schema, parser_sheet_exports, player_log_evidence_ledger problem representation, and player_log_evidence_ledger contract

Goal:
Compare the current ADR policy files and source artifacts against docs/contracts/code_hardening_seed_adrs.md. Create only the four contracted seed ADR files, update only the docs/decisions/README.md ADR index, and produce docs/implementation_handoffs/code_hardening_seed_adrs_comparison.md.

Before editing:
- Confirm the branch is codex/code-hardening-suite.
- Confirm the branch is at or after PR #63 merge commit 774076b.
- Inspect git status and exclude unrelated modified or untracked files.
- Confirm no numbered ADR files exist yet.
- State what the seed ADRs are supposed to do, what source docs are local versus remote-only, and the exact docs-only implementation plan.

Do:
- Create docs/decisions/ADR-0001-parser-owns-truth.md.
- Create docs/decisions/ADR-0002-local-deterministic-scorer-decides-llm-explains.md.
- Create docs/decisions/ADR-0003-player-log-drift-policy.md.
- Create docs/decisions/ADR-0004-protected-surfaces-and-schema-change-policy.md.
- Use Status: Accepted for each seed ADR, with acceptance effective after reviewed merge.
- Include the required citations, decision statements, non-goals, protected-surface boundaries, and branch/source caveats from the contract.
- Update only the ADR index section in docs/decisions/README.md.
- Produce docs/implementation_handoffs/code_hardening_seed_adrs_comparison.md with comparison, files changed, validation, protected-surface status, remaining risks, and next recommended role.

Do not:
- Create additional numbered ADRs.
- Implement policy changes beyond the four ADR docs and README index.
- Change parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, event kind values, parser payload shapes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, production deployment behavior, or merge-to-main policy.
- Sync or merge main into the hardening branch.
- Copy parser-audit or evidence-ledger source docs into the hardening branch.
- Absorb unrelated local modified or untracked files.
- Target main.
- Mark tracker #33 complete.
- Stage, commit, open a PR, or merge unless explicitly asked.

Validation:
git diff --check
py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite
rg -n "ADR-0001|ADR-0002|ADR-0003|ADR-0004" docs\decisions\README.md docs\decisions\ADR-0001-parser-owns-truth.md docs\decisions\ADR-0002-local-deterministic-scorer-decides-llm-explains.md docs\decisions\ADR-0003-player-log-drift-policy.md docs\decisions\ADR-0004-protected-surfaces-and-schema-change-policy.md
rg -n "Status: Accepted|Related issues|Related PRs|Related contracts|Decision|Non-Goals|Protected Surfaces Touched|Supersedes|Superseded By" docs\decisions\ADR-000*.md
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/64"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/33"
  completed_thread: "B"
  next_thread: "C"
  next_role: "Codex C: Module Implementer / comparison thread"
  source_artifact: "docs/contracts/code_hardening_seed_adrs.md"
  target_artifact: "docs/implementation_handoffs/code_hardening_seed_adrs_comparison.md"
  risk_tier: "Medium"
  branch: "codex/code-hardening-suite"
  validation:
    - "git diff --check"
    - "git diff --no-index --check -- NUL docs\\contracts\\code_hardening_seed_adrs.md"
  stop_conditions:
    - "Do not create additional numbered ADRs beyond ADR-0001 through ADR-0004."
    - "Do not implement policy changes beyond the four ADR docs and README index."
    - "Do not change parser behavior, parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, event kind values, parser payload shapes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, workbook exports, production deployment behavior, or merge-to-main policy."
    - "Do not sync or merge main into the hardening branch."
    - "Do not copy parser-audit or evidence-ledger source docs into the hardening branch."
    - "Do not absorb unrelated local modified or untracked files."
    - "Do not target main; hardening work belongs on codex/code-hardening-suite."
    - "Do not mark tracker #33 complete."
```
