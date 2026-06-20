# Parser Evidence Local Harvest Candidate Reports Contract

## Module

Planning-only contract for issue #382, the local harvest candidate report
boundary in the parser evidence-pipeline lane.

Plain English: this contract defines how a future Mythic Edge harvest tool may
describe candidate parser-evidence windows and scenario-family opportunities
without reading private logs in this contract pass, promoting fixtures,
changing parser behavior, or claiming parser/readiness truth.

This Codex B pass does not implement code, activate #382 for implementation,
run or read private logs, create fixtures, promote corpus rows, or claim
parser behavior readiness.

## Source Issue

- Repository: `Tahjali11/Mythic-Edge`
- Repository URL: `https://github.com/Tahjali11/Mythic-Edge`
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/382
- Pipeline tracker: https://github.com/Tahjali11/Mythic-Edge/issues/388
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/381
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/520
- Parent private-evidence issue: https://github.com/Tahjali11/Mythic-Edge/issues/434
- Base branch: `main`
- Target branch: `main`
- Risk tier: High
- Previous merge commit: `34631ed7f67702aa6d96791d74506a72b1bba24f`

Observed during this Codex B pass:

- Operating checkout remote matches
  `https://github.com/Tahjali11/Mythic-Edge.git`.
- `main` is up to date with `origin/main`.
- `HEAD` is `34631ed7f67702aa6d96791d74506a72b1bba24f`.
- Issue #381 is closed.
- PR #520 is merged.
- Tracker #388 is open and inactive.
- Parent private-evidence issue #434 is open.
- Issue #382 is open and still contains stale all-45 coverage start-condition
  wording. The latest #382 comment routes this issue to Codex B for
  planning-only contract work and explicitly preserves non-activation.

Current readiness facts to preserve:

```yaml
parser_behavior_ready: false
pipeline_activation_ready_for_issue_388: false
report_preconditions_ready_for_issue_388: true
evidence_pipeline_planning_ready_for_issue_388: false
implementation_authorized: false
private_harvest_authorized: false
fixture_promotion_authorized: false
```

## Source Artifacts Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- Issue #382 and its latest Codex A comment
- Tracker #388
- Parent private-evidence issue #434
- Issue #381 and PR #520
- `docs/contracts/parser_evidence_pipeline_planning_umbrella.md`
- `docs/contracts/parser_evidence_utc_log_source_adapter.md`
- `docs/implementation_handoffs/parser_evidence_utc_log_source_adapter_comparison.md`
- `docs/contracts/parser_diagnostics_mode.md`
- `docs/contracts/parser_golden_replay_harness.md`
- `docs/contracts/parser_corpus_private_evidence_window_offset_capture.md`
- `docs/local_artifacts_manifest.json`
- `src/mythic_edge_parser/app/utc_log_source_adapter.py`
- `src/mythic_edge_parser/app/parser_diagnostics.py`
- `src/mythic_edge_parser/app/log_drift_sensor.py`
- focused diagnostics, drift, UTC_Log adapter, and evidence-pipeline tests by
  inspection where relevant

## Observed Current Behavior

The repository now has a synthetic-only `UTC_Log` source adapter boundary:

- `normalize_utc_log_text()` accepts synthetic `UTC_Log`-style text, strips
  UTC frame prefixes, reports normalization stats, and returns
  `Player.log`-equivalent text.
- `describe_user_selected_utc_log_candidate()` fails closed for private/local
  candidate discovery.
- The adapter does not inspect private paths, read private `UTC_Log` files,
  produce local harvest reports, create fixtures, or promote corpus rows.

Existing diagnostics and drift surfaces can produce report-like evidence from
explicit log paths, but those are independent observer/reporting tools. They
must not be silently turned into a harvest pipeline, fixture promotion tool,
private-log reader, or parser truth owner by this contract.

There is no dedicated local harvest candidate report module, CLI, schema, test
fixture, or committed report artifact for issue #382.

## Problem

Issue #382 is the first point where the parser evidence pipeline wants to
identify useful evidence windows before fixture promotion. This is helpful but
high risk because candidate reports sit near:

- raw private `Player.log` or `UTC_Log` content;
- local source selection and windowing;
- diagnostics and drift summaries;
- parser-owned event and state facts;
- corpus scenario-family coverage decisions;
- later review packets and fixture-promotion proof.

Without a contract, a future implementation could accidentally:

- read private logs without approval;
- print exact private paths, hashes, offsets, sizes, or source fragments;
- treat candidate scoring as parser truth or fixture truth;
- bypass the #381 UTC_Log normalization boundary;
- promote blocked, report-only, private-evidence, or external-boundary rows;
- infer hidden information or deck facts from incomplete evidence;
- claim #388 activation, parser behavior readiness, release readiness, or full
  corpus parity from candidate metadata alone.

## Scope Decision

This contract approves a planning boundary only.

Codex C implementation is not authorized by this contract. The next workflow
step should be a lifecycle/activation decision after this contract is reviewed
or accepted. A later implementation requires an explicit user prompt or
Codex A/G activation that names the exact implementation scope and confirms
whether it is synthetic-only, local-only private, or deferred.

This contract defines:

- future public interfaces in logical form;
- accepted and forbidden input classes;
- report shape and vocabulary;
- private pointer boundaries;
- parser fact preview limits;
- validation expectations for a later implementation pass, if separately
  authorized.

This contract does not authorize:

- code implementation;
- private source reads;
- private harvest execution;
- local app-data discovery;
- fixture creation or promotion;
- corpus status changes;
- parser behavior changes;
- #388 or #381 activation;
- `parser_behavior_ready=true`;
- `pipeline_activation_ready_for_issue_388=true`.

## Owning Layer

Owning layer: Corpus / Provenance, with Parser Reliability support.

Corpus / Provenance owns candidate report vocabulary, scenario-family mapping
metadata, local-only artifact boundaries, and review handoff concepts.

Parser Reliability owns diagnostics, drift summaries, truncation/data-loss
reporting, and existing parser evidence surfaces consumed by a future report.

Parser owns event interpretation, routing semantics, parser events, parser
state, match/game identity, deduplication, and final reconciliation.

Generated / Local Artifacts owns any future local-only source pointers,
candidate reports, parser fact previews, private pointers, offset-window
metadata, private review packets, or draft fixture packets.

Quality / Governance owns role routing, issue activation, protected-surface
checks, private-evidence gates, and review requirements.

## Truth Boundary

Harvest candidate reports are advisory evidence-discovery artifacts.

They may say:

- a local or synthetic source appears worth human review;
- a window appears related to one or more scenario families;
- a parser/diagnostics/drift surface produced reduced counts or labels;
- a candidate has coverage value, confidence, duplication risk, and privacy
  risk;
- a candidate is blocked, duplicate-likely, insufficient, or local-review-only.

They must not say:

- parser behavior is verified;
- a fixture should be promoted;
- a corpus row should change status;
- a private source proves parser support;
- an unknown entry's semantic meaning is understood;
- a hidden card, decklist, archetype, gameplay mistake, or coaching conclusion
  is known;
- #388, #381, release, production, analytics, AI, or coaching readiness is
  achieved.

Candidate reports are not parser truth, fixture truth, workbook truth, runtime
truth, analytics truth, AI truth, merge readiness, deploy readiness, release
readiness, production truth, or tracker-completion evidence.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/parser_evidence_local_harvest_candidate_reports.md`

Expected future review artifact, if this contract is submitted for review:

- `docs/contract_test_reports/parser_evidence_local_harvest_candidate_reports.md`

Potential future implementation artifacts, not authorized by this contract:

- `src/mythic_edge_parser/app/local_harvest_candidate_reports.py`
- `tests/test_local_harvest_candidate_reports.py`
- `docs/implementation_handoffs/parser_evidence_local_harvest_candidate_reports_comparison.md`

Potential future local-only generated artifacts, not committed:

- `candidate_summary.json`
- `candidate_summary.md`
- `parser_fact_preview.json`
- `private_pointer.json`

## Public Interface Boundary

No public runtime interface is approved in this contract.

If later activated, the smallest acceptable public module interface should be a
pure report builder over already supplied in-memory or explicit synthetic
inputs. It should not discover files, traverse private directories, read
default local logs, tail live sources, or mutate artifacts by default.

Logical future interface:

```python
build_harvest_candidate_report(
    *,
    source_label: str,
    source_kind: str,
    privacy_class: str,
    parser_evidence: Mapping[str, Any],
    diagnostics_summary: Mapping[str, Any] | None = None,
    drift_summary: Mapping[str, Any] | None = None,
    scenario_family_hints: Sequence[str] = (),
) -> Mapping[str, Any]
```

Any future file-writing helper must require an explicit output path and must
default to ignored local artifact locations, never to committed fixture or docs
paths.

## Accepted Input Classes

Approved for contract discussion:

- synthetic `Player.log`-style strings supplied by a focused test;
- synthetic `UTC_Log`-style strings normalized by the #381 adapter;
- synthetic parser/diagnostics/drift summary dictionaries with no raw payloads;
- committed sanitized fixtures already approved by separate contracts, when a
  future issue explicitly names them;
- public corpus scenario-family IDs and statuses from committed corpus metadata.

Potential future input classes requiring separate activation:

- user-selected private `Player.log` source;
- user-selected private normalized `UTC_Log` source;
- local-only offset-window metadata created under an approved private-evidence
  window contract;
- local diagnostics or drift reports generated from private evidence;
- operator-authored private incident notes.

The latter class may be used only in local-only execution packets with explicit
user approval and a scoped private-evidence contract. It is not authorized by
this contract.

## Forbidden Inputs

A #382 contract, implementation, test, report, or public artifact must not
read, include, summarize, hash, copy, or commit:

- raw private `Player.log` content;
- raw private `UTC_Log` content;
- raw log lines or raw JSON payload bodies;
- exact private paths;
- raw source hashes;
- exact private file offsets, sizes, or byte ranges in public artifacts;
- app-data contents;
- live MTGA, network, firewall/drop, packet, OS/router, or private smoke data;
- runtime status files from a real run;
- failed posts;
- workbook exports;
- generated SQLite databases;
- decklists, sealed pools, draft picks, strategy notes, card choices, or
  private reports;
- secrets, credentials, tokens, API keys, webhook URLs, or screenshots.

## Player.log And UTC_Log Source Policy

There is no Player.log-only private bypass in this planning contract.

Future synthetic tests may use synthetic `Player.log`-style strings directly.
Future synthetic `UTC_Log` tests must use the #381 source adapter when they
need `Player.log`-equivalent text.

Future private `UTC_Log` source handling must go through the #381 adapter or a
later contract-authorized successor. Future private `Player.log` source
handling requires its own activation, local-only artifact rules, and private
evidence gate under #434.

No future implementation may silently fall back to default configured
`Player.log` paths. All local/private sources must be explicitly selected by
the operator under a scoped approval.

## Candidate Summary JSON Shape

If later implemented, `candidate_summary.json` must use this logical shape:

```yaml
object: "mythic_edge_harvest_candidate_summary"
schema_version: "parser_evidence_harvest_candidate_summary.v1"
report_id: "symbolic-public-safe-id"
created_at_utc: "ISO-8601 timestamp"
source:
  source_label: "symbolic-public-safe-label"
  source_kind: "synthetic_player_log|synthetic_utc_log|synthetic_normalized_utc_log|user_selected_player_log|user_selected_normalized_utc_log"
  privacy_class: "public_fixture|synthetic|private_local|local_only_redacted"
  source_adapter: "none|utc_log_source_adapter.v1"
  raw_source_committed: false
  raw_path_included: false
  raw_hash_included: false
  raw_content_included: false
authorization:
  authorization_status: "not_required_synthetic|missing_required|approved_local_only"
  authorization_issue: "GitHub issue URL or null"
  private_harvest_authorized: false
  fixture_promotion_authorized: false
summary:
  candidate_count: 0
  blocked_candidate_count: 0
  duplicate_likely_count: 0
  highest_privacy_risk: "none|low|medium|high|blocked"
  highest_coverage_value: "none|low|medium|high|critical_gap_candidate"
candidate_windows:
  - window_id: "symbolic-public-safe-id"
    window_label: "symbolic-public-safe-label"
    source_window_kind: "synthetic_line_range|synthetic_event_range|local_only_pointer|unavailable"
    public_location_included: false
    local_pointer_ref: "private_pointer.json#pointer_id or null"
    scenario_family_candidates: []
non_claims:
  parser_behavior_verified: false
  corpus_status_change_authorized: false
  fixture_promotion_authorized: false
  pipeline_activation_ready_for_issue_388: false
```

For committed synthetic tests, deterministic synthetic line or event indexes
may be included. For private/local runs, exact offsets, sizes, paths, hashes,
and raw line numbers must remain local-only or unavailable, according to the
future execution contract.

## Scenario Candidate Shape

Each `scenario_family_candidates` entry must use this logical shape:

```yaml
family_id: "corpus.family.id"
candidate_status: "candidate|review|blocked_private_evidence|blocked_external_boundary|duplicate_likely|insufficient_evidence|rejected"
evidence_status: "observed|derived|degraded|unknown|blocked"
coverage_value: "none|low|medium|high|critical_gap_candidate"
confidence: "unknown|low|medium|high"
duplication_risk: "unknown|low|medium|high"
privacy_risk: "none|low|medium|high|blocked"
parser_behavior_applicable: true
parser_behavior_verified: false
reasons:
  - "short public-safe reason code"
blocking_conditions:
  - "short public-safe blocker code"
related_contracts:
  - "docs/contracts/example.md"
```

`confidence` is confidence that the candidate is worth review, not confidence
that parser truth is correct.

`coverage_value` is estimated candidate value for evidence triage, not corpus
status and not readiness.

`parser_behavior_verified` must remain `false` unless a later implementation
contract explicitly authorizes behavior verification and focused validation
proves it.

## Candidate Summary Markdown Shape

If later implemented, `candidate_summary.md` must be a human-readable view of
the JSON report. It may include:

- report id and schema version;
- symbolic source label;
- source kind and privacy class;
- candidate table with family id, status, scoring vocabulary, and blockers;
- validation commands run;
- explicit non-claims.

It must not include:

- raw log excerpts;
- raw payload excerpts;
- exact private paths;
- raw hashes;
- exact private offsets or sizes;
- decklists or card choices;
- local-only private notes;
- readiness or truth claims beyond the report vocabulary.

## Parser Fact Preview Shape

If later implemented, `parser_fact_preview.json` must be reduced and
review-oriented:

```yaml
object: "mythic_edge_parser_fact_preview"
schema_version: "parser_evidence_parser_fact_preview.v1"
source_label: "symbolic-public-safe-label"
privacy_class: "public_fixture|synthetic|private_local|local_only_redacted"
preview_status: "available|degraded|blocked|unavailable"
raw_log_lines_included: false
raw_payloads_included: false
private_paths_included: false
event_counts:
  total: 0
event_kinds: []
diagnostics_summary:
  status: "pass|review|fail|unknown|unavailable"
drift_summary:
  status: "review|unknown|unavailable"
state_summary:
  included: false
  reason: "not_in_scope_for_v1"
```

Allowed preview content:

- event counts;
- event kind names;
- diagnostics status labels;
- unknown-entry counts and reduced signatures only when already sanitized by a
  future approved implementation;
- truncation/data-loss counts;
- corpus family hints.

Forbidden preview content:

- raw log lines;
- raw JSON payloads;
- private paths;
- raw hashes;
- exact private offsets or file sizes in public artifacts;
- private decklists, draft picks, sealed pools, or card-choice evidence;
- inferred hidden information;
- workbook rows as truth;
- AI or coaching analysis.

## Private Pointer Shape

If later authorized for local-only private evidence, `private_pointer.json`
must remain outside Git and must use symbolic labels by default:

```yaml
object: "mythic_edge_private_evidence_pointer"
schema_version: "parser_evidence_private_pointer.v1"
pointer_id: "symbolic-local-id"
source_label: "symbolic-public-safe-label"
source_kind: "user_selected_player_log|user_selected_normalized_utc_log"
privacy_class: "private_local"
raw_content_included: false
raw_path_included_in_public_artifacts: false
raw_hash_included_in_public_artifacts: false
retention_policy: "local_only_operator_controlled"
approved_window_ref: "local-only ref or null"
public_summary_ref: "candidate_summary.json#window_id or null"
```

This contract does not authorize creating `private_pointer.json`. It defines
the boundary for a later private-evidence execution contract.

## Malformed Or Partial Input Behavior

A future report builder must degrade safely:

- missing parser evidence produces `candidate_status=insufficient_evidence`;
- malformed summary dictionaries produce `preview_status=degraded` or
  `candidate_status=rejected`;
- private source authorization missing produces
  `authorization_status=missing_required`;
- forbidden content detected produces `candidate_status=rejected` or
  `privacy_risk=blocked`;
- unknown scenario-family hints must remain `unknown` or `review`, not
  auto-created corpus families.

The report builder must not attempt to reconstruct missing GameState data,
infer hidden cards, fill decklists, classify archetypes, label player mistakes,
or complete absent evidence.

## Relationship To Adjacent Modules

### UTC_Log Source Adapter

The #381 adapter is the required normalization boundary for synthetic
`UTC_Log`-style input and any future private `UTC_Log` source path. #382 must
not reimplement UTC prefix normalization or introduce a second `UTC_Log`
parser.

### Diagnostics Mode

Diagnostics reports are observer/acceptance artifacts. #382 may consume
reduced diagnostics summaries only under a future contract-authorized
implementation. Candidate scoring must not change diagnostics report semantics
or status vocabulary.

### Log Drift Sensor

Drift reports identify unknown or changed routing evidence. #382 may consume
sanitized drift summary fields in a future implementation, but it must not
claim unknown semantic meaning or automatic parser-gap issue creation.

### Golden Replay

Golden replay remains the deterministic fixture validation harness. #382 may
identify future fixture candidates, but it must not create, promote, or update
golden fixtures or expected manifests.

### Corpus Parity

Corpus parity metadata remains the committed coverage map. #382 may identify
candidate scenario families, but it must not change corpus manifest,
session-ledger, status, readiness metrics, or parser behavior flags.

### Private Evidence Gate

Issue #434 remains the parent private-evidence gate. Any private/local
execution needs a separate issue/contract, explicit source/window approval,
redaction rules, retention rules, and local-only artifact boundaries.

## Compatibility Expectations

Any future implementation must:

- preserve existing parser APIs and behavior;
- preserve existing diagnostics and drift report semantics;
- preserve existing corpus manifest and session-ledger status unless a
  separate contract authorizes metadata changes;
- keep reports deterministic for synthetic inputs;
- avoid environment-variable or credential changes;
- avoid CI, merge, deploy, release, production, workbook, webhook,
  Apps Script, Google Sheets, analytics, AI, and coaching behavior changes.

## Validation Obligations

This Codex B contract pass should validate documentation only:

```bash
python3 tools/check_agent_docs.py
git diff --check
printf 'docs/contracts/parser_evidence_local_harvest_candidate_reports.md\n' | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf 'docs/contracts/parser_evidence_local_harvest_candidate_reports.md\n' | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
printf 'docs/contracts/parser_evidence_local_harvest_candidate_reports.md\n' | python3 tools/select_validation.py --base origin/main --paths-from-stdin
```

If a future implementation is explicitly authorized, minimum focused
validation should include synthetic-only tests:

```bash
python3 -m pytest -q tests/test_utc_log_source_adapter.py tests/test_local_harvest_candidate_reports.py
python3 tools/check_agent_docs.py
git diff --check
printf 'src/mythic_edge_parser/app/local_harvest_candidate_reports.py\ntests/test_local_harvest_candidate_reports.py\ndocs/implementation_handoffs/parser_evidence_local_harvest_candidate_reports_comparison.md\n' | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf 'src/mythic_edge_parser/app/local_harvest_candidate_reports.py\ntests/test_local_harvest_candidate_reports.py\ndocs/implementation_handoffs/parser_evidence_local_harvest_candidate_reports_comparison.md\n' | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
printf 'src/mythic_edge_parser/app/local_harvest_candidate_reports.py\ntests/test_local_harvest_candidate_reports.py\ndocs/implementation_handoffs/parser_evidence_local_harvest_candidate_reports_comparison.md\n' | python3 tools/select_validation.py --base origin/main --paths-from-stdin
```

Future implementation tests must prove:

- deterministic report shape for synthetic `Player.log`-style summaries;
- deterministic report shape for synthetic `UTC_Log` text after #381
  normalization;
- no private path, raw hash, raw log line, raw payload, or exact private offset
  leaks;
- missing authorization blocks private source classes;
- scoring vocabulary stays within the contracted values;
- `parser_behavior_verified=false`;
- `fixture_promotion_authorized=false`;
- no corpus status changes are emitted.

## Protected Surfaces

Do not change:

- parser behavior;
- parser state final reconciliation;
- parser event classes;
- router semantics;
- diagnostics report shape;
- drift report behavior;
- golden replay behavior;
- feature-equity behavior;
- evidence-ledger behavior;
- corpus manifest or session ledger status;
- match/game identity;
- deduplication;
- workbook schema;
- webhook payload shape;
- Apps Script behavior;
- Google Sheets sync;
- output transport;
- runtime status schema;
- failed-post handling;
- workbook exports;
- analytics behavior;
- AI/model-provider behavior;
- coaching behavior;
- CI gates;
- merge readiness;
- deploy readiness;
- release readiness;
- production behavior;
- final integration policy.

Do not read, copy, hash, summarize, upload, or commit private logs, local-only
evidence, generated/private/runtime artifacts, secrets, credentials, tokens,
API keys, webhook URLs, screenshots, decklists, card choices, or private
reports.

## Acceptance Criteria

This contract is complete when:

- it defines the local harvest candidate report truth boundary;
- it preserves `implementation_authorized=false`;
- it preserves `private_harvest_authorized=false`;
- it preserves `fixture_promotion_authorized=false`;
- it defines accepted and forbidden input classes;
- it defines candidate summary, parser fact preview, and private pointer
  logical shapes;
- it defines candidate scoring vocabulary;
- it explains why candidate reports are advisory and not parser/readiness
  truth;
- documentation-only validation is run or explicitly recorded as unavailable;
- the next workflow route does not activate #382 implementation by default.

## Recommended Next Role

Recommended next role: Codex A, lifecycle/activation thinker.

Codex C is not recommended immediately because this contract is planning-only
and the latest handoff says implementation is not authorized. Codex A should
decide whether #382 should remain deferred, split into a synthetic-only
implementation issue, or request explicit user approval for a local-only
private-evidence execution path under #434.

## Pasteable Next-Role Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex A: Thinker for issue #382 lifecycle activation after the Codex B
contract for local harvest candidate reports.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/382

Pipeline tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/388

Parent private-evidence issue:
https://github.com/Tahjali11/Mythic-Edge/issues/434

Contract:
docs/contracts/parser_evidence_local_harvest_candidate_reports.md

Base branch:
main

Goal:
Decide whether #382 should remain planning-only, split into a synthetic-only
Codex C implementation issue, or require a separate user-approved private
evidence execution path. Preserve implementation_authorized=false,
private_harvest_authorized=false, and fixture_promotion_authorized=false unless
you create an explicit scoped activation path.

Do not implement code.
Do not activate #388 or #381.
Do not run or read private Player.log, UTC_Log, app-data, live MTGA, network,
firewall/drop, packet, OS/router, diagnostics, drift, or private smoke checks.
Do not create fixtures or fixture-promotion packets.
Do not promote blocked, report-only, private-evidence, or external-boundary rows.
Do not claim parser_behavior_ready, pipeline activation readiness, fixture
promotion readiness, release readiness, production readiness, analytics truth,
AI truth, coaching truth, or full parser regression parity.

Expected output:
- lifecycle decision for #382
- whether a Codex C synthetic-only implementation prompt is appropriate
- required activation gates if implementation is recommended
- workflow_handoff block with repository and repository_url
```

workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/382"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/381"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/520"
  parent_private_evidence_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  completed_thread: "B"
  next_thread: "A"
  source_artifact: "GitHub issue #382 and parser evidence pipeline handoff"
  target_artifact: "docs/contracts/parser_evidence_local_harvest_candidate_reports.md"
  verdict: "planning_contract_complete_implementation_not_authorized"
  risk_tier: "High"
  base_branch: "main"
  target_branch: "main"
  previous_merge_commit: "34631ed7f67702aa6d96791d74506a72b1bba24f"
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  report_preconditions_ready_for_issue_388: true
  evidence_pipeline_planning_ready_for_issue_388: false
  implementation_authorized: false
  private_harvest_authorized: false
  fixture_promotion_authorized: false
  stop_conditions:
    - "Do not implement code without a later explicit activation prompt."
    - "Do not activate #388 or #381."
    - "Do not run or read private Player.log, UTC_Log, app-data, live MTGA, network, firewall/drop, packet, OS/router, diagnostics, drift, or private smoke checks."
    - "Do not create fixtures or fixture-promotion packets."
    - "Do not promote blocked, report-only, private-evidence, or external-boundary rows."
    - "Do not claim parser_behavior_ready, pipeline activation readiness, fixture-promotion readiness, release readiness, production readiness, analytics truth, AI truth, coaching truth, or full parser regression parity."
