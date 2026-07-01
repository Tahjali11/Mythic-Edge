# Quality Ruff Current Advisory Measurement Report Contract

## Module

Contract for issue #582, the current all-rules Ruff advisory measurement
report under quality tracker #567.

Plain English: this contract defines how Mythic Edge may later run a bounded
current Ruff all-rules measurement in advisory mode and convert the temporary
raw Ruff JSON into a sanitized report with
`tools/generate_ruff_advisory_report.py`. Advisory mode means the measurement
can describe current findings, but it must not fail CI, enable blocking rules,
run autofix, change source code, or claim readiness.

This Codex B pass writes only this contract. It does not run the current
all-rules Ruff measurement, create or commit a measurement report, change CI,
edit Ruff configuration, enable blocking rules, run autofix, change parser
behavior, activate #388/#381, or claim parser truth, corpus readiness,
security assurance, privacy assurance, release readiness, deploy readiness,
production readiness, analytics truth, AI truth, or coaching truth.

## Source Issue

- Repository: `Tahjali11/Mythic-Edge`
- Repository URL: `https://github.com/Tahjali11/Mythic-Edge`
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/582
- Clarification issue: https://github.com/Tahjali11/Mythic-Edge/issues/584
- Sanitized report execution issue:
  https://github.com/Tahjali11/Mythic-Edge/issues/588
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/567
- Project roadmap: https://github.com/Tahjali11/Mythic-Edge/issues/568
- Previous issue: https://github.com/Tahjali11/Mythic-Edge/issues/578
- Previous PR: https://github.com/Tahjali11/Mythic-Edge/pull/581
- Previous merge commit:
  `f6d29b3eac8c63f6ee797246f4023a749abaa361`
- Sibling coverage lane: https://github.com/Tahjali11/Mythic-Edge/issues/580
- Active parser evidence tracker:
  https://github.com/Tahjali11/Mythic-Edge/issues/388
- Base branch: `main`
- Target branch: `main`
- Working branch:
  `codex/quality-ruff-current-advisory-measurement-report-582`
- Target artifact:
  `docs/contracts/quality_ruff_current_advisory_measurement_report.md`
- Risk tier: High

Observed during this Codex B pass:

- The primary checkout contained unrelated local governance and parser-contract
  work, so this contract was reconciled in a clean issue worktree.
- The target contract existed as untracked local WIP at the start of this pass
  and was preserved rather than overwritten.
- `origin/main` included previous merge commit
  `f6d29b3eac8c63f6ee797246f4023a749abaa361`.
- Issue #582 was open.
- Tracker #567 was open.
- Roadmap #568 was open.
- Previous issue #578 was closed.
- Previous PR #581 was merged into `main`.
- Sibling coverage preflight issue #580 was open.
- No Ruff all-rules measurement was run.
- No report artifact was created.
- No CI, Ruff config, parser, corpus, workbook, webhook, Apps Script,
  analytics, AI, coaching, release, deploy, or production behavior changed.

Current authority flags to preserve:

```yaml
implementation_authorized: false
ci_change_authorized: false
ruff_blocking_promotion_authorized: false
ruff_autofix_authorized: false
ruff_measurement_execution_authorized: false
report_artifact_creation_authorized: false
parser_behavior_change_authorized: false
parser_behavior_ready: false
pipeline_activation_ready_for_issue_388: false
```

## Source Artifacts Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- Issue #582
- Issue #584
- Issue #588 and Codex E blocker handoff
- Tracker #567
- Roadmap #568
- Previous issue #578
- Previous PR #581
- Sibling coverage issue #580
- `docs/contracts/quality_ruff_advisory_zero_baseline_design.md`
- `docs/implementation_handoffs/quality_ruff_advisory_report_helper.md`
- `tools/generate_ruff_advisory_report.py`
- `tests/test_ruff_advisory_report.py`
- `pyproject.toml`
- `.github/workflows/repo-checks.yml`
- `tools/run_repo_checks.ps1`
- related quality coverage contracts as boundary references
- `docs/implementation_handoffs/quality_ruff_current_advisory_measurement_report.md`
  as the #584 Codex C blocker handoff

No private Player.log, UTC_Log, app-data, live MTGA data, network data,
workbook export, SQLite database, generated runtime artifact, private report,
secret, token, credential, API key, webhook URL, raw Ruff output artifact, raw
coverage artifact, private evidence, or source patch was read, copied,
summarized, committed, or generated.

## Owning Layer

Owning layer: Quality / Governance.

Ruff owns static-analysis findings only. A Ruff advisory measurement report may
describe current static-analysis findings for a named commit, Ruff version,
scan scope, and command. It does not own parser truth, corpus truth, fixture
validity, private-harvest readiness, security assurance, privacy assurance, CI
readiness, release readiness, deploy readiness, production readiness,
analytics truth, AI truth, or coaching truth.

## Internal Project Area

Primary: Quality / Governance.

Supporting area: CI / Tooling, as future planning only.

This contract is not a parser module, corpus module, analytics module,
AI/coaching module, workbook module, webhook module, deployment module, release
module, or production behavior change.

## Truth Owner

Truth owner for this contract: repo quality governance.

The sanitized report may be evidence that a specific Ruff command completed
and that `tools/generate_ruff_advisory_report.py` produced a deterministic
summary from the supplied JSON. It must not be treated as proof that:

- the repository is correct;
- parser behavior is correct;
- private evidence is safe;
- CI should block;
- a rule should be promoted;
- a rule finding is a vulnerability;
- release, deploy, or production readiness exists.

## Bridge-Code Status

`not_bridge_code`

The future report helper is a local quality/governance tool. It does not bridge
parser facts into downstream systems and does not change runtime behavior.

## Files Owned By This Contract

This contract owns only:

- `docs/contracts/quality_ruff_current_advisory_measurement_report.md`

Future execution lanes may reference, but are not authorized by this contract
to edit:

- `tools/generate_ruff_advisory_report.py`
- `tests/test_ruff_advisory_report.py`
- `docs/implementation_handoffs/quality_ruff_advisory_report_helper.md`
- `pyproject.toml`
- `.github/workflows/repo-checks.yml`
- `tools/run_repo_checks.ps1`

## Observed Current Behavior

Current Ruff configuration in `pyproject.toml` remains narrow:

```toml
[tool.ruff.lint]
select = ["E", "F", "I"]
```

Current CI lint command in `.github/workflows/repo-checks.yml`:

```text
py -m ruff check src tests tools
```

Current local PowerShell lint command in `tools/run_repo_checks.ps1`:

```text
py -m ruff check src tests
```

The #578 helper exists and can consume already-produced Ruff JSON through:

```bash
python3 tools/generate_ruff_advisory_report.py --input <ruff-json-file>
```

The helper writes a sanitized summary to stdout only. It does not run Ruff,
does not run autofix, does not edit source files, does not update CI, does not
enable blocking rules, and does not create a report artifact by itself.

## Problem

The first bad value is running:

```bash
python3 -m ruff check src tests tools --select ALL
```

and treating the result as a blocking gate.

The second bad value is running all-rules Ruff in advisory mode, then committing
raw Ruff JSON, local absolute paths, private markers, secret-like output,
generated artifacts, raw source snippets, autofix diffs, or source patches.

The third bad value is treating zero findings for an exact rule code as parser
correctness, security assurance, release readiness, CI readiness, or automatic
blocking-promotion approval.

The fourth bad value is using stale tracker-only counts from #567 as current
measurement evidence. The current report must name the exact branch/ref,
commit, Ruff version, scan scope, and command used.

The fifth bad value is treating Ruff-emitted absolute filenames as either
automatically public-safe or automatically impossible to process. Ruff may
emit native local absolute filenames in JSON diagnostics. Those filenames may
be normalized only when they are proven to live under the measured clean
checkout root. Any filename outside the measured checkout, any unresolved
absolute path, and any local path in public output remains a stop condition.

The sixth bad value is treating raw Ruff diagnostic `message` fields as public
summary fields. Ruff messages are untrusted diagnostic text. They may include
local path wording, private-marker vocabulary, source-like snippets, or
implementation details even when the sanitized report does not need message
text. Public reports must not echo raw messages. They may only ignore,
redact, or symbolically classify message fields under the message-handling
boundary below.

## Scope Decision

Selected scope:

```yaml
selected_scope: "contract_for_future_report_only_ruff_advisory_measurement"
implementation_authorized: false
ruff_measurement_execution_authorized: false
ci_change_authorized: false
ruff_blocking_promotion_authorized: false
ruff_autofix_authorized: false
report_artifact_creation_authorized: false
parser_behavior_change_authorized: false
```

This contract authorizes only contract language for:

- future preflight checks before current all-rules Ruff measurement;
- a report-only advisory command boundary;
- raw Ruff JSON temporary handling;
- a narrow Ruff-native filename normalization boundary;
- a narrow raw diagnostic-message handling boundary;
- sanitized report artifact shape and path pattern;
- symbolic diagnostic-filename omission for public-unsafe private-marker path
  text;
- helper usage with `tools/generate_ruff_advisory_report.py`;
- stop conditions for malformed, stale, private, local, secret-like, autofix,
  unsupported, or overclaiming output;
- exact-code zero-baseline candidate semantics;
- triggered-rule advisory classification;
- protected-surface review-required classification;
- routing after a future sanitized report exists.

This contract does not authorize:

- running the measurement now;
- implementing code;
- creating or committing a report now;
- opening a PR;
- changing CI;
- changing `pyproject.toml`;
- enabling any blocking Ruff rule;
- running autofix;
- broad cleanup;
- source rewrites;
- parser behavior changes;
- fixture promotion;
- corpus status changes;
- #388/#381 activation;
- readiness, assurance, truth, release, deploy, production, analytics, AI, or
  coaching claims.

## Future Measurement Preconditions

A future Codex C measurement pass may run only after all of these are true:

1. A later issue or explicit user instruction authorizes
   `ruff_measurement_execution_authorized: true`.
2. The future prompt names the target branch/ref and commit.
3. The worktree is clean before measurement except for already-authorized
   report output paths.
4. `origin/main` or the named target ref has been fetched immediately before
   measurement.
5. The measured commit matches the authorized commit.
6. The scan scope is exactly `src tests tools` unless a later contract narrows
   it.
7. The command uses `--select ALL`, `--exit-zero`, and `--output-format json`.
8. The command does not include `--fix`, `--unsafe-fixes`, `--fix-only`, or any
   output path outside ignored `_review_*/`.
9. The raw Ruff JSON is treated as temporary local evidence and remains
   uncommitted.
10. The helper accepts the raw JSON and emits the expected sanitized schema,
    including repo-relative filenames only.
11. The sanitized report passes secret/private/local-path scans.
12. The sanitized report says advisory only and includes non-claims.

If any precondition is missing, the future measurement must not run.

## Future Command Boundary

Future advisory measurement command, if separately authorized:

```bash
python3 -m ruff check src tests tools --select ALL --exit-zero --output-format json > _review_/quality_ruff_advisory/<run-id>/ruff-all.json
```

Required properties:

- `--select ALL` is allowed only because `--exit-zero` keeps the scan
  report-only.
- `--exit-zero` is mandatory.
- `--output-format json` is mandatory for helper input.
- `src tests tools` is the required scan scope.
- no `--fix`;
- no `--unsafe-fixes`;
- no `--fix-only`;
- no CI workflow edits;
- no Ruff config edits;
- no source edits;
- no parser, fixture, corpus, analytics, AI, workbook, webhook, Apps Script,
  release, deploy, or production behavior changes.

The future measurement pass should also record:

```bash
python3 -m ruff --version
git rev-parse --verify HEAD
git status --short --branch
```

These are metadata checks. They do not make the all-rules measurement a
blocking gate.

## Future Helper Boundary

After a separately authorized future measurement creates temporary raw Ruff
JSON, the helper command should be equivalent to:

```bash
python3 tools/generate_ruff_advisory_report.py \
  --input _review_/quality_ruff_advisory/<run-id>/ruff-all.json \
  --branch-or-ref <branch-or-ref> \
  --commit <commit-sha> \
  --ruff-version <ruff-version> \
  --scan-scope src tests tools \
  --command "python3 -m ruff check src tests tools --select ALL --exit-zero --output-format json"
```

Optional exact-code candidate inputs may be supplied only as exact Ruff rule
codes:

```bash
  --rule-code <EXACT_RULE_CODE>
```

or through a public-safe JSON list of exact rule codes:

```bash
  --rule-codes-file <repo-relative-json-list>
```

The helper must reject broad family candidates such as `S`, `B`, `PL`, `ANN`,
or `D`.

The helper output must remain stdout-only unless a later issue explicitly
authorizes writing a sanitized report artifact. If a report is authorized, the
committed file must be helper output or a reduced wrapper around helper output,
not raw Ruff output.

### Ruff-Native Filename Normalization

Ruff JSON diagnostics may contain native absolute filenames for files under
the measured checkout. A future helper or pre-helper step may normalize those
diagnostic filenames to repo-relative paths only when all of these are true:

1. The measurement target commit was verified immediately before the scan.
2. The measured checkout root is known from the clean dedicated worktree used
   for measurement.
3. Each absolute diagnostic filename resolves under that measured checkout
   root after symlink and `..` normalization.
4. The normalized path is repo-relative, uses forward slashes, and does not
   start with `/`, a drive prefix, `file://`, `..`, `_review_`, `data/`, or a
   generated/private artifact directory.
5. The raw absolute filename is not copied to stdout, committed reports,
   implementation handoffs, issue comments, PR bodies, tracker comments, or
   public docs.
6. The normalized path either passes private-marker and secret-pattern scans
   or is omitted from public path output under the diagnostic filename
   private-marker omission boundary below.

This exception applies only to Ruff diagnostic filename fields. It does not
apply to:

- command metadata;
- scan-scope metadata;
- rule messages;
- source snippets;
- fix edits;
- raw JSON records pasted into docs;
- private markers outside the diagnostic filename private-marker omission
  boundary;
- secret-like values;
- paths outside the measured checkout;
- generated local evidence paths;
- runtime artifact paths.

If any diagnostic filename cannot be normalized within the measured checkout,
the helper must fail closed. Allowed failure statuses:

- `measurement_blocked_path_outside_checkout`
- `measurement_blocked_path_normalization_unsupported`
- `measurement_blocked_local_path_leak`

The sanitized report must contain only repo-relative paths or public-safe
symbolic path-omission/bucket fields. It must not contain local absolute paths
even when they were accepted as temporary raw input.

### Diagnostic Filename Private-Marker Omission Boundary

Ruff diagnostic filename fields may sometimes resolve under the measured
checkout and still contain private-marker-like text as part of a source or
test filename. The public-safety boundary is to prevent that text from
appearing in committed artifacts, not to convert advisory findings into false
zero-baseline evidence.

A future helper may count a diagnostic whose filename contains private-marker
vocabulary without emitting the filename only when all of these are true:

1. the filename is a Ruff diagnostic `filename` field, not metadata, command
   text, a diagnostic message, a source snippet, a fix edit, or raw JSON copied
   into public output;
2. the filename resolves under the measured clean checkout after symlink and
   `..` normalization;
3. the normalized repo-relative path is inside the approved scan scope
   (`src`, `tests`, or `tools`) and is not under `_review_`, `data/`, runtime,
   generated, private-evidence, raw-log, workbook-export, SQLite, or local
   artifact paths;
4. the path does not contain secret-like values, credentials, tokens, API
   keys, webhook URLs, auth headers, source patches, or raw payload content;
5. the raw absolute path and normalized repo-relative path are not emitted to
   stdout, committed reports, implementation handoffs, issue comments, PR
   bodies, tracker comments, or public docs;
6. the public report records only non-reversible symbolic path handling such
   as counts, approved top-level scan-scope buckets, and labels like
   `path_omitted_private_marker_filename` or
   `path_bucketed_private_marker_filename`;
7. the finding remains counted under its exact Ruff rule code and must not be
   treated as a zero-baseline candidate;
8. any rule summary with omitted private-marker filename data uses a
   review-required or advisory disposition, not a blocking-promotion,
   cleanup-issue, or ignore disposition by default;
9. the final public artifact passes secret/private/local-path/protected-surface
   scans.

Allowed public fields for this boundary are optional and symbolic only:

```json
{
  "affected_paths": ["tools/public_safe_example.py"],
  "omitted_affected_path_count": 1,
  "path_handling_policy": "symbolic_private_marker_filename_omission",
  "path_scope_buckets": ["tests"]
}
```

These example values are illustrative. They do not authorize raw path output,
path hashes, reversible lookup keys, original basenames, path fragments,
private-marker strings, source snippets, fix edits, local absolute paths, or
raw Ruff JSON.

The helper must still fail closed with `measurement_blocked_private_marker`
when:

- private-marker text would be emitted in any public artifact;
- the path points outside the measured checkout;
- the path is under `_review_`, `data/`, runtime, generated, private-evidence,
  raw-log, workbook-export, SQLite, or local artifact paths;
- the path contains secret-like values or credential-shaped content;
- the path is needed for a human-readable explanation that cannot be expressed
  symbolically;
- omission would make a rule look clean, blocking-ready, or promotion-ready.

### Ruff Diagnostic Message Handling

Ruff JSON diagnostics may contain a `message` field. The sanitized report does
not require raw diagnostic messages, and raw messages must not become public
summary text.

A future helper may handle diagnostic `message` fields in one of these bounded
ways:

- ignore the message entirely when rule code, repo-relative filename, fix
  metadata, and aggregate counts are sufficient;
- store only symbolic message-handling labels, such as
  `message_not_emitted`, `message_redacted`, `message_symbolic_only`, or
  `message_review_required`;
- use message text only as temporary local input to decide whether a record
  must fail closed, without copying the raw message to stdout, committed
  reports, implementation handoffs, issue comments, PR bodies, tracker
  comments, or public docs.

Allowed symbolic classifications are public-safe labels only. They must not
include substrings, hashes intended for lookup, raw path values, source text,
fix text, private-marker values, secret-like values, log payloads, or quoted
message fragments.

Raw message content that contains local path wording or private-marker
vocabulary does not automatically block a sanitized report when all of these
are true:

1. the raw message is not emitted;
2. no human-readable message-derived text is emitted;
3. no path from the message is normalized, promoted, or copied into public
   output;
4. any retained message signal is reduced to symbolic labels or aggregate
   counts only;
5. the final public artifact passes secret/private/local-path/protected-surface
   scans.

The helper must still fail closed if a diagnostic message contains, requires
emitting, or is transformed into any of these forbidden outputs:

- secret-like values, credentials, tokens, API keys, webhook URLs, or auth
  headers;
- raw source snippets, copied source lines, source patches, fix edits, autofix
  diffs, or edit previews;
- unsafe paths, including paths outside the measured checkout, unnormalizable
  paths, URI/scheme-like paths, UNC/double-slash paths, `_review_*/`, `data/`,
  generated/private artifact paths, or local absolute paths in public output;
- raw log content, raw private payloads, Player.log/UTC_Log contents, workbook
  exports, SQLite rows, runtime artifacts, or private reports;
- text implying CI readiness, blocking readiness, parser truth, security
  assurance, privacy assurance, release readiness, deploy readiness,
  production readiness, analytics truth, AI truth, or coaching truth.

If a diagnostic message is needed for public human-readable explanation, the
future helper must fail closed instead of emitting it. The report may say only
that message text was omitted, redacted, or reduced to symbolic classification.

## Raw Output Handling

Raw Ruff JSON must be stored only as temporary, local, uncommitted evidence.
It may preserve Ruff's native diagnostic fields so the helper can classify
findings, but those native records must not become the committed report.
Raw Ruff JSON may contain Ruff-native absolute diagnostic filenames only under
the normalization boundary above. Raw Ruff JSON may contain diagnostic
messages only as temporary local input under the message-handling boundary
above.

Allowed temporary path pattern:

```text
_review_/quality_ruff_advisory/<run-id>/ruff-all.json
```

The repo ignores `_review_*/`, so raw output under this path must remain local.
It must not be staged or committed.

Forbidden raw output handling:

- committing raw Ruff JSON;
- copying raw Ruff JSON into docs;
- posting raw Ruff JSON to issues, PRs, comments, or trackers;
- storing raw output under `docs/`;
- storing raw output under `data/`;
- storing raw output under runtime or generated artifact paths;
- storing raw output outside ignored `_review_*/`;
- retaining local raw output after the report has been reviewed unless the
  follow-up issue explicitly authorizes retention.

## Sanitized Report Artifact Policy

This contract does not create a report artifact. A future measurement execution
issue may authorize one sanitized report artifact if the helper output passes
public-safety checks.

Allowed committed sanitized report path pattern, if separately authorized:

```text
docs/quality_reports/ruff_advisory/<YYYY-MM-DD>-<short-commit>-ruff-advisory-report.json
```

Optional implementation handoff path:

```text
docs/implementation_handoffs/quality_ruff_current_advisory_measurement_report.md
```

The sanitized report must use:

```json
{
  "object": "mythic_edge_quality_ruff_advisory_report",
  "schema_version": "quality_ruff_advisory_report.v1"
}
```

Required report metadata:

- repository;
- repository URL;
- branch or ref;
- commit;
- Ruff version;
- scan scope;
- command;
- exit behavior;
- generated timestamp in UTC, if added by the future report writer;
- helper schema version;
- total finding count;
- triggered exact rule-code count;
- zero-baseline exact rule-code count;
- rule summaries;
- zero-baseline candidates;
- non-claims.

The sanitized report must not include local absolute paths, private markers,
secret-like values, raw log names, runtime artifacts, generated private
artifacts, raw Ruff JSON, source patches, autofix diffs, raw source snippets,
or any output implying CI readiness, parser truth, security assurance, privacy
assurance, release readiness, deploy readiness, production readiness,
analytics truth, AI truth, or coaching truth.

If a diagnostic filename is omitted under the private-marker filename boundary,
the report may include only symbolic omission/count/bucket fields. It must not
include the omitted path, its basename, any path fragment, a path hash, or the
private-marker text that caused omission.

If the helper records diagnostic-message handling, it may emit only bounded
symbolic fields such as:

```json
{
  "diagnostic_message_policy": "not_emitted",
  "message_signal": "symbolic_only"
}
```

These example values are illustrative, not required schema fields. They do not
authorize raw message output.

If a future implementation handoff needs examples, examples must be synthetic
and reduced. They must not paste raw Ruff records, source snippets, raw command
output, local absolute paths, generated artifacts, or private markers.

## Report Status Vocabulary

Allowed report statuses for a future measurement handoff:

- `measurement_not_run`
- `measurement_authorized_not_started`
- `measurement_completed_report_only`
- `measurement_completed_report_only_with_symbolic_path_omissions`
- `measurement_blocked_tool_missing`
- `measurement_blocked_command_failed`
- `measurement_blocked_malformed_json`
- `measurement_blocked_input_unreadable`
- `measurement_blocked_local_path_leak`
- `measurement_blocked_path_outside_checkout`
- `measurement_blocked_path_normalization_unsupported`
- `measurement_blocked_private_marker`
- `measurement_blocked_private_marker_path_required`
- `measurement_blocked_secret_like_output`
- `measurement_blocked_stale_commit`
- `measurement_blocked_dirty_worktree`
- `measurement_blocked_autofix_flag`
- `measurement_blocked_raw_output_public`
- `measurement_blocked_raw_source_snippet_public`
- `measurement_blocked_helper_rejection`
- `measurement_blocked_unsupported_rule_record`

Forbidden report statuses:

- `ci_ready`
- `blocking_ready`
- `blocking_enabled`
- `parser_ready`
- `parser_truth_confirmed`
- `security_assured`
- `privacy_assured`
- `release_ready`
- `deploy_ready`
- `production_ready`
- `auto_fixed`
- `truth_confirmed`

All blocked statuses fail closed. A blocked measurement must not become a
partial success or a promotion recommendation.

## Rule Classification Semantics

Exact-code zero-baseline candidate:

- allowed only for exact Ruff rule codes with zero findings in the named
  branch/ref, commit, Ruff version, scan scope, and command;
- must not be inferred from broad family cleanliness;
- must not be treated as blocking by default;
- must route to a later candidate-selection or blocking-promotion issue.

Triggered rule:

- any exact rule code with one or more findings;
- remains advisory by default;
- may be classified as `cleanup_issue_candidate` or
  `protected_surface_review_required` by later review;
- must not be promoted to blocking until existing findings are cleaned or a
  protected-surface contract authorizes narrower handling.

Protected-surface finding:

- any finding touching parser truth, private evidence, corpus/evidence,
  workbook/webhook/Apps Script, analytics/AI/coaching, CI/release/deploy, or
  governance/workflow surfaces;
- routes to review before any fix or promotion;
- does not prove the protected surface is broken.

Autofix metadata:

- evidence only;
- never approval to run `--fix`, `--fix-only`, or `--unsafe-fixes`;
- future autofix work requires a separate exact-rule/path contract.

## Stop Conditions

Future measurement must stop without report adoption when:

- measurement execution has not been explicitly authorized;
- the worktree is dirty before measurement;
- the target commit does not match the authorized commit;
- Ruff is missing;
- Ruff exits nonzero for a reason other than findings despite `--exit-zero`;
- the command omits `--exit-zero`;
- the command uses `--fix`, `--fix-only`, or `--unsafe-fixes`;
- the command changes CI or Ruff config;
- raw Ruff JSON is malformed;
- raw Ruff JSON contains local absolute paths outside Ruff diagnostic filename
  fields;
- any Ruff diagnostic filename is absolute and cannot be normalized to a
  repo-relative path under the measured checkout;
- raw Ruff JSON contains secret-like output in any field;
- raw Ruff JSON contains private markers outside un-emitted diagnostic message
  fields handled under the message-handling boundary and outside diagnostic
  filename fields handled under the symbolic private-marker filename omission
  boundary;
- a diagnostic filename with private-marker text cannot be omitted or
  symbolically bucketed without losing required count evidence;
- raw diagnostic messages require public emission or contain forbidden content
  under the message-handling boundary;
- raw output would need to be committed to proceed;
- helper input is unreadable;
- helper output is malformed;
- helper rejects unsupported records;
- helper output contains local absolute paths, emitted private-marker path
  text, secret-like values, raw logs, source patches, raw source snippets,
  autofix diffs, or non-symbolic path omission data;
- a proposed public report or handoff would paste raw Ruff records or raw
  command output instead of reduced helper summary fields;
- the sanitized report omits repository, branch/ref, commit, Ruff version,
  command, scan scope, helper schema, totals, or non-claims;
- any text implies CI readiness, parser truth, security/privacy assurance,
  release readiness, deploy readiness, production readiness, analytics truth,
  AI truth, or coaching truth.

## Relationship To Tracker #567

Tracker #567 owns the all-rules Ruff advisory sweep and zero-baseline CI
promotion roadmap.

This contract is the next report-only bridge after #570 and #578:

- #570 defined advisory-first and exact-code zero-baseline semantics.
- #578 implemented the local helper that transforms already-produced Ruff JSON
  into a sanitized summary.
- #582 defines when a current measurement report may be run and recorded.

Historical tracker counts are planning context only. They are not current
measurement evidence for #582.

## Relationship To Roadmap #568 And Sibling Coverage Lane #580

Roadmap #568 allows Phase 0 read-only measurement and planning lanes to proceed
in parallel when they do not mutate source behavior, change CI, activate
enforcement, or interfere with #388.

Sibling issue #580 is coverage preflight work under tracker #566. It does not
authorize Ruff measurement execution, and this Ruff contract does not authorize
coverage execution.

If #580 and #582 are active at the same time, each lane must keep separate
artifacts, separate validation, and separate non-claims.

## Relationship To #388

The parser evidence tracker #388 remains open/inactive for this contract.

A Ruff advisory report must not:

- activate #388 or #381;
- authorize private harvest;
- validate parser evidence;
- promote fixtures;
- update corpus metadata;
- prove parser behavior readiness;
- prove pipeline activation readiness;
- prove private smoke success.

## Future Routing After Report Creation

After a future sanitized report exists, route follow-up work into one of these
separate lanes:

1. Candidate-selection contract for exact-code zero-baseline candidates.
2. Cleanup issue creation for triggered high-signal findings.
3. Protected-surface review contract for findings touching parser, corpus,
   private-evidence, CI/release/deploy, workbook/webhook/Apps Script,
   analytics/AI/coaching, or workflow surfaces.
4. Blocking-promotion precondition issue for exact codes that remain clean and
   pass review.
5. Autofix trial contract for one exact rule/path slice, only if explicitly
   authorized.

The report itself must not create issues, PRs, comments, branches, commits,
labels, tracker updates, CI gates, or rule promotions.

## Validation Expectations For Codex B

Codex B validation for this contract should be docs-only:

```bash
printf '%s\n' docs/contracts/quality_ruff_current_advisory_measurement_report.md \
  | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' docs/contracts/quality_ruff_current_advisory_measurement_report.md \
  | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
git diff --check
git diff --check --no-index /dev/null docs/contracts/quality_ruff_current_advisory_measurement_report.md
```

Codex B must not run:

```bash
python3 -m ruff check src tests tools --select ALL --exit-zero --output-format json
```

because that is the future measurement execution surface.

## Validation Expectations For A Future Measurement Pass

A future Codex C measurement pass, if separately authorized, should validate:

- exact branch/ref and commit;
- clean worktree before measurement;
- measured checkout root used for any diagnostic filename normalization;
- Ruff version;
- advisory command includes `--select ALL`, `--exit-zero`, and
  `--output-format json`;
- no `--fix`, `--fix-only`, or `--unsafe-fixes`;
- raw Ruff JSON remains under ignored `_review_*/`;
- helper output uses `quality_ruff_advisory_report.v1`;
- helper output validates as JSON;
- helper output contains required metadata and non-claims;
- helper output contains repo-relative paths only for emitted path fields;
- diagnostic filenames omitted for private-marker reasons are represented only
  through symbolic counts or approved top-level scan-scope buckets;
- helper output contains no raw diagnostic messages;
- any diagnostic-message handling is either ignored, redacted, or symbolic
  only;
- local-path, private-marker, secret-pattern, source-patch, and autofix-diff
  scans pass over any public artifact;
- raw JSON is not staged;
- sanitized report is labeled report-only/advisory-only.

## Acceptance Criteria

- The contract exists at
  `docs/contracts/quality_ruff_current_advisory_measurement_report.md`.
- The contract defines the future all-rules Ruff advisory measurement boundary.
- The contract does not authorize measurement execution by itself.
- The contract preserves no-CI-change, no-blocking-promotion, no-autofix, and
  no-readiness boundaries.
- The contract defines raw Ruff JSON temporary handling.
- The contract defines the sanitized report artifact path pattern, if a later
  execution issue authorizes committing one.
- The contract defines that raw diagnostic messages are not public summary
  fields and may only be ignored, redacted, or symbolically classified when
  they are not emitted.
- The contract defines that diagnostic filename fields containing
  private-marker text may be omitted or symbolically bucketed only when the
  filename resolves under the measured checkout, remains inside the approved
  scan scope, and the public artifact emits no raw or normalized private-marker
  path text.
- The contract defines stop conditions for malformed Ruff output, command
  failure, helper rejection, local-path leakage, unnormalizable Ruff
  diagnostic filenames, private markers, secret-like output, raw log
  references, autofix flags, unsupported records, stale commit or branch
  metadata, and overclaims.
- The contract defines exact-code zero-baseline candidate semantics, triggered
  rule advisory classification, and protected-surface review-required
  classification.
- The contract routes future work to candidate-selection, cleanup,
  protected-surface review, blocking-promotion precondition, or autofix-trial
  lanes instead of performing those actions directly.

## Non-Claims

This contract does not claim:

- current Ruff measurement completed;
- CI readiness;
- blocking-promotion readiness;
- parser behavior readiness;
- pipeline activation readiness for #388;
- parser truth;
- fixture promotion readiness;
- corpus readiness;
- private smoke success;
- release readiness;
- deploy readiness;
- production readiness;
- security assurance;
- privacy assurance;
- analytics truth;
- AI truth;
- coaching truth.

## Protected Surfaces

This contract does not authorize:

- code implementation outside the bounded helper/test filename-normalization,
  message-handling, and symbolic private-marker filename omission fixes
  described for issues #584 and #588;
- PR creation;
- tracker closure;
- issue closure;
- all-rules Ruff measurement execution;
- report artifact creation;
- CI or GitHub Actions changes;
- `pyproject.toml` Ruff rule-selection changes;
- blocking Ruff rules;
- Ruff autofix;
- Ruff unsafe fixes;
- broad cleanup;
- parser behavior changes;
- fixture promotion;
- corpus status changes;
- private harvest;
- #388 or #381 activation;
- workbook, webhook, Apps Script, analytics, AI, coaching, release, deploy, or
  production behavior changes.

## Issue #584 Clarification Decision

Selected decision for issue #584:

```yaml
contract_clarification: "allow_bounded_ruff_filename_and_message_sanitization"
filename_normalization_allowed_only_for: "Ruff diagnostic filename fields under the measured checkout"
message_handling_allowed_only_for: "unemitted Ruff diagnostic message fields"
public_output_must_use: "repo_relative_paths_only"
raw_messages_may_be: "ignored_redacted_or_symbolically_classified_only"
raw_messages_must_not_be_emitted: true
paths_outside_checkout_fail_closed: true
secrets_raw_snippets_fix_edits_unsafe_paths_raw_logs_and_overclaims_fail_closed: true
raw_json_remains_local_uncommitted: true
sanitized_report_created_by_this_clarification: false
measurement_rerun_authorized_by_this_clarification: false
ci_change_authorized: false
ruff_blocking_promotion_authorized: false
ruff_autofix_authorized: false
```

Rationale: Codex C established that Ruff `0.15.12` may emit absolute
diagnostic filenames as native JSON behavior. The safety boundary should block
public leakage, not make current measurement impossible when every diagnostic
filename is provably inside the measured clean checkout and can be reduced to a
repo-relative path before any public artifact is created.

Codex C also established that Ruff diagnostic messages may contain local-path
or private-marker wording even when the helper does not emit diagnostic
messages. The public-safety boundary should block unsafe public output, not
require public reports to parse or publish unneeded raw diagnostic messages.
Messages that are not emitted may therefore be ignored, redacted, or reduced
to symbolic labels, while secrets, raw source snippets, fix edits, unsafe
paths in public output, raw logs, private payloads, and readiness/truth/
assurance claims still fail closed.

## Issue #588 Clarification Decision

Selected decision for issue #588:

```yaml
contract_clarification: "allow_symbolic_private_marker_filename_omission"
applies_only_to: "Ruff diagnostic filename fields under the measured checkout"
public_path_output_allowed: "repo_relative_paths_that_pass_public_scans_only"
private_marker_filename_output_allowed: false
private_marker_filename_counting_allowed: true
private_marker_filename_bucket_reporting_allowed: true
allowed_buckets: "approved top-level scan-scope buckets only"
path_hashes_or_reversible_lookup_keys_allowed: false
omitted_paths_may_create_zero_baseline_candidates: false
secrets_raw_snippets_fix_edits_unsafe_paths_raw_logs_and_overclaims_fail_closed: true
raw_json_remains_local_uncommitted: true
sanitized_report_created_by_this_clarification: false
measurement_rerun_authorized_by_this_clarification: false
ci_change_authorized: false
ruff_blocking_promotion_authorized: false
ruff_autofix_authorized: false
```

Rationale: Codex E verified that the raw-source/fix-edit message blocker was
fixed for issue #588, then found the next fail-closed boundary:
`measurement_blocked_private_marker` from diagnostic filename fields. The
contract now distinguishes public path emission from private-marker path
counting. A public report may count the affected finding and use symbolic
omission or approved top-level scan-scope buckets, but it must not emit the
path, basename, path fragment, hash, or private-marker text.

This clarification does not make private-marker filename findings safe for
automatic promotion. Any rule summary affected by omitted private-marker path
data remains advisory or review-required and cannot become a zero-baseline,
blocking-promotion, cleanup-issue, or ignore recommendation by default.

## Recommended Next Role

Recommended next role for issue #588: Codex D.

For issue #588, this clarification should route to Codex D for the smallest
helper/test update needed to keep private-marker diagnostic filename fields
out of public path output while preserving advisory counts and symbolic bucket
evidence. The existing #588 approval may be used only within the original
report-execution scope and only if Codex D first validates that raw Ruff JSON
remains local, uncommitted, and unchanged except through the already-approved
measurement path.

Codex D must not treat this contract clarification as permission to broaden
the report, emit omitted filenames, create cleanup issues, promote blocking
rules, change CI, run autofix, or claim readiness/truth/assurance.

## Pasteable Codex D Prompt

```text
Use the Mythic Edge workflow rules.

Act as Codex D: Module Fixer for issue #588.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/588

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/567

Project roadmap:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Previous issue:
https://github.com/Tahjali11/Mythic-Edge/issues/584

Previous PR:
https://github.com/Tahjali11/Mythic-Edge/pull/587

Previous merge commit:
51d5d8352c10204663d904765a8820bb464a52ac

Contract:
docs/contracts/quality_ruff_current_advisory_measurement_report.md

Implementation handoff:
docs/implementation_handoffs/quality_ruff_sanitized_advisory_report_execution.md

Blocker:
Codex E verified that the raw-source/fix-edit message blocker was fixed. The
remaining blocker is `measurement_blocked_private_marker` from Ruff diagnostic
filename fields. The contract now clarifies that a diagnostic filename under
the measured checkout may be omitted from public path output and counted
symbolically when the filename itself contains private-marker text.

Goal:
Implement the smallest helper/test fix allowed by the clarified contract:
keep Ruff-native diagnostic filename fields repo-relative when they pass public
scans, omit or symbolically bucket private-marker diagnostic filename fields
without emitting the path, preserve advisory counts, and keep raw diagnostic
messages un-emitted. Continue to reject secrets, raw source snippets, fix
edits, unsafe paths in public output, raw logs/private payloads, autofix
output, outside-checkout paths, generated/private artifact paths, and
readiness/truth/assurance claims.

Allowed scope:
- `tools/generate_ruff_advisory_report.py`
- `tests/test_ruff_advisory_report.py`
- `docs/implementation_handoffs/quality_ruff_sanitized_advisory_report_execution.md`
  if a D handoff update is needed

Do not run a new all-rules Ruff measurement. Use only the already-approved
#588 local raw Ruff JSON if it is still present, ignored, uncommitted, and tied
to the approved target commit. Do not create or commit a sanitized measurement
report unless the original #588 approval remains valid and the fixed helper
passes validation.

Run:
- PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q tests/test_ruff_advisory_report.py
- python3 -m ruff check src tests tools --no-cache
- printf '%s\n' tools/generate_ruff_advisory_report.py tests/test_ruff_advisory_report.py | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
- printf '%s\n' tools/generate_ruff_advisory_report.py tests/test_ruff_advisory_report.py | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
- git diff --check

Do not open a PR.
Do not change CI.
Do not enable blocking Ruff rules.
Do not run autofix.
Do not change parser behavior, promote fixtures, change corpus status, or
activate #388/#381.
Do not claim CI readiness, parser truth, corpus readiness, security/privacy
assurance, release readiness, deploy readiness, production readiness, analytics
truth, AI truth, or coaching truth.
```

## Workflow Handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/588"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/567"
  project_roadmap: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/584"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/587"
  previous_merge_commit: "51d5d8352c10204663d904765a8820bb464a52ac"
  completed_thread: "B"
  next_thread: "D"
  verdict: "ruff_private_marker_filename_omission_contract_clarified_ready_for_helper_fix"
  risk_tier: "High"
  base_branch: "main"
  target_branch: "main"
  branch: "codex/quality-ruff-sanitized-advisory-report-588"
  target_artifact: "docs/contracts/quality_ruff_current_advisory_measurement_report.md"
  implementation_handoff: "docs/implementation_handoffs/quality_ruff_sanitized_advisory_report_execution.md"
  sanitized_report_created: false
  raw_ruff_json_committed: false
  ci_change_authorized: false
  ruff_blocking_promotion_authorized: false
  ruff_autofix_authorized: false
  ruff_measurement_execution_authorized: false
  report_artifact_creation_authorized: false
  private_marker_filename_output_authorized: false
  symbolic_private_marker_filename_omission_authorized: true
  parser_behavior_change_authorized: false
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  validation:
    - "printf '%s\\n' docs/contracts/quality_ruff_current_advisory_measurement_report.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin"
    - "printf '%s\\n' docs/contracts/quality_ruff_current_advisory_measurement_report.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin"
    - "git diff --check"
    - "git diff --check --no-index /dev/null docs/contracts/quality_ruff_current_advisory_measurement_report.md"
  stop_conditions:
    - "Do not run the all-rules Ruff measurement."
    - "Do not open a PR."
    - "Do not change CI or GitHub Actions."
    - "Do not edit pyproject.toml Ruff rule selection."
    - "Do not enable blocking Ruff rules."
    - "Do not run Ruff autofix or unsafe fixes."
    - "Do not create or commit a measurement report in this Codex B pass."
    - "Do not change parser behavior, promote fixtures, change corpus status, or activate #388/#381."
    - "Do not claim CI readiness, parser truth, corpus readiness, security/privacy assurance, release readiness, deploy readiness, production readiness, analytics truth, AI truth, or coaching truth."
```
