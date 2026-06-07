# Parser Corpus Parity Expansion Contract

## Metadata

- role: Codex B / Module Contract Writer
- issue: https://github.com/Tahjali11/Mythic-Edge/issues/291
- tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
- base_branch: main
- branch: codex/parser-corpus-parity-expansion
- base_commit: 9cb5f5b9805f530edad827378d14bf3b373b526d
- target_artifact: docs/contracts/parser_corpus_parity_expansion.md
- expected_next_artifact: docs/implementation_handoffs/parser_corpus_parity_expansion_comparison.md
- risk_tier: High
- status: contract only

Required agent docs:

- AGENTS.md
- docs/agent_rules.yml
- docs/agent_constitution.md
- docs/codex_module_workflow.md
- docs/agent_threads/module_contract.md
- docs/templates/module_contract.md

Related Mythic Edge authority:

- docs/contracts/parser_golden_replay_harness.md
- docs/contracts/parser_diagnostics_mode.md
- docs/contracts/parser_feature_equity_corpus_ratchet.md
- docs/contracts/player_log_evidence_ledger.md
- docs/contracts/player_log_evidence_ledger_schema.md
- docs/problem_representations/parser_feature_equity_with_manasight.md
- src/mythic_edge_parser/app/golden_replay.py
- src/mythic_edge_parser/app/parser_diagnostics.py
- src/mythic_edge_parser/app/feature_equity_corpus_ratchet.py
- src/mythic_edge_parser/app/evidence_ledger.py
- tests/fixtures/golden_replay/*.manifest.json
- tests/fixtures/feature_equity_corpus/feature_equity_corpus_baseline.v1.json

External reference inspected:

- Manasight corpus repository metadata, README, smoke corpus manifest, and
  sessions ledger were inspected as public category/reference material only.
  This contract does not import, copy, mirror, or authorize committing
  Manasight logs, parser source, compressed corpus files, raw session records,
  or full external manifest contents.

## Purpose

Issue #291 defines the first Mythic Edge corpus parity module under tracker
#158. The goal is to create a durable corpus manifest, session-ledger, scenario
taxonomy, and compatibility-report standard so future work can compare Mythic
Edge reliability coverage against Manasight-style scenario families.

Plain English: Mythic Edge needs to know which parser situations its committed
safe corpus covers, which situations are local/private report-only, and which
external scenario families are still gaps. That coverage evidence should help
humans choose future fixtures and tests. It must not become parser truth, a
second parser, a baseline auto-blesser, a merge/deploy gate, gameplay advice,
or a route for private or external logs into the repository.

## Scope Decision

Implementation should proceed as a metadata and report scaffold.

Codex C may implement:

- a Mythic Edge corpus manifest schema;
- a session-ledger schema or template;
- a compatibility report builder over committed Mythic Edge fixture metadata;
- focused tests for manifest validation, taxonomy mapping, report vocabulary,
  and privacy/protected-surface behavior;
- a comparison handoff document.

Codex C must not implement parser behavior changes, add private/external logs,
import Manasight corpus files, copy Manasight parser source, or make corpus
coverage counts authoritative.

V1 should use existing committed Mythic Edge fixture and report surfaces. It
does not need to add new log fixtures in the first implementation. If Codex C
finds that a sample fixture is required, it must be synthetic or already
sanitized, minimal, and authorized by the golden replay fixture rules.

## Owning Layer

Owning layer: parser reliability / corpus evidence metadata.

Supporting layers:

- golden replay for committed fixture execution;
- parser diagnostics for local parser-health evidence;
- feature-equity corpus ratchet for count-shaped parser-family coverage;
- Player.log evidence ledger for provenance vocabulary;
- future analytics or local app surfaces as downstream consumers only.

Truth boundary:

- Parser modules, router dispatch, event classes, and parser state remain the
  owners of parser interpretation and match/game facts.
- Golden replay owns replaying committed fixtures through the normal parser
  path and comparing parser-owned outputs to expected manifests.
- Feature-equity corpus ratchet owns count-shaped report-only coverage over
  explicit golden replay manifests.
- The corpus parity module owns taxonomy, manifest metadata, session metadata,
  compatibility reports, coverage-gap labels, and fixture acceptance policy.
- External corpus materials are reference categories only.
- Analytics, Match Journal, local app UI, workbook formulas, Google Sheets,
  Apps Script, webhooks, OpenAI/model-provider behavior, and AI/coaching output
  remain downstream or out of scope.

This module must not become:

- a parser;
- parser state;
- parser final reconciliation;
- match identity, game identity, or deduplication logic;
- workbook schema or webhook payload shape;
- Apps Script, Google Sheets, local app, Match Journal, overlay, or SQLite
  behavior;
- analytics truth, AI truth, gameplay advice, hidden-card inference,
  archetype classification, player-mistake labeling, best-line truth, merge
  readiness, deploy readiness, public-release readiness, or tracker-completion
  authority.

## Files Owned By This Contract

Contract artifact:

- docs/contracts/parser_corpus_parity_expansion.md

Future implementation artifacts authorized by this contract:

- src/mythic_edge_parser/app/corpus_parity_report.py
- tests/test_corpus_parity_report.py
- docs/templates/parser_corpus_session.md
- tests/fixtures/parser_corpus/corpus_manifest.v1.json
- tests/fixtures/parser_corpus/session_ledger.v1.json
- docs/implementation_handoffs/parser_corpus_parity_expansion_comparison.md
- docs/contract_test_reports/parser_corpus_parity_expansion.md

Protected-surface authorization: Authorized drift - workflow_authority_docs -
docs/templates/parser_corpus_session.md - issue #291 and
docs/contracts/parser_corpus_parity_expansion.md.

Existing files that may be read or consumed without changing their semantics:

- src/mythic_edge_parser/app/golden_replay.py
- src/mythic_edge_parser/app/parser_diagnostics.py
- src/mythic_edge_parser/app/feature_equity_corpus_ratchet.py
- src/mythic_edge_parser/app/evidence_ledger.py
- tests/fixtures/golden_replay/*.manifest.json
- tests/fixtures/feature_equity_corpus/feature_equity_corpus_baseline.v1.json
- docs/contracts/parser_golden_replay_harness.md
- docs/contracts/parser_diagnostics_mode.md
- docs/contracts/parser_feature_equity_corpus_ratchet.md
- docs/contracts/player_log_evidence_ledger.md

Not owned by this contract:

- parser modules;
- parser event classes;
- parser state final reconciliation;
- match/game identity or deduplication;
- workbook schema, exports, formulas, or Google Sheets sync;
- webhook payloads or delivery;
- Apps Script;
- local app behavior;
- Match Journal behavior;
- SQLite schema, migrations, or ingest;
- generated runtime artifacts;
- private/local logs or private app-data;
- AI/model-provider behavior.

## Observed Current Behavior

Observed from current main at
`9cb5f5b9805f530edad827378d14bf3b373b526d`:

- Tracker #158 is open for corpus parity and expansion planning.
- Issue #291 is open as the first corpus parity contract child issue.
- Golden replay exists as a committed-fixture harness with explicit manifest
  inputs, normal parser-path execution, report statuses `pass`, `degraded`,
  `review`, `diff`, and `fail`, and privacy checks for unsafe fixture content.
- Current committed golden replay manifests cover:
  - sanitized Bo1 match win fixture;
  - sanitized Bo3 sideboard match loss fixture;
  - synthetic draft parser-family fixture.
- Feature-equity corpus ratchet exists as a report-only count ratchet over
  explicit golden replay manifests. It consumes committed manifests, compares
  count-shaped observations to a baseline, and does not decide parser truth or
  merge readiness.
- The current feature-equity baseline covers three manifest inputs and counts
  parser event families, parser claim families, GameState evidence families,
  truncation/data-loss indicators, and unknown/degradation counters.
- Parser diagnostics exists as a local observer/report harness and separates
  parser-health evidence from transport/workbook/App Script truth.
- The Player.log evidence ledger exists as provenance metadata and review
  vocabulary. It does not own parser facts.
- There is not yet a durable corpus-level manifest or session-ledger standard
  for scenario-family coverage.
- There is not yet a compatibility report standard that maps Mythic Edge
  committed/local coverage to external Manasight-style scenario categories.

Observed from the external Manasight corpus reference material:

- The external corpus organizes sanitized compressed log captures with manifest
  metadata and human-readable session notes.
- Its scenario categories include standard Bo1/Bo3, limited draft/sealed
  sessions, log rotation, detailed-log disabled states, connection/reconnect
  cases, timer/inactivity cases, deck/economy/API surfaces, gameplay mechanics
  stress cases, and drift/debug regression cases.
- Those categories are useful reference taxonomy inputs, but their logs,
  compressed files, hashes, raw filenames, session rows, and parser source are
  not Mythic Edge artifacts and must not be copied into this repository.

## Required Guarantees

### Manifest Purpose

The Mythic Edge corpus manifest must describe committed Mythic Edge reliability
fixtures and reference reports. It must not execute parser logic by itself.

V1 manifest entries should identify:

- fixture or report id;
- source kind;
- privacy class;
- commit status;
- sanitizer status;
- linked issue or contract;
- scenario families;
- parser event families;
- parser claim families;
- related golden replay manifests;
- related diagnostics or feature-equity reports, if any;
- known gaps;
- validation commands or report sources.

The manifest may reference existing committed golden replay manifests. It must
not duplicate full expected parser outputs from golden replay manifests unless
a later contract explicitly authorizes that duplication.

### Session Ledger Purpose

The session ledger must provide human-readable and machine-readable session
metadata for corpus planning. It should help reviewers answer:

- What scenario does this fixture/session represent?
- Is it committed, synthetic, sanitized, local-private report-only, or external
  reference only?
- Which parser surfaces does it exercise?
- Which coverage gaps or degraded states are expected?
- Which future issue should expand this coverage?

The session ledger must not contain raw log lines, raw payloads, full private
decklists, private paths, credentials, webhook URLs, failed delivery artifacts,
runtime-state artifacts, generated databases, workbook exports, or private
app-data.

### Compatibility Report Purpose

The compatibility report must compare Mythic Edge coverage categories against
Manasight-style scenario families at category level.

It may say:

- a category is covered by committed Mythic Edge fixtures;
- a category is covered only by synthetic fixtures;
- a category is represented only by local/private report-only evidence;
- a category is partially covered;
- a category is missing;
- a category is deferred or blocked by privacy/external-boundary constraints.

It must not say:

- Mythic Edge is semantically equivalent to Manasight overall;
- Manasight logs or parser source have been imported;
- a category count proves parser correctness;
- a coverage gap should be closed by committing private or external logs;
- a report status decides merge readiness, deploy readiness, public-release
  readiness, tracker completion, parser truth, analytics truth, AI truth, or
  gameplay advice.

### External Reference Boundary

Allowed external-reference inputs:

- public repository URL;
- repository name;
- default branch name;
- observed pushed/inspection timestamp;
- category names and scenario-family summaries;
- README-level corpus policy summaries;
- high-level manifest/session schema concepts.

Forbidden external-reference inputs:

- external log files;
- external compressed log files;
- external parser source code;
- raw external session payloads;
- a wholesale copy of external manifest file rows;
- a wholesale copy of external session ledger rows;
- external file hashes, byte sizes, or capture dates as Mythic Edge canonical
  data;
- any external corpus item treated as a committed Mythic Edge fixture.

If a future implementation needs an external reference list, it should store a
small category taxonomy with source URL and inspection date, not a mirror of
the external corpus manifest.

## Public Interface

V1 may expose a small local report API. Exact Python names may vary, but the
behavior must preserve this shape if implementation proceeds:

```python
def build_corpus_parity_report(
    manifest_path: Path,
    *,
    feature_equity_report: Mapping[str, Any] | None = None,
    external_reference: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    ...

def load_corpus_manifest(path: Path) -> dict[str, Any]:
    ...

def validate_corpus_manifest(payload: Mapping[str, Any]) -> list[str]:
    ...

def main(argv: Sequence[str] | None = None) -> int:
    ...
```

CLI expectations:

- A local module entrypoint may be added, for example
  `python3 -m mythic_edge_parser.app.corpus_parity_report`.
- Inputs must be explicit paths to committed manifest/session metadata or
  explicit local report files.
- Generated reports must be local review artifacts by default.
- The CLI must not read private local logs implicitly.
- The CLI must not fetch external corpora, clone external repos, download
  compressed logs, or call AI/model providers.
- The CLI must not add or change environment-variable contracts.

## Corpus Manifest Schema

Required top-level logical shape:

```yaml
object: "mythic_edge_parser_corpus_manifest"
schema_version: "parser_corpus_manifest.v1"
corpus_id: "mythic_edge_parser_reliability_corpus_v1"
source_privacy:
  raw_private_log_committed: false
  external_logs_committed: false
  local_private_artifacts_committed: false
entries:
  - corpus_entry
taxonomy:
  scenario_family_version: "parser_corpus_scenario_family.v1"
  families:
    - scenario_family
```

Required `corpus_entry` fields:

```yaml
entry_id: "bo1_match_win_basic"
entry_type: "golden_replay_manifest"
source_kind: "sanitized_committed_fixture"
commit_status: "committed"
privacy_class: "sanitized_committable"
sanitization_status: "sanitized"
linked_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/48"
authorized_by_contract: "docs/contracts/parser_golden_replay_harness.md"
paths:
  golden_replay_manifest: "tests/fixtures/golden_replay/bo1_match_win_basic.manifest.json"
scenario_families:
  - "core_gameplay.standard_bo1"
parser_event_families:
  - "Rank"
  - "MatchState"
  - "ClientAction"
  - "GameState"
  - "GameResult"
parser_claim_families:
  - "rank_context"
  - "match_lifecycle"
  - "client_action"
  - "game_state"
  - "game_result"
  - "final_reconciliation"
coverage_status: "covered_committed"
known_gaps: []
review_notes: []
```

Allowed `entry_type` values:

- `golden_replay_manifest`
- `feature_equity_report`
- `diagnostics_report`
- `session_ledger_entry`
- `external_reference_category`
- `local_private_report_summary`

Allowed `source_kind` values:

- `sanitized_committed_fixture`
- `synthetic_committed_fixture`
- `committed_count_only_report`
- `local_private_report_only`
- `external_reference_only`

Allowed `commit_status` values:

- `committed`
- `local_report_only`
- `external_reference_only`
- `deferred`

Allowed `privacy_class` values:

- `sanitized_committable`
- `synthetic_committable`
- `committed_count_only`
- `local_private_not_committed`
- `external_reference_metadata_only`

Allowed `sanitization_status` values:

- `sanitized`
- `synthetic`
- `not_applicable_count_only`
- `not_applicable_external_reference`
- `requires_review`

`requires_review` entries must not be committed as fixture entries. They may
exist only as proposed local metadata in uncommitted review output or in a
contract-test report describing why implementation stopped.

## Session Ledger Schema

The session ledger may be JSON for machine validation, Markdown for human
review, or both. If both exist, the machine-readable JSON owns validation
fields and Markdown owns explanatory prose.

Required logical shape:

```yaml
object: "mythic_edge_parser_corpus_session_ledger"
schema_version: "parser_corpus_session_ledger.v1"
sessions:
  - session_entry
```

Required `session_entry` fields:

```yaml
session_id: "standard_bo3_sideboard_loss_v1"
title: "Sanitized Standard Bo3 sideboard match loss"
source_kind: "sanitized_committed_fixture"
commit_status: "committed"
privacy_class: "sanitized_committable"
scenario_families:
  - "core_gameplay.standard_bo3"
  - "core_gameplay.sideboarding_signal"
format_family: "constructed_standard"
match_shape: "best_of_three"
record_summary: "redacted_or_synthetic_summary"
parser_coverage:
  event_families:
    MatchState: 1
    GameState: 4
    GameResult: 2
  unknown_entries: 0
  truncation_count: 0
game_rows:
  count: 2
  result_shape: "win_loss"
known_gaps: []
report_only_redactions:
  raw_log_lines_included: false
  private_paths_included: false
  raw_payloads_included: false
```

The session ledger may include exact parser counts for committed safe fixtures.
For local/private report-only sessions, it may include redacted counts and
labels only. It must not include raw lines, raw payload objects, private
filenames, local paths, account identifiers, opponent identifiers, or full
decklists.

## Scenario Taxonomy

The V1 taxonomy should use stable dot-separated family ids. Initial family ids
authorized by this contract:

- `manifest.metadata`
- `session.ledger_metadata`
- `core_gameplay.standard_bo1`
- `core_gameplay.standard_bo3`
- `core_gameplay.traditional_bo3`
- `core_gameplay.draft_with_games`
- `core_gameplay.draft_only`
- `core_gameplay.sealed_entry`
- `core_gameplay.sealed_deckbuild`
- `core_gameplay.sealed_matches`
- `log_runtime.detailed_logs_disabled`
- `log_runtime.rotation`
- `log_runtime.malformed_or_headerless`
- `log_runtime.timestamp_anomaly`
- `log_runtime.unknown_entry`
- `connection.reconnect`
- `connection.disconnect`
- `connection.firewall_or_network_drop`
- `connection.connection_error_payload`
- `timer.active_player_timer`
- `timer.inactivity_timeout`
- `timer.pre_match_idle`
- `deck_api.start_hook_deck_snapshot`
- `deck_api.deck_summary`
- `deck_api.deck_upsert`
- `deck_api.event_set_deck`
- `deck_api.store_pack_inbox_or_crafting`
- `gameplay_stress.mulligan`
- `gameplay_stress.opponent_auto_concede`
- `gameplay_stress.conjure`
- `gameplay_stress.spellbook`
- `gameplay_stress.companion_or_large_deck`
- `gameplay_stress.action_attribution`
- `gameplay_stress.event_ordering`
- `drift_debug.gsm_truncation`
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

Coverage status values:

- `covered_committed`
- `covered_synthetic`
- `covered_report_only`
- `partial`
- `missing`
- `deferred`
- `blocked_private_evidence`
- `blocked_external_boundary`
- `not_applicable`

Coverage basis values:

- `parser_behavior_verified`
- `fixture_metadata_only`
- `diagnostics_only`
- `count_ratchet_only`
- `evidence_ledger_only`
- `local_report_only`
- `external_reference_only`

## Compatibility Report Schema

Required top-level logical shape:

```yaml
object: "mythic_edge_parser_corpus_compatibility_report"
schema_version: "parser_corpus_compatibility_report.v1"
status: "partial_coverage_map_ready"
status_reasons: []
inputs:
  corpus_manifest_path: "tests/fixtures/parser_corpus/corpus_manifest.v1.json"
  session_ledger_path: "tests/fixtures/parser_corpus/session_ledger.v1.json"
  feature_equity_report_supplied: false
  external_reference:
    source: "manasight-corpus"
    source_url: "https://github.com/manasight/manasight-corpus"
    usage: "category_reference_only"
summary:
  total_scenario_families: 0
  covered_committed: 0
  covered_synthetic: 0
  covered_report_only: 0
  partial: 0
  missing: 0
  deferred: 0
coverage_matrix:
  - scenario_family_result
gaps:
  - gap_record
privacy:
  raw_private_log_committed: false
  external_logs_committed: false
  raw_log_lines_in_report: false
  local_absolute_paths_redacted: true
protected_surfaces:
  parser_behavior_changed: false
  workbook_schema_changed: false
  webhook_payload_shape_changed: false
  apps_script_behavior_changed: false
limitations: []
```

Allowed report `status` values:

- `coverage_map_ready`
- `partial_coverage_map_ready`
- `review`
- `blocked_private_artifact_risk`
- `blocked_external_boundary`
- `fail`

Required `scenario_family_result` fields:

```yaml
scenario_family: "core_gameplay.standard_bo1"
coverage_status: "covered_committed"
coverage_basis:
  - "parser_behavior_verified"
mythic_edge_entries:
  - "bo1_match_win_basic"
external_reference_status: "reference_category_present"
notes: []
```

Allowed `external_reference_status` values:

- `reference_category_present`
- `reference_category_not_checked`
- `reference_not_applicable`

Required `gap_record` fields:

```yaml
scenario_family: "connection.reconnect"
gap_status: "missing"
risk_tier: "High"
recommended_next_step: "Codex A problem representation or Codex B follow-up contract"
blocked_by:
  - "no_committed_safe_fixture"
  - "private_evidence_required"
```

## Fixture And Artifact Rules

Committed fixture rules:

- Only sanitized committed fixtures and synthetic committed fixtures are
  allowed.
- Fixture entries must be minimal and tied to a contract and issue.
- Any committed log-like fixture must pass existing golden replay privacy
  checks and repo secret/private-marker checks.
- A fixture must not be added solely to make external category counts look
  better.
- No Manasight log, Manasight compressed log, private local log, failed
  delivery artifact, runtime-state artifact, generated database, workbook
  export, private JSON/JSONL artifact, private app-data, secret, credential,
  token, API key, or webhook URL may be committed.

Local/private report-only rules:

- Local private logs may be used only through explicit user-approved local
  report runs.
- Local/private reports must redact local paths and private identifiers.
- Local/private reports must not include raw log lines or raw payload objects.
- Local/private report summaries may be represented in compatibility reports
  only as redacted counts, scenario labels, and review notes.
- Local/private report-only coverage must use `covered_report_only` or
  `blocked_private_evidence`; it must not be upgraded to
  `covered_committed`.

External reference rules:

- External corpus materials may inform category names and gap framing.
- External logs, compressed logs, parser source, and full manifest/session
  copies are forbidden.
- External category coverage must use `external_reference_only` as a basis
  unless Mythic Edge has its own committed or local report-only evidence.

## Unknowns And Suspected Gaps

Unknowns:

- Whether Mythic Edge should use JSON, Markdown, or both for the first session
  ledger artifact.
- Whether the first implementation should include a CLI or only schema
  validation helpers.
- Whether future corpus expansion should add new synthetic fixtures before any
  additional sanitized real-log fixtures.
- Whether local/private live-log report-only evidence should be summarized in
  committed reports or kept entirely out of committed artifacts until a later
  privacy contract.

Suspected gaps:

- Current committed corpus appears much smaller than the external reference
  scenario family list.
- Connection/reconnect, log rotation, detailed-log disabled, timer/inactivity,
  deck/economy/API, Conjure, Spellbook, companion/large-deck, and several
  drift/debug regression families likely do not have committed Mythic Edge
  fixtures yet.
- Feature-equity coverage counts do not prove semantic correctness.
- Some categories may need future parser contracts before a fixture can safely
  become a golden replay oracle.
- Report-only local/private evidence could be overread as support coverage if
  the compatibility report does not clearly label it.

## Validation Obligations

Codex B validation:

- docs-only validation is sufficient;
- verify branch/status;
- run diff hygiene and targeted doc/protected-surface checks if available.

Codex C implementation validation should include:

- `python3 -m pytest -q tests/test_corpus_parity_report.py`
- `python3 -m pytest -q tests/test_golden_replay_harness.py tests/test_feature_equity_corpus_ratchet.py`
- `python3 -m ruff check src tests tools`
- `python3 tools/check_agent_docs.py`
- `git diff --name-only origin/main...HEAD | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin`
- `git diff --name-only origin/main...HEAD | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin`
- `git diff --name-only origin/main...HEAD | python3 tools/select_validation.py --base origin/main --paths-from-stdin`
- `git diff --check`

Codex E review should verify:

- no external or private log artifacts were added;
- no generated/private/local artifacts were committed;
- no parser behavior or protected surface changed;
- compatibility report labels cannot be mistaken for parser truth, merge
  readiness, deploy readiness, public-release readiness, analytics truth, AI
  truth, or gameplay advice;
- external Manasight material is category/reference-only and not mirrored.

## Acceptance Criteria

The contract is implementable when Codex C can produce:

- a machine-readable corpus manifest with validation;
- a machine-readable or templated session ledger;
- a compatibility report with stable status vocabulary;
- tests covering accepted source kinds, rejected private/external artifact
  shapes, scenario taxonomy mapping, and protected-surface assertions;
- no parser behavior changes;
- no private/external corpus imports;
- no generated/local/private artifact commits;
- a clear implementation handoff.

## Stop Conditions

Stop and route back to Codex B or Codex A if:

- implementing the report requires changing parser behavior;
- a scenario category cannot be represented without importing external logs;
- a fixture contains raw or questionably sanitized private evidence;
- a report would need to include raw log lines, raw payload objects, private
  paths, or private decklists;
- external corpus files, external parser source, or full external manifest rows
  are needed;
- compatibility labels would be used as parser truth, analytics truth,
  gameplay advice, merge readiness, deploy readiness, public-release readiness,
  or tracker completion;
- a protected surface change appears necessary.

## Codex C Handoff Prompt

```yaml
prompt: |
  Use the Mythic Edge agent constitution.
  Use $mythic-edge-workflow.

  Act as Codex C: Module Implementer for issue #291, the first corpus parity
  module under tracker #158.

  Issue:
  https://github.com/Tahjali11/Mythic-Edge/issues/291

  Tracker:
  https://github.com/Tahjali11/Mythic-Edge/issues/158

  Branch:
  codex/parser-corpus-parity-expansion

  Base:
  main at 9cb5f5b9805f530edad827378d14bf3b373b526d

  Contract:
  docs/contracts/parser_corpus_parity_expansion.md

  Goal:
  Implement the smallest metadata/report scaffold needed to satisfy the corpus
  parity expansion contract. Preserve existing parser behavior and existing
  report semantics.

  Do:
    - Compare current repo behavior to the contract before editing.
    - Add a corpus manifest and session-ledger schema or template.
    - Add a compatibility report helper or CLI only if it can remain
      report-only and deterministic.
    - Add focused tests for schema validation, taxonomy mapping, report
      vocabulary, privacy boundaries, and protected-surface assertions.
    - Use existing golden replay, diagnostics, feature-equity, and
      evidence-ledger surfaces as inputs without changing their truth
      semantics.
    - Produce docs/implementation_handoffs/parser_corpus_parity_expansion_comparison.md.

  Do not:
    - Implement parser behavior changes.
    - Import or commit Manasight logs.
    - Copy Manasight parser source code.
    - Copy raw private Player.log excerpts into repo files or GitHub issues.
    - Commit local private logs, failed delivery artifacts, runtime-state
      artifacts, generated data, workbook exports, SQLite databases, secrets,
      credentials, tokens, API keys, webhook URLs, generated card/tier data, or
      private local app-data contents.
    - Change parser state final reconciliation, parser event classes,
      match/game identity, deduplication, workbook schema, webhook payload
      shape, Apps Script behavior, Google Sheets sync, output transport,
      production behavior, OpenAI/model-provider behavior, AI/coaching behavior,
      local app behavior, Match Journal behavior, SQLite schema, migrations,
      ingest, or analytics truth.
    - Make corpus reports decide parser truth, merge readiness, deploy
      readiness, tracker completion, gameplay advice, hidden-card inference,
      archetype classification, player mistakes, or best-line truth.
    - Stage or commit unless explicitly asked.

  Validation:
    - python3 -m pytest -q tests/test_corpus_parity_report.py
    - python3 -m pytest -q tests/test_golden_replay_harness.py tests/test_feature_equity_corpus_ratchet.py
    - python3 -m ruff check src tests tools
    - python3 tools/check_agent_docs.py
    - git diff --name-only origin/main...HEAD | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
    - git diff --name-only origin/main...HEAD | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
    - git diff --name-only origin/main...HEAD | python3 tools/select_validation.py --base origin/main --paths-from-stdin
    - git diff --check
```

## Workflow Handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/291"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  completed_thread: "B"
  next_thread: "C"
  source_artifact: "docs/contracts/parser_corpus_parity_expansion.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_parity_expansion_comparison.md"
  verdict: "contract_ready_for_metadata_report_scaffold_implementation"
  risk_tier: "High"
  branch: "codex/parser-corpus-parity-expansion"
  base_commit: "9cb5f5b9805f530edad827378d14bf3b373b526d"
  validation:
    - "Codex B docs-only validation expected."
    - "Codex C should run focused corpus parity, golden replay, feature-equity, ruff, agent-doc, secret-pattern, protected-surface, selector, and diff checks."
  stop_conditions:
    - "Do not implement parser behavior changes."
    - "Do not import or commit Manasight logs or copy Manasight parser source code."
    - "Do not copy raw private Player.log excerpts into repo files or GitHub issues."
    - "Do not commit local private logs, failed delivery artifacts, runtime-state artifacts, generated data, workbook exports, SQLite databases, secrets, credentials, tokens, API keys, webhook URLs, generated card/tier data, or private local app-data contents."
    - "Do not change parser state final reconciliation, parser event classes, match/game identity, deduplication, workbook schema, webhook payload shape, Apps Script behavior, Google Sheets sync, output transport, production behavior, OpenAI/model-provider behavior, AI/coaching behavior, local app behavior, Match Journal behavior, SQLite schema, migrations, ingest, or analytics truth."
    - "Do not make corpus reports decide parser truth, merge readiness, deploy readiness, tracker completion, gameplay advice, hidden-card inference, archetype classification, player mistakes, or best-line truth."
```
