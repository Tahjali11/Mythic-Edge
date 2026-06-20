# Parser Evidence UTC_Log Source Adapter Contract

## Module

Planning contract for issue #381, the optional `UTC_Log` source adapter
boundary for parser evidence-pipeline harvest workflows.

Plain English: this contract defines how Mythic Edge may later adapt
operator-selected or synthetic `UTC_Log`-style source text into
`Player.log`-equivalent text for existing parser/replay paths. The adapter is
not a second parser, not a private-log reader by default, not a fixture
promotion tool, and not parser/readiness truth.

This Codex B pass does not implement code, activate #381 for implementation,
read or run private logs, create fixtures, promote corpus rows, or claim
parser behavior readiness.

## Source Issue

- Repository: `Tahjali11/Mythic-Edge`
- Repository URL: `https://github.com/Tahjali11/Mythic-Edge`
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/381
- Pipeline tracker: https://github.com/Tahjali11/Mythic-Edge/issues/388
- Parent private-evidence issue: https://github.com/Tahjali11/Mythic-Edge/issues/434
- Dependency issue: https://github.com/Tahjali11/Mythic-Edge/issues/518
- Dependency PR: https://github.com/Tahjali11/Mythic-Edge/pull/519
- Prior activation issue: https://github.com/Tahjali11/Mythic-Edge/issues/516
- Prior activation PR: https://github.com/Tahjali11/Mythic-Edge/pull/517
- Recently closed corpus tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
- Base branch: `main`
- Target branch: `main`
- Risk tier: High

Observed during this Codex B pass:

- Operating checkout remote matches
  `https://github.com/Tahjali11/Mythic-Edge.git`.
- `main` is up to date with `origin/main`.
- `HEAD` is `810ba3a Add parser evidence pipeline planning umbrella`.
- Issue #381 is open and inactive.
- Tracker #388 is open and inactive.
- Parent private-evidence issue #434 is open.
- Issue #518 is completed and PR #519 is merged.
- Issue #516 is completed and PR #517 is merged.
- Tracker #158 is closed for corpus classification/report-precondition
  closeout.
- Issue #381's body still contains the old all-45
  covered-synthetic-or-stronger start condition. The latest #381 comment and
  the #518 umbrella supersede that wording for planning purposes only.

## Source Artifacts Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/internal_project_map.md`
- `docs/local_artifacts_manifest.json`
- Issue #381
- Tracker #388
- Parent private-evidence issue #434
- Issue #518 and PR #519
- Issue #516 and PR #517
- Tracker #158 closeout comments
- `docs/contracts/parser_evidence_pipeline_planning_umbrella.md`
- `docs/contracts/parser_evidence_pipeline_activation_criteria.md`
- `docs/contracts/parser_corpus_private_evidence_window_offset_capture.md`
- `docs/contracts/parser_corpus_private_log_report_only_drift_private_evidence_execution.md`
- `docs/contracts/parser_corpus_firewall_network_drop_private_evidence_execution.md`
- `src/mythic_edge_parser/log/entry.py`
- `src/mythic_edge_parser/log/tailer.py`
- `src/mythic_edge_parser/stream.py`
- `tests/test_log_entry_headers.py`
- adjacent parser, diagnostics, drift, corpus, and private-evidence docs found
  during focused searches

## Observed Current Behavior

The repository has no dedicated `UTC_Log` source adapter module.

Existing parser input behavior:

- `src/mythic_edge_parser/log/entry.py` defines `UTC_PREFIX_RE` as
  `^\[\d+\]\s+`.
- `LineBuffer` removes that prefix from complete lines before header
  classification.
- `resolve_header_policy` also removes that prefix after left-stripping before
  classifying metadata, matchmaking, truncation, bracketed parser headers, and
  unknown headers.
- `tests/test_log_entry_headers.py` covers UTC-style frame-prefix handling for
  UnityCrossThreadLogger and detailed-logging metadata lines.
- `src/mythic_edge_parser/log/tailer.py` reads bytes from a configured path,
  tracks offsets, handles truncation/rotation by size comparison, decodes with
  UTF-8 replacement, and returns parser `LogEntry` batches.
- `src/mythic_edge_parser/stream.py` starts the live parser by opening the
  configured log path from the end and routing existing `LogEntry` objects
  through `Router`.

Existing privacy behavior:

- `docs/local_artifacts_manifest.json` classifies configured `Player.log`
  as `Private Local Inputs` and forbids content reads, tailing, hashing,
  copying, and raw path printing in readiness checks.
- Private-evidence contracts allow only explicitly approved source classes,
  windows, artifact classes, redaction policy, and local-only handling before
  any private source is touched.
- No current contract authorizes this Codex B pass to inspect private
  `Player.log`, private `UTC_Log`, app-data, offset windows, local smoke
  output, or private reports.

Current readiness facts to preserve:

```yaml
parser_behavior_ready: false
pipeline_activation_ready_for_issue_388: false
report_preconditions_ready_for_issue_388: true
evidence_pipeline_planning_ready_for_issue_388: false
```

## Problem

Issue #381 needs a durable boundary before anyone implements a `UTC_Log`
source adapter. The adapter sits near several high-risk edges:

- private local archive discovery;
- exact local source selection;
- log content normalization;
- existing parser/replay paths;
- future local harvest reports;
- fixture-promotion workflows.

Without a contract, an implementation could accidentally:

- treat `UTC_Log` as a second parser source of truth;
- scan arbitrary private directories;
- read private logs during tests or contract work;
- print exact private paths;
- commit normalized private log output;
- feed incomplete evidence into fixture promotion;
- overclaim parser behavior readiness or #388 activation readiness.

## Scope Decision

This contract approves the #381 planning boundary only.

This contract does not authorize immediate Codex C implementation. A future
Codex C implementation is appropriate only after a later explicit user prompt
or Codex A/G lifecycle approval says to activate #381 implementation against
this contract.

If later activated, Codex C may implement only synthetic-fixture source-adapter
behavior and tests. It must not run against real private `Player.log`,
private `UTC_Log`, live MTGA, app-data, network, firewall/drop, packet,
OS/router, private smoke, local offset windows, or private reports.

If later activated, Codex C may define a source adapter that:

- treats `UTC_Log` as a local input format, not a truth owner;
- normalizes source text into `Player.log`-equivalent text for existing
  parser/replay paths;
- uses synthetic fixture strings/files only in tests;
- reports normalization statistics and provenance metadata without content
  leaks;
- rejects or redacts private-path and private-content surfaces by default.

This contract does not authorize:

- private source discovery execution;
- private source content reads;
- private source hashing or copying;
- committed normalized private source artifacts;
- new corpus fixtures;
- fixture-promotion packets;
- corpus status promotion;
- parser behavior changes;
- #388 or #381 activation readiness claims.

## Owning Layer

Owning layer: Corpus / Provenance, with Parser support.

Corpus / Provenance owns the evidence-pipeline source-adapter boundary,
normalization provenance vocabulary, synthetic-fixture test scope, and
privacy-safe metadata policy.

Parser owns existing log entry parsing, header classification, routing,
parser events, parser state, match/game identity, deduplication, and final
reconciliation.

Generated / Local Artifacts owns any future local-only selected source,
offset-window metadata, normalized local copy, harvest candidate report, or
private review packet.

Quality / Governance owns workflow routing, contract validation, protected
surface checks, secret/private-marker checks, and review gates.

## Internal Project Area

Primary: Corpus / Provenance.

Supporting:

- Parser, for existing `src/mythic_edge_parser/log/` behavior and parser/replay
  consumption.
- Generated / Local Artifacts, for any future local-only source and normalized
  local output.
- Quality / Governance, for workflow and validation.

This contract is not a live parser capture contract, not a diagnostics
contract, not a fixture-promotion contract, not a local app contract, not an
analytics contract, not a workbook/transport contract, not an AI/coaching
contract, not a CI gate, and not a deploy/release readiness gate.

## Truth Owner

Truth owner for existing parser line/header interpretation:

- `src/mythic_edge_parser/log/entry.py`
- focused parser log-entry tests

Truth owner for future `UTC_Log` adapter source/provenance vocabulary:

- this contract;
- any later reviewed #381 implementation handoff and contract-test report, if
  implementation is explicitly authorized.

Truth owner for private-evidence execution boundaries:

- issue #434;
- `docs/contracts/parser_corpus_private_evidence_window_offset_capture.md`;
- relevant future explicit private-evidence issue, contract, privacy review,
  and user approval.

The adapter must not own parser facts, match facts, game facts, corpus status,
fixture expected output, live Player.log health, drift health, release
readiness, production readiness, analytics truth, AI truth, coaching truth, or
full parser regression parity.

## Bridge-Code Status

`deferred_future_boundary`

This contract authorizes no bridge code in Codex B.

If later activated, the source adapter would be bridge code from
Generated / Local Artifacts into existing Parser log-entry/replay surfaces.

Allowed future data flow:

```text
synthetic UTC_Log-style source
  -> UTC_Log source adapter normalization/provenance
  -> Player.log-equivalent text
  -> existing LineBuffer / Router / replay path
```

Future private data flow may be considered only under a later explicit
approval:

```text
user-approved local-only UTC_Log window
  -> local-only normalization
  -> local-only candidate/review artifact
```

Forbidden reverse flow:

- parser/replay results must not rewrite source evidence;
- analytics/workbook/AI summaries must not redefine adapter truth;
- local-only private artifacts must not flow into committed fixtures or corpus
  metadata without later proof/review/deployer gates.

## Files Owned By This Contract

Contract artifact:

- `docs/contracts/parser_evidence_utc_log_source_adapter.md`

Future Codex C files that may be authorized only after explicit #381
implementation activation:

- `src/mythic_edge_parser/app/utc_log_source_adapter.py`
- `tests/test_utc_log_source_adapter.py`
- `docs/implementation_handoffs/parser_evidence_utc_log_source_adapter_comparison.md`

Future Codex E review artifact:

- `docs/contract_test_reports/parser_evidence_utc_log_source_adapter.md`

Files that future Codex C may read but must not change unless the later prompt
explicitly authorizes it:

- `src/mythic_edge_parser/log/entry.py`
- `src/mythic_edge_parser/log/tailer.py`
- `src/mythic_edge_parser/stream.py`
- `tests/test_log_entry_headers.py`
- `tests/test_entry_buffer_edges.py`
- `tests/test_stream_unit.py`
- `docs/contracts/parser_evidence_pipeline_planning_umbrella.md`
- `docs/contracts/parser_evidence_pipeline_activation_criteria.md`
- `docs/local_artifacts_manifest.json`

Not owned by this contract:

- raw `Player.log` files;
- raw or normalized private `UTC_Log` files;
- exact private paths;
- local offset state;
- private source discovery results;
- private harvest artifacts;
- app-data;
- runtime status files;
- failed posts;
- workbook exports;
- generated SQLite files;
- screenshots;
- raw hashes;
- network traces;
- firewall/router/OS diagnostics;
- secrets, credentials, tokens, API keys, or webhook URLs;
- corpus manifest/session-ledger status promotion;
- golden replay fixtures or expected outputs;
- parser behavior, parser event classes, parser state final reconciliation,
  router semantics, match/game identity, deduplication, workbook schema,
  webhook payload shape, Apps Script behavior, Google Sheets sync, analytics,
  AI, coaching, CI gates, merge policy, deploy policy, release policy, or
  production behavior.

## Public Interface

This contract defines a future source-adapter interface. It does not create
that interface in Codex B.

If later activated, the public interface should be small and deterministic.
Recommended logical types and functions:

```python
@dataclass(frozen=True)
class UtcLogCandidate:
    source_label: str
    display_name: str
    size_bytes: int | None
    modified_time: str | None
    source_kind: Literal["synthetic", "user_selected_local"]
    privacy_class: Literal["public_fixture", "private_local"]

@dataclass(frozen=True)
class UtcLogNormalizationStats:
    input_line_count: int
    output_line_count: int
    utc_frame_prefix_lines: int
    unchanged_lines: int
    dropped_lines: int
    replacement_character_count: int
    degradation_status: Literal["ok", "review", "degraded", "failed"]

@dataclass(frozen=True)
class UtcLogNormalizationResult:
    text: str
    stats: UtcLogNormalizationStats
    source_label: str
    source_kind: Literal["synthetic", "user_selected_local"]
    warnings: tuple[str, ...]
```

Recommended functions:

```python
def normalize_utc_log_text(
    text: str,
    *,
    source_label: str,
    source_kind: Literal["synthetic", "user_selected_local"] = "synthetic",
) -> UtcLogNormalizationResult:
    ...
```

Optional future function, not required in the first implementation and not
allowed to scan private directories without later approval:

```python
def describe_user_selected_utc_log_candidate(path: Path) -> UtcLogCandidate:
    ...
```

`describe_user_selected_utc_log_candidate` may inspect only metadata allowed
by the active contract and approval. It must not read, hash, copy, tail,
normalize, or print the raw path of a private source by default.

No environment variable, CLI, local app route, runtime status field, workbook
field, webhook payload field, corpus manifest field, session-ledger field, or
fixture format is created by this contract.

## Inputs

Allowed inputs for this Codex B pass:

- committed repo docs, source, tests, and contracts;
- GitHub issue and PR metadata for #381, #388, #434, #516, #517, #518, #519,
  and #158 closeout.

Allowed future Codex C inputs only after explicit implementation activation:

- synthetic `UTC_Log`-style strings embedded in focused tests;
- synthetic fixture files under a test-controlled temp directory;
- existing committed sanitized fixtures if a later prompt names them;
- committed source and tests;
- existing public-safe docs and contracts.

Forbidden inputs for this contract and any future implementation unless a
later explicit contract and user approval name the exact source, window, and
artifact class:

- private `Player.log` contents;
- private `UTC_Log` contents;
- private app-data;
- live MTGA state;
- private smoke output;
- local offset windows;
- private drift reports;
- private harvest packets;
- exact private paths;
- raw hashes;
- raw log lines;
- screenshots;
- SQLite files;
- workbook exports;
- runtime artifacts;
- failed posts;
- credentials, tokens, API keys, webhook URLs, or secrets;
- decklists, card choices, private strategy notes;
- IP/network traces, packet captures, OS/router diagnostics, firewall logs,
  or Wi-Fi logs;
- external raw corpus contents.

## Normalization Rules

If later implemented, normalization must stay source-shape focused and must
not interpret game facts.

Required guarantees:

- Preserve source line order.
- Preserve source content except for the specifically contracted UTC frame
  prefix normalization and line-ending normalization.
- Normalize line endings to `\n` for synthetic/replay use.
- Treat the existing parser header classifier as the owner of header
  interpretation.
- Use the same UTC frame-prefix shape observed in `entry.py`:
  `^\[\d+\]\s+`.
- If stripping prefixes before parser/replay, strip only that prefix from the
  start of a line.
- If feeding unstripped UTC-prefixed lines into `LineBuffer`, rely on existing
  parser behavior and record prefix counts only if the adapter inspects
  synthetic content.
- Do not invent missing headers.
- Do not reconstruct missing GameState data.
- Do not infer match/game facts.
- Do not classify unknown parser content as supported.
- Do not silently drop non-empty lines except under an explicit malformed-input
  rule with a warning and `degradation_status`.

Malformed synthetic input should return warnings and a degraded/failed status
instead of raising for ordinary content shape issues. Programmer errors such
as non-string input may raise normal Python exceptions.

Private input errors must fail closed without printing raw paths or content.

## Local-Only Artifact Policy

No local-only artifacts are authorized by this Codex B pass.

If later explicitly approved, private/local adapter outputs must stay outside
Git and may use only symbolic source labels in public summaries. They must not
include:

- exact private paths;
- raw private lines;
- exact private offsets or file sizes;
- raw hashes;
- copied private source files;
- normalized private source text;
- private source snippets;
- decklists, strategy notes, screenshots, or credentials.

Committed repo artifacts may contain only synthetic fixtures or separately
reviewed sanitized fixtures under a later dedicated fixture-promotion
contract.

## Outputs

Allowed output for this Codex B pass:

- `docs/contracts/parser_evidence_utc_log_source_adapter.md`;
- final summary;
- pasteable next-thread prompt;
- workflow handoff block.

Allowed future Codex C outputs only after explicit #381 implementation
activation:

- source adapter module;
- focused synthetic-only tests;
- implementation handoff.

Forbidden outputs:

- private source reads or summaries;
- normalized private log files;
- private source discovery listings;
- fixture-promotion packets;
- corpus status changes;
- committed private/local/generated/runtime artifacts;
- parser behavior changes;
- readiness claims.

## Invariants

- `UTC_Log` is a source format, not a new truth owner.
- The adapter must produce `Player.log`-equivalent text for existing parser
  paths, not parser events directly.
- Existing parser entry/header/routing code remains the owner of parser
  interpretation.
- Synthetic tests may exercise normalization and parser-path compatibility.
- Synthetic tests must not prove private archive support, live support, or
  parser behavior readiness.
- Private source discovery is disabled unless a later explicit approval names
  the source class and local-only artifact class.
- Exact private paths and raw private content must not be printed, committed,
  hashed, copied, or summarized by default.
- #381 remains inactive for implementation until explicitly activated after
  this contract.
- #388 remains open and inactive.
- #434 remains the private-evidence parent gate.
- `parser_behavior_ready` remains false.
- `pipeline_activation_ready_for_issue_388` remains false.
- `report_preconditions_ready_for_issue_388` remains a report-local planning
  signal only.
- `evidence_pipeline_planning_ready_for_issue_388` remains false until a later
  lifecycle contract/update defines otherwise.

## Error Behavior

If future Codex C is asked to run against a real private source, stop unless
the prompt includes explicit approval naming the exact source class, symbolic
source label, window, artifact class, and redaction policy.

If implementation would need to scan arbitrary directories, stop and route to
Codex A/B for a narrower discovery contract.

If implementation would print exact private paths, raw private content, raw
hashes, exact offsets, or exact file sizes, stop.

If implementation would create normalized private source files, local harvest
artifacts, fixture-promotion packets, corpus metadata diffs, or committed
fixtures, stop unless a later child issue and contract authorize that exact
artifact.

If adapter behavior conflicts with existing parser header classification, stop
and route to Codex B before changing parser behavior.

If a future test requires private data to pass, the test is invalid for this
contract.

## Side Effects

Side effect of this Codex B pass:

- adds `docs/contracts/parser_evidence_utc_log_source_adapter.md`.

No code, tests, fixtures, corpus metadata, private artifacts, local app data,
runtime files, issue bodies, trackers, PRs, or GitHub state are changed by
this contract.

Future implementation side effects, if explicitly activated, are limited to
source/test/handoff files named by the activation prompt and this contract.

## Dependency Order

1. Complete this contract-only Codex B pass.
2. Review/submit/deploy this contract if requested through normal Codex E/F/G
   workflow.
3. Obtain explicit user or lifecycle approval to activate #381 implementation
   against this contract.
4. Implement only synthetic-fixture source-adapter support.
5. Review implementation against this contract.
6. Submit/deploy only after review and validation.
7. Do not proceed to #382 harvest candidate reports until #381 implementation
   exists or #382 receives a separate bypass contract.

## Compatibility

This contract is compatible with:

- existing `LineBuffer` UTC frame-prefix handling;
- existing `FileTailer` and `MtgaEventStream` behavior;
- existing parser/replay paths;
- existing #518 umbrella sequence;
- existing private-evidence and offset-window boundaries;
- current corpus readiness metrics.

This contract intentionally supersedes issue #381's stale start-condition
wording for planning interpretation only. It does not edit the issue body and
does not activate implementation.

## Tests Required

For this contract-only pass:

```bash
python3 tools/check_agent_docs.py
git diff --check
python3 tools/check_secret_patterns.py --all
python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
python3 tools/select_validation.py --base origin/main --paths docs/contracts/parser_evidence_utc_log_source_adapter.md
```

For future Codex C, if explicitly activated:

```bash
python3 -m pytest -q tests/test_utc_log_source_adapter.py tests/test_log_entry_headers.py
python3 -m pytest -q tests/test_entry_buffer_edges.py tests/test_stream_unit.py
python3 -m ruff check src tests tools
python3 tools/check_agent_docs.py
git diff --check
python3 tools/check_secret_patterns.py --all
python3 tools/check_protected_surfaces.py --base origin/main
python3 tools/select_validation.py --base origin/main
```

Future tests must include:

- synthetic UTC frame-prefix normalization;
- preservation of non-prefixed lines;
- no parser event emission from the adapter itself;
- compatibility with existing `LineBuffer`/parser-entry behavior;
- malformed synthetic input warnings/degradation;
- rejection or fail-closed behavior for private/local source operations when
  no explicit approval exists;
- no raw private path/content output in errors or reports.

## Acceptance Criteria

- The contract states that issue #381's original start condition is stale for
  planning purposes and superseded by #516/#518.
- The contract keeps #381 inactive for implementation until explicit later
  approval.
- The contract defines `UTC_Log` as an adapter source format, not a truth
  owner or second parser.
- The contract names the existing parser-owned header behavior.
- The contract defines synthetic-fixture-only implementation boundaries.
- The contract blocks private log reads, private source discovery, private
  normalized outputs, fixture promotion, corpus status promotion, and readiness
  claims.
- The contract preserves #388, #434, and readiness non-claims.
- The contract routes next work safely.

## Open Questions And Contract Risks

- Whether future #381 implementation should add a new source module under
  `src/mythic_edge_parser/app/` or a different local-artifact area. This
  contract recommends `src/mythic_edge_parser/app/utc_log_source_adapter.py`
  only as a small V1 path.
- Whether future private archive discovery should ever be implemented in the
  source repo, or kept as a local-only/operator tool. This requires a later
  contract.
- Whether `UTC_Log` normalization should strip prefixes before replay or feed
  raw prefixed synthetic lines through `LineBuffer`. This contract allows
  either only if semantics match existing `UTC_PREFIX_RE` behavior and tests
  prove compatibility.
- Whether #382 should support a `Player.log`-only bypass if #381 remains
  unimplemented. That requires a #382-specific contract.

## Next Workflow Action

Next role: Codex A: Thinker / lifecycle activation decision.

Reason: this contract intentionally does not activate #381 implementation.
Codex A or the user should decide whether to explicitly route #381 to Codex C
for synthetic-only implementation, keep #381 deferred, or split source
discovery into a separate issue.

Pasteable next-thread prompt:

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex A: Thinker for issue #381 after the UTC_Log source adapter
contract.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/381

Pipeline tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/388

Parent private-evidence issue:
https://github.com/Tahjali11/Mythic-Edge/issues/434

Contract:
docs/contracts/parser_evidence_utc_log_source_adapter.md

Goal:
Decide whether #381 should be explicitly activated for a synthetic-only
Codex C implementation, remain deferred, or be split before implementation.

Preserve:
- parser_behavior_ready=false
- pipeline_activation_ready_for_issue_388=false
- evidence_pipeline_planning_ready_for_issue_388=false

Do not implement code.
Do not read or run private Player.log, UTC_Log, app-data, live MTGA, network,
firewall/drop, packet, OS/router, or private smoke checks.
Do not create fixtures or fixture-promotion packets.
Do not promote blocked, report-only, private-evidence, or external-boundary
rows.
Do not claim parser behavior readiness, pipeline activation readiness,
release readiness, production readiness, analytics truth, AI truth, coaching
truth, or full parser regression parity.

Expected output:
- Activation decision
- If activated, pasteable Codex C prompt constrained to synthetic-only
  source-adapter implementation
- If deferred or split, next issue/problem representation
- workflow_handoff block
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/381"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  parent_private_evidence_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/434"
  dependency_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/518"
  completed_thread: "B"
  next_thread: "A"
  source_artifact: "GitHub issue #381 reconciliation comment and docs/contracts/parser_evidence_pipeline_planning_umbrella.md"
  target_artifact: "docs/contracts/parser_evidence_utc_log_source_adapter.md"
  verdict: "utc_log_source_adapter_contract_ready_planning_only"
  risk_tier: "High"
  base_branch: "main"
  target_branch: "main"
  branch: "main"
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  report_preconditions_ready_for_issue_388: true
  evidence_pipeline_planning_ready_for_issue_388: false
  implementation_authorized: false
  validation:
    - "python3 tools/check_agent_docs.py"
    - "git diff --check"
    - "python3 tools/check_secret_patterns.py --all"
    - "path-scoped protected-surface gate for docs/contracts/parser_evidence_utc_log_source_adapter.md"
    - "python3 tools/select_validation.py --base origin/main --paths docs/contracts/parser_evidence_utc_log_source_adapter.md"
  stop_conditions:
    - "Do not implement code in Codex B."
    - "Do not activate #381 for implementation from this contract alone."
    - "Do not run or read private Player.log, UTC_Log, app-data, live MTGA, network, firewall/drop, packet, OS/router, or private smoke checks."
    - "Do not create fixtures or fixture-promotion packets."
    - "Do not promote blocked, report-only, private-evidence, or external-boundary rows."
    - "Do not claim parser_behavior_ready, strict pipeline activation readiness, fixture-promotion readiness, release readiness, production readiness, analytics truth, AI truth, coaching truth, or full parser regression parity."
```
