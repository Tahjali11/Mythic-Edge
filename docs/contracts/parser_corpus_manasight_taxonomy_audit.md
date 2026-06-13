# Parser Corpus Manasight Taxonomy Audit Contract

## Module

Metadata-only Manasight corpus taxonomy audit against Mythic Edge corpus
parity.

Plain English: this contract defines a safe audit artifact that maps public
Manasight corpus category metadata to Mythic Edge corpus parity scenario
families and current Mythic Edge coverage states. It must help choose future
#158 child issues without importing external corpus files, changing parser
behavior, or claiming full parity.

## Source Issue

- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/352

## Tracker

- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158

## Metadata

- role: Codex B / Module Contract Writer
- worktree: dedicated local issue #352 worktree
- branch: `codex/manasight-corpus-taxonomy-audit`
- base_branch: `main`
- observed_base_commit: `f91e38e7de421e52e44f2e6d9e693c40bbe7218b`
- target_artifact: `docs/contracts/parser_corpus_manasight_taxonomy_audit.md`
- expected_audit_artifact:
  `docs/contract_test_reports/parser_corpus_manasight_taxonomy_audit.md`
- expected_next_artifact:
  `docs/implementation_handoffs/parser_corpus_manasight_taxonomy_audit_comparison.md`
- risk_tier: High
- status: contract only

Required agent docs:

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`

Related Mythic Edge authority:

- `docs/contracts/parser_corpus_parity_expansion.md`
- `docs/contracts/parser_gsm_truncation_corpus_coverage.md`
- `docs/contracts/parser_feature_equity_corpus_ratchet.md`
- `docs/contracts/parser_golden_replay_harness.md`
- `docs/contracts/parser_diagnostics_mode.md`
- `docs/contracts/parser_gsm_truncation.md`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`

Public external references inspected as metadata only:

- https://github.com/manasight/manasight-corpus
- https://github.com/manasight/manasight-corpus/blob/main/README.md
- https://github.com/manasight/manasight-corpus/blob/main/sessions.md
- https://github.com/manasight/manasight-corpus/blob/main/smoke-corpus-manifest.toml

## Prerequisite Checkpoint

Issue #351 is complete.

Verified evidence:

- GitHub issue #351 is closed.
- PR #353 is merged into `main`.
- PR #353 merge commit is
  `f91e38e7de421e52e44f2e6d9e693c40bbe7218b`.
- The #352 worktree was fast-forwarded to that commit before this contract was
  written.
- A fresh Mythic Edge corpus parity report from repo-owned inputs now shows
  `drift_debug.gsm_truncation` as `covered_synthetic`, not provisional.

If Codex C later runs from a stale checkout that does not include
`f91e38e7de421e52e44f2e6d9e693c40bbe7218b`, it must stop, refresh the branch,
or explicitly record that its local snapshot is stale. It must not regress the
GSM truncation mapping to a pre-#351 provisional state.

## Owning Layer

Owning layer: Corpus / Provenance.

The audit owns metadata comparison and roadmap planning only. It does not own
parser interpretation, Mythic Edge coverage truth, external corpus truth, or
future implementation priority by itself.

## Internal Project Area

Corpus / Provenance.

This work consumes Parser evidence and Quality / Governance workflow evidence,
but the artifact itself is a corpus parity planning report.

## Truth Owner

Truth owner for Mythic Edge coverage statuses:

- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`

Truth owner for parser behavior:

- parser modules, router, event classes, and parser state.

Truth owner for public Manasight metadata:

- the public `manasight/manasight-corpus` repository.

Truth boundary:

- Manasight public metadata is reference taxonomy only.
- The #352 audit may map and compare category labels, but it must not treat
  Manasight metadata as Mythic Edge parser support, executable tests, fixture
  truth, analytics truth, AI truth, merge readiness, deploy readiness, or
  tracker-completion authority.
- Mythic Edge corpus parity report statuses are Mythic Edge-owned coverage
  statuses. They must not be overwritten by external corpus labels.

## Bridge-Code Status

`bridge_code`

Source project area: External / Collaboration Surface.

Consuming project area: Corpus / Provenance.

Allowed data flow:

```text
public Manasight corpus metadata categories
  -> bounded taxonomy mapping rows
  -> Mythic Edge corpus parity scenario families and coverage statuses
  -> future #158 child issue recommendations
```

Forbidden reverse flow:

- The audit must not import Manasight corpus files.
- The audit must not copy Manasight parser source.
- The audit must not change Mythic Edge parser behavior to improve a table.
- The audit must not close #158 or declare full corpus parity.
- The audit must not move parser truth into external metadata, workbook
  formulas, analytics, AI, dashboard logic, Apps Script, webhook transport, or
  generated reports.

Protected surfaces explicitly not touched:

- parser behavior
- parser state final reconciliation
- parser event classes
- router semantics
- match/game identity
- deduplication
- workbook schema
- webhook payload shape
- Apps Script behavior
- Google Sheets sync
- output transport
- runtime status artifacts
- failed delivery artifacts
- workbook exports
- SQLite/local app behavior
- analytics truth
- AI truth
- coaching behavior
- OpenAI/model-provider behavior
- production behavior

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/parser_corpus_manasight_taxonomy_audit.md`

Future Codex C artifacts authorized by this contract:

- `docs/contract_test_reports/parser_corpus_manasight_taxonomy_audit.md`
- `docs/implementation_handoffs/parser_corpus_manasight_taxonomy_audit_comparison.md`

Optional future artifacts, only if Codex C finds Markdown alone is not enough
and keeps them category-only:

- `tests/fixtures/parser_corpus/manasight_taxonomy_reference.v1.json`
- `tests/test_corpus_manasight_taxonomy_audit.py`
- `src/mythic_edge_parser/app/corpus_manasight_taxonomy_audit.py`

The optional files are not required for V1. A Markdown audit report is the
preferred first implementation.

Files that may be read but not changed by Codex C unless a later contract
explicitly authorizes it:

- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `tests/test_corpus_parity_report.py`
- parser, router, diagnostics, golden replay, feature-equity, workbook,
  webhook, Apps Script, analytics, local app, AI, and production files

## Public Interface

V1 public interface is a documentation/report artifact:

```text
docs/contract_test_reports/parser_corpus_manasight_taxonomy_audit.md
```

The audit artifact must be readable by humans and structured enough for Codex
threads to use as the next roadmap input. No public Python API, CLI flag,
environment variable, schema migration, workbook column, webhook field, or
runtime route is required.

If Codex C chooses to add optional machine-readable support, it must keep the
same logical schema defined below and must remain metadata-only.

## Observed Current Behavior

Observed from the post-#351 worktree at
`f91e38e7de421e52e44f2e6d9e693c40bbe7218b`:

- Issue #352 is open.
- Tracker #158 is open.
- Issue #351 is closed and merged through PR #353.
- The Mythic Edge corpus parity report is still
  `partial_coverage_map_ready`.
- Current Mythic Edge report summary:
  - total scenario families: 45
  - covered committed: 6
  - covered synthetic: 2
  - covered report-only: 0
  - partial: 3
  - missing: 28
  - blocked external boundary: 6
- `drift_debug.gsm_truncation` is now `covered_synthetic`.
- Several Manasight-style categories remain missing, partial, or blocked in
  Mythic Edge, including draft-with-games, sealed entry/deckbuild/matches,
  detailed-logs-disabled, log rotation, reconnect, inactivity timeout, deck
  management/store, Conjure, Spellbook, rollback/recycle, rename collision,
  and phantom/deck-origin drift.

Observed public Manasight metadata:

- Repository: `manasight/manasight-corpus`
- Default branch: `main`
- Repository description: sanitized MTG Arena log corpus for parser smoke
  testing.
- Latest observed push: `2026-05-28T21:22:52Z`.
- `smoke-corpus-manifest.toml` advertises
  `corpus_tag = "manasight-corpus-v1"`.
- The public manifest currently contains 44 file metadata entries.
- Public session headings and README metadata indicate scenario categories
  such as draft, Standard Bo1/Bo3, log rotation, detailed logs disabled,
  connection/firewall/Wi-Fi/clumsy network sessions, deck management/store,
  sealed entry/deckbuild/matches, Conjure, Spellbook, mulligan stress,
  opponent auto-concede, phantom drift, rename collision, rollback/limbo,
  truncation/recycle drift, timer/inactivity, and related parser drift cases.

These observations are metadata only. The audit must not copy the 44 manifest
rows, hashes, sizes, dates, raw filenames as a canonical mirror, raw session
payloads, or any external log contents into Mythic Edge.

## Allowed Public Metadata Inputs

Allowed external inputs:

- Manasight repository URL, owner/name, default branch, description, and
  observed public pushed timestamp.
- README-level corpus purpose and sanitization/contribution policy summary.
- `smoke-corpus-manifest.toml` corpus tag.
- Total count of public manifest file metadata entries.
- Bounded category hints derived from public filenames, without copying the
  full manifest or making filenames canonical.
- Public `sessions.md` headings, section labels, and short scenario category
  descriptions.
- Bounded public session heading examples, at most three per mapped category,
  when useful for explaining a taxonomy mapping.
- Public release/category metadata if needed for category labels only.

Allowed Mythic Edge inputs:

- The current corpus parity report generated from repo-owned inputs.
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`.
- `tests/fixtures/parser_corpus/session_ledger.v1.json`.
- Current corpus parity, golden replay, feature-equity, diagnostics, and GSM
  truncation contracts.

## Forbidden Inputs

Forbidden external inputs:

- Manasight `.log` or `.log.gz` files.
- Decompressed Manasight logs.
- Raw external corpus payloads.
- Compressed corpus files.
- Mirrored external corpus directories.
- Wholesale copies of `smoke-corpus-manifest.toml`.
- Wholesale copies of `sessions.md`.
- External SHA-256 hash lists, file sizes, and capture dates as Mythic Edge
  canonical data.
- Manasight parser source code.

Forbidden local/private inputs:

- raw private `Player.log` excerpts;
- private local logs;
- generated data;
- SQLite databases or WAL/SHM/journal files;
- runtime artifacts;
- failed delivery artifacts;
- workbook exports;
- credentials, tokens, API keys, webhook URLs, or secrets.

## Audit Artifact Path

Required V1 audit artifact:

```text
docs/contract_test_reports/parser_corpus_manasight_taxonomy_audit.md
```

This artifact is a metadata audit/report. It is not a contract, executable
fixture, parser test, CI gate, release-readiness report, or tracker-closeout
report.

The artifact must include:

- source snapshot metadata;
- #351 dependency status;
- Mythic Edge corpus parity snapshot;
- Manasight public metadata summary;
- taxonomy mapping table;
- follow-up issue recommendations;
- privacy/protected-surface assertions;
- residual risks and non-claims.

## Taxonomy Mapping Schema

Each audit row must use this logical shape:

```yaml
manasight_category_id: "connection.reconnect"
manasight_category_label: "Reconnect and connection health"
manasight_metadata_sources:
  - "README.md"
  - "sessions.md"
  - "smoke-corpus-manifest.toml"
manasight_public_session_examples:
  - "Session heading only, optional, bounded"
mythic_edge_scenario_family: "connection.reconnect"
mythic_edge_current_coverage_status: "blocked_external_boundary"
mythic_edge_coverage_basis:
  - "external_reference_only"
comparison_status: "mapped_blocked_external_boundary"
dependency_notes:
  - "Requires Mythic Edge-owned fixture or report-only evidence before coverage claim."
privacy_boundary: "external_metadata_only_no_log_import"
recommended_follow_up_issue_type: "codex_a_child_issue"
recommended_priority: "High"
notes:
  - "Do not infer parser support from Manasight category presence."
```

Required fields:

- `manasight_category_id`
- `manasight_category_label`
- `manasight_metadata_sources`
- `mythic_edge_scenario_family`
- `mythic_edge_current_coverage_status`
- `mythic_edge_coverage_basis`
- `comparison_status`
- `dependency_notes`
- `privacy_boundary`
- `recommended_follow_up_issue_type`
- `recommended_priority`
- `notes`

Optional field:

- `manasight_public_session_examples`

The optional examples must be public session headings or high-level labels
only. They must not include raw log snippets, raw payload excerpts, full
external rows, hashes, file sizes, capture dates, or copied session bodies.

## Comparison Status Vocabulary

Allowed comparison statuses:

- `mapped_covered`
- `mapped_partial`
- `mapped_missing`
- `mapped_blocked_external_boundary`
- `mapped_blocked_private_evidence`
- `mapped_deferred`
- `mapped_not_applicable`
- `needs_new_mythic_edge_family`
- `needs_parser_behavior_before_corpus_claim`
- `provisional_pending_dependency`

Definitions:

- `mapped_covered`: the Manasight category maps to a Mythic Edge scenario
  family with `covered_committed`, `covered_synthetic`, or
  `covered_report_only`. The row must still preserve the exact Mythic Edge
  coverage status, so synthetic coverage is not overread as committed
  real-log coverage.
- `mapped_partial`: the category maps to a Mythic Edge family with `partial`
  coverage.
- `mapped_missing`: the category maps to a Mythic Edge family with no Mythic
  Edge-owned coverage.
- `mapped_blocked_external_boundary`: the category is known from external
  metadata, but Mythic Edge must not import external corpus material and needs
  its own future fixture or report-only evidence.
- `mapped_blocked_private_evidence`: the category likely requires private or
  locally captured evidence that must remain report-only unless separately
  sanitized and authorized.
- `mapped_deferred`: the category is valid but intentionally deferred by
  current roadmap scope.
- `mapped_not_applicable`: the category does not apply to Mythic Edge goals
  under current contracts.
- `needs_new_mythic_edge_family`: the public Manasight category does not map
  cleanly to an existing Mythic Edge scenario family.
- `needs_parser_behavior_before_corpus_claim`: the category cannot receive an
  honest corpus coverage claim until Mythic Edge has parser behavior, focused
  tests, or diagnostics support for it.
- `provisional_pending_dependency`: a dependency issue is not merged in the
  local snapshot. This status should not be used for #351 in the current
  post-merge worktree.

## Mythic Edge Coverage Status Definitions

The audit must reuse the existing corpus parity coverage statuses:

- `covered_committed`
- `covered_synthetic`
- `covered_report_only`
- `partial`
- `missing`
- `deferred`
- `blocked_private_evidence`
- `blocked_external_boundary`
- `not_applicable`

The audit must not introduce new Mythic Edge coverage statuses. Any additional
labels are comparison-only and must be clearly scoped to the audit artifact.

## Expected Mapping Families

Codex C should map at least these Manasight-style categories:

- corpus manifest metadata
- session ledger metadata
- Standard Bo1
- Standard Bo3 / Traditional Bo3
- draft-only
- draft with games
- sealed entry
- sealed deckbuilding
- sealed matches
- detailed logs disabled
- log rotation
- malformed/headerless entries
- timestamp anomalies
- unknown entries
- reconnect/disconnect/connection health
- firewall, Wi-Fi, or directional network drop
- connection error payloads
- active player timer
- inactivity timeout
- pre-match idle/timer state
- StartHook deck snapshot
- deck summaries
- deck upsert / event set deck
- store, pack, inbox, or crafting surfaces
- mulligan stress
- opponent auto-concede or no-action games
- Conjure
- Spellbook
- companion or large-deck shape
- action attribution and event ordering
- GSM truncation markers
- recycle/rollback/limbo drift
- missing GameState message type / parser type-field failures
- rename/recycle collision
- phantom/deck-origin drift

Codex C may add rows when public metadata clearly identifies a relevant
category, but it must not copy the public corpus wholesale.

## #351 Dependency Behavior

Because #351 is merged in the current branch:

- `drift_debug.gsm_truncation` must map as non-provisional.
- Its Mythic Edge coverage status should be `covered_synthetic`.
- Its comparison status should be `mapped_covered`.
- Its notes must preserve that GSM truncation is parser-owned data-loss
  evidence, not recovered GameState truth.

If Codex C detects a stale local branch where #351 is absent:

- stop and fast-forward if safe; or
- record `provisional_pending_dependency` for the GSM truncation row and state
  that the audit must be rerun after #351 is merged.

Do not silently produce a pre-#351 audit from stale repo state.

## Invariants

- Public Manasight metadata remains reference taxonomy only.
- Mythic Edge coverage status comes only from Mythic Edge repo-owned corpus
  parity inputs.
- Mapping a Manasight category to a Mythic Edge family does not prove parser
  support or semantic equivalence.
- Missing, partial, blocked, or deferred categories must stay visibly labeled.
- The audit must not import, copy, mirror, or commit external logs, compressed
  corpus files, raw session payloads, or external corpus contents.
- The audit must not close #158 or #352.
- The audit must not change parser behavior or protected downstream surfaces.
- The audit must not call OpenAI or any model provider.
- The audit must not become analytics truth, AI truth, coaching truth,
  gameplay advice, hidden-card inference, archetype classification, merge
  readiness, deploy readiness, public-release readiness, or tracker
  completion.

## Error Behavior

If public Manasight metadata is unavailable, Codex C may proceed only if it
records the fetch failure and marks affected rows as `provisional` or
`reference_unavailable` in prose. It must not fabricate public category facts.

If the current Mythic Edge corpus parity report cannot be generated, Codex C
must stop unless it can explain why a docs-only audit is still valid from
committed report inputs. It must not invent Mythic Edge coverage statuses.

If any proposed artifact includes raw/private or external corpus content, stop
and remove it. Do not sanitize by editing external payloads into a committed
fixture inside this issue.

If the taxonomy suggests parser behavior is missing, route that to a future
Codex A problem representation rather than implementing parser behavior.

## Side Effects

Allowed side effects for Codex C:

- create the audit artifact at
  `docs/contract_test_reports/parser_corpus_manasight_taxonomy_audit.md`;
- create an implementation handoff at
  `docs/implementation_handoffs/parser_corpus_manasight_taxonomy_audit_comparison.md`;
- optionally add a category-only JSON reference and tests if Markdown alone is
  inadequate, while preserving the forbidden-input rules.

Forbidden side effects:

- code changes by default;
- parser behavior changes;
- parser event class changes;
- corpus fixture imports from Manasight;
- raw/private log commits;
- generated report JSON commits unless explicitly scoped as safe
  category-only metadata;
- runtime writes;
- SQLite/local app changes;
- workbook/webhook/App Script/Google Sheets changes;
- analytics/AI/model-provider behavior.

## Dependency Order

Codex C should implement in this order:

1. Verify #351 is present in the local branch and regenerate the Mythic Edge
   corpus parity report from repo-owned inputs.
2. Inspect public Manasight metadata as reference taxonomy only.
3. Create the audit artifact with source snapshot metadata and non-claims.
4. Fill taxonomy mapping rows using current Mythic Edge coverage statuses.
5. Identify recommended future #158 child issues without closing #158.
6. Run docs-scoped validation and artifact scans.
7. Write the implementation handoff.

## Compatibility

The audit must remain compatible with:

- `parser_corpus_manifest.v1`
- `parser_corpus_session_ledger.v1`
- `parser_corpus_compatibility_report.v1`
- existing Mythic Edge corpus coverage statuses
- existing corpus parity report CLI
- #351's post-merge GSM truncation coverage
- existing protected-surface rules

The audit does not authorize schema version changes.

## Tests Required

Codex C should run:

```bash
PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
python3 -m pytest -q tests/test_corpus_parity_report.py
python3 tools/check_agent_docs.py
git diff --check
git diff --name-only origin/main...HEAD | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
git diff --name-only origin/main...HEAD | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
git diff --name-only origin/main...HEAD | python3 tools/select_validation.py --base origin/main --paths-from-stdin
```

If Codex C adds optional Python helpers or JSON validators, it must also run:

```bash
python3 -m pytest -q tests/test_corpus_manasight_taxonomy_audit.py
python3 -m ruff check src tests tools
```

Codex E should verify:

- #351 dependency is treated as merged in the current branch;
- the audit uses public metadata as reference taxonomy only;
- no Manasight raw logs, `.log.gz` files, compressed corpus files, raw session
  payloads, or mirrored external corpus files are committed;
- no raw private `Player.log` excerpts or local/private/generated artifacts
  are committed;
- the audit does not claim full Mythic Edge corpus parity;
- follow-up recommendations do not close #158 or implement parser behavior;
- all changed files are within the contracted docs/report scope unless a
  later contract explicitly authorizes more.

Codex F should stage only reviewed files and must not open a PR to `main`
without explicit base approval if the workflow requires that approval.

Codex G must not close tracker #158 unless explicitly instructed by the user.

## Acceptance Criteria

- `docs/contracts/parser_corpus_manasight_taxonomy_audit.md` exists.
- The contract records #351 as completed and merged.
- The contract defines allowed public metadata inputs and forbidden external
  raw inputs.
- The contract defines the audit artifact path.
- The contract defines taxonomy mapping schema and comparison status
  vocabulary.
- The contract reuses Mythic Edge corpus coverage statuses.
- The contract defines validation requirements for Codex C/E/F/G.
- The contract preserves privacy and protected-surface boundaries.

## Open Questions And Contract Risks

- The public Manasight metadata may change over time. Codex C must include an
  observed date or commit/pushed timestamp in the audit artifact.
- A category-level mapping may reveal missing Mythic Edge scenario families.
  Those should become future issue candidates, not silent schema changes.
- Some categories may require parser behavior before corpus coverage is honest.
  This audit must not implement that behavior.
- A Markdown table may be enough for V1, but future automation may need a
  machine-readable category-only reference. That should stay optional in this
  slice.

## Next Workflow Action

Next role: Codex C / Module Implementer.

Pasteable prompt:

```yaml
prompt: |
  Use the Mythic Edge agent constitution.
  Use $mythic-edge-workflow.

  Act as Codex C: Module Implementer for issue #352 under tracker #158.

  Issue:
  https://github.com/Tahjali11/Mythic-Edge/issues/352

  Tracker:
  https://github.com/Tahjali11/Mythic-Edge/issues/158

  Worktree:
  dedicated local issue #352 worktree

  Branch:
  codex/manasight-corpus-taxonomy-audit

  Contract:
  docs/contracts/parser_corpus_manasight_taxonomy_audit.md

  Goal:
  Produce a metadata-only Manasight corpus taxonomy audit that maps public
  Manasight corpus metadata categories to Mythic Edge corpus parity scenario
  families and current Mythic Edge coverage states.

  Do:
    - Verify #351 is present in the local branch and regenerate the Mythic Edge
      corpus parity report from repo-owned inputs.
    - Inspect public Manasight README, sessions.md, and
      smoke-corpus-manifest.toml as metadata/reference taxonomy only.
    - Create docs/contract_test_reports/parser_corpus_manasight_taxonomy_audit.md.
    - Include source snapshot metadata, #351 dependency status, the current
      Mythic Edge corpus parity snapshot, taxonomy mapping rows, follow-up
      issue recommendations, privacy/protected-surface assertions, and
      non-claims.
    - Produce docs/implementation_handoffs/parser_corpus_manasight_taxonomy_audit_comparison.md.

  Do not:
    - Implement parser behavior changes.
    - Open a PR.
    - Close #158 or #352.
    - Target main directly.
    - Import, copy, mirror, or commit Manasight raw logs, .log.gz files, raw
      session payloads, compressed corpus files, or external corpus contents.
    - Claim full Mythic Edge corpus parity from taxonomy mapping alone.
    - Change parser behavior, parser state final reconciliation, parser event
      classes, router semantics, match/game identity, deduplication, workbook
      schema, webhook payload shape, Apps Script behavior, Google Sheets sync,
      output transport, runtime status files, failed delivery artifacts,
      workbook exports,
      analytics truth, AI truth, coaching behavior, OpenAI/model-provider
      behavior, or production behavior.
    - Commit raw private Player.log excerpts, private local logs, generated
      data, SQLite files, runtime artifacts, workbook exports, credentials,
      tokens, API keys, or webhook URLs.
    - Stage or commit unless explicitly asked.

  Validation:
    - PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json
    - python3 -m pytest -q tests/test_corpus_parity_report.py
    - python3 tools/check_agent_docs.py
    - git diff --check
    - git diff --name-only origin/main...HEAD | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
    - git diff --name-only origin/main...HEAD | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
    - git diff --name-only origin/main...HEAD | python3 tools/select_validation.py --base origin/main --paths-from-stdin
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/352"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  dependency_completed: "https://github.com/Tahjali11/Mythic-Edge/issues/351"
  dependency_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/353"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/parser_corpus_manasight_taxonomy_audit.md"
  target_artifact: "docs/contract_test_reports/parser_corpus_manasight_taxonomy_audit.md"
  expected_handoff: "docs/implementation_handoffs/parser_corpus_manasight_taxonomy_audit_comparison.md"
  verdict: "contract_ready_for_metadata_only_taxonomy_audit"
  risk_tier: "High"
  branch: "codex/manasight-corpus-taxonomy-audit"
  base_commit: "f91e38e7de421e52e44f2e6d9e693c40bbe7218b"
  validation:
    - "PYTHONPATH=src python3 -m mythic_edge_parser.app.corpus_parity_report tests/fixtures/parser_corpus/corpus_manifest.v1.json --session-ledger tests/fixtures/parser_corpus/session_ledger.v1.json"
    - "python3 -m pytest -q tests/test_corpus_parity_report.py"
    - "python3 tools/check_agent_docs.py"
    - "git diff --check"
    - "git diff --name-only origin/main...HEAD | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin"
    - "git diff --name-only origin/main...HEAD | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin"
    - "git diff --name-only origin/main...HEAD | python3 tools/select_validation.py --base origin/main --paths-from-stdin"
  stop_conditions:
    - "Do not implement parser behavior changes."
    - "Do not open a PR."
    - "Do not close #158 or #352."
    - "Do not target main directly."
    - "Do not import, copy, mirror, or commit Manasight raw logs, .log.gz files, raw session payloads, compressed corpus files, or external corpus contents."
    - "Use public Manasight corpus metadata only as reference taxonomy."
    - "Do not claim full Mythic Edge corpus parity from taxonomy mapping alone."
    - "Do not change parser behavior, parser state final reconciliation, parser event classes, router semantics, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets sync, output transport, runtime status files, failed delivery artifacts, workbook exports, analytics truth, AI truth, coaching behavior, OpenAI/model-provider behavior, or production behavior."
    - "Do not commit raw private Player.log excerpts, private local logs, generated data, SQLite files, runtime artifacts, workbook exports, credentials, tokens, API keys, or webhook URLs."
```
