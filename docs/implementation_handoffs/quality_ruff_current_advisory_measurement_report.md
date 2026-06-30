# Quality Ruff Current Advisory Measurement Report Handoff

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/584

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/567

## Project Roadmap

https://github.com/Tahjali11/Mythic-Edge/issues/568

## Contract

`docs/contracts/quality_ruff_current_advisory_measurement_report.md`

## Internal Project Area

Quality / Governance.

## Truth Owner

Ruff output is static-analysis evidence only. This pass does not own parser
truth, corpus truth, CI readiness, release readiness, deploy readiness,
production readiness, security assurance, privacy assurance, analytics truth,
AI truth, or coaching truth.

## Bridge-Code Status

`not_bridge_code`

## Role Performed

Codex C: Contract-limited measurement / report implementer.

## Target Verification

- Repository: `Tahjali11/Mythic-Edge`
- Target ref: `origin/main`
- Authorized target commit:
  `97f7d9ced74410d03fe4b94ba9f6dc3257bc6a5f`
- Measured checkout commit:
  `97f7d9ced74410d03fe4b94ba9f6dc3257bc6a5f`
- Working branch:
  `codex/quality-ruff-current-advisory-measurement-584`
- Ruff version: `ruff 0.15.12`

The primary checkout was dirty and on a gone branch, so this pass used a clean
dedicated issue worktree from `origin/main`.

## Measurement Status

`measurement_blocked_local_path_leak`

The contracted all-rules advisory Ruff command ran with `--exit-zero` and
wrote JSON under ignored `_review_*/` local evidence storage:

```bash
python3 -m ruff check src tests tools --select ALL --exit-zero --output-format json > _review_/quality_ruff_advisory/2026-06-29-97f7d9c-local-macos-r1/ruff-all.json
```

Ruff exited 0. It emitted compatibility warnings for `D203`/`D211` and
`D212`/`D213`; no CI, Ruff config, source, parser, corpus, workbook, webhook,
Apps Script, analytics, AI, coaching, release, deploy, or production behavior
changed.

The raw JSON was valid. A local aggregate inspection showed:

- available exact Ruff rule codes from `ruff rule --all`: 956
- advisory findings in the raw all-rules scan: 17,576
- triggered exact rule codes in the raw all-rules scan: 115

These numbers are diagnostic context only. They are not an adopted sanitized
report because the helper rejected the input before public report creation.

## Blocker

`tools/generate_ruff_advisory_report.py` failed closed with:

```text
measurement_blocked_local_path_leak
```

Reason: Ruff `0.15.12` JSON diagnostics emitted local absolute filenames for
diagnostic records. A focused `D103` reproduction confirmed this is native Ruff
JSON behavior in this checkout, not a side effect of the all-rules scan.

The contract lists local absolute paths in raw Ruff JSON/helper output as a
stop condition. I did not normalize those paths through an uncontracted
sidecar, did not patch the helper, and did not adopt a sanitized report.

## Files Changed

- `docs/implementation_handoffs/quality_ruff_current_advisory_measurement_report.md`

No runtime code, tests, CI config, Ruff config, parser behavior, corpus
metadata, or generated public report artifact changed.

## Generated Local Evidence

Ignored local evidence remains under:

```text
_review_/quality_ruff_advisory/2026-06-29-97f7d9c-local-macos-r1/
```

Contents are not staged and are ignored by Git:

- raw all-rules Ruff JSON;
- focused `D103` reproduction JSON;
- temporary Ruff rule catalog JSON;
- temporary exact rule-code list.

These files must stay local/uncommitted and must not be pasted into issues,
PRs, comments, trackers, or public docs.

## Validation Run

Passed:

```bash
git fetch --prune origin
git rev-parse origin/main
git status --short --branch --untracked-files=all
python3 -m ruff --version
python3 -m ruff check src tests tools --select ALL --exit-zero --output-format json > _review_/quality_ruff_advisory/2026-06-29-97f7d9c-local-macos-r1/ruff-all.json
python3 -m json.tool _review_/quality_ruff_advisory/2026-06-29-97f7d9c-local-macos-r1/ruff-all.json >/dev/null
python3 -m ruff rule --all --output-format json > _review_/quality_ruff_advisory/2026-06-29-97f7d9c-local-macos-r1/ruff-rules.json
python3 -m json.tool _review_/quality_ruff_advisory/2026-06-29-97f7d9c-local-macos-r1/ruff-rules.json >/dev/null
```

Blocked as designed:

```bash
python3 tools/generate_ruff_advisory_report.py --input _review_/quality_ruff_advisory/2026-06-29-97f7d9c-local-macos-r1/ruff-all.json --rule-codes-file _review_/quality_ruff_advisory/2026-06-29-97f7d9c-local-macos-r1/ruff-rule-codes.json --branch-or-ref origin/main --commit 97f7d9ced74410d03fe4b94ba9f6dc3257bc6a5f --ruff-version 'ruff 0.15.12' --scan-scope src tests tools --command 'python3 -m ruff check src tests tools --select ALL --exit-zero --output-format json'
```

Result:

```text
ERROR: measurement_blocked_local_path_leak
```

No sanitized report was adopted.

Public artifact validation passed:

```bash
printf '%s\n' docs/implementation_handoffs/quality_ruff_current_advisory_measurement_report.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' docs/implementation_handoffs/quality_ruff_current_advisory_measurement_report.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
printf '%s\n' docs/implementation_handoffs/quality_ruff_current_advisory_measurement_report.md | python3 tools/select_validation.py --base origin/main --paths-from-stdin --format text
python3 tools/check_agent_docs.py
python3 -m ruff check src tests tools --no-cache
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q tests/test_ruff_advisory_report.py
git diff --check
```

Results:

- secret/private-marker scan: passed; `forbidden: 0`, `warnings: 0`;
- protected-surface gate: passed; `forbidden: 0`, `warnings: 0`;
- validation selector: `selection_status: ok`;
- agent docs checker: passed;
- normal Ruff check: passed;
- helper tests: 23 passed;
- diff check: passed;
- handoff whitespace/final-newline scan: passed.

## Still Unverified

- No committed sanitized Ruff advisory report exists for issue #584.
- Zero-baseline candidates were not adopted because helper processing stopped
  before public report generation.
- Whether the helper may safely normalize absolute filenames under the measured
  repo root to repo-relative filenames requires a contract clarification.
- No CI or blocking Ruff promotion was attempted.

## Recommended Next Role

Codex B: Module Contract Writer, to clarify whether issue #584/#582 should
allow `tools/generate_ruff_advisory_report.py` or a pre-helper step to
normalize Ruff-emitted absolute filenames to repo-relative paths when they are
provably under the measured clean checkout.

If that clarification is approved, route to Codex D or Codex C for the
smallest helper/report update. If the current stop condition remains
intentional, issue #584 should remain blocked without a sanitized report.

## Pasteable Codex B Prompt

```text
Use the Mythic Edge workflow rules.

Act as Codex B: Module Contract Writer for issue #584.

Repository:
Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/584

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/567

Source contract:
docs/contracts/quality_ruff_current_advisory_measurement_report.md

Implementation handoff:
docs/implementation_handoffs/quality_ruff_current_advisory_measurement_report.md

Problem:
Codex C ran the authorized all-rules Ruff advisory measurement on origin/main
at 97f7d9ced74410d03fe4b94ba9f6dc3257bc6a5f. Ruff 0.15.12 emitted JSON
diagnostics with local absolute filenames. The existing helper correctly failed
closed with measurement_blocked_local_path_leak, so no sanitized report was
adopted.

Goal:
Clarify the contract boundary for Ruff-emitted absolute filenames. Decide
whether a future helper or pre-helper step may normalize filenames under the
measured clean checkout to repo-relative paths while still rejecting paths
outside the checkout, private markers, secrets, raw snippets, autofix output,
and readiness/truth/assurance claims.

Do not:
- change CI;
- edit pyproject.toml;
- enable blocking Ruff rules;
- run autofix or unsafe-fix;
- perform broad cleanup;
- change parser behavior;
- activate #388/#381;
- claim readiness, truth, or assurance.

Expected output:
- contract clarification or follow-up contract;
- explicit route to Codex D/C if helper behavior should change;
- preserved report-only/advisory-only boundaries.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/584"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/567"
  project_roadmap: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/582"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/583"
  previous_merge_commit: "97f7d9ced74410d03fe4b94ba9f6dc3257bc6a5f"
  completed_thread: "C"
  next_thread: "B"
  source_artifact: "docs/contracts/quality_ruff_current_advisory_measurement_report.md"
  target_artifact: "docs/implementation_handoffs/quality_ruff_current_advisory_measurement_report.md"
  verdict: "measurement_blocked_local_path_leak_contract_clarification_needed"
  risk_tier: "High"
  base_branch: "main"
  target_branch: "main"
  branch: "codex/quality-ruff-current-advisory-measurement-584"
  target_ref: "origin/main"
  target_commit: "97f7d9ced74410d03fe4b94ba9f6dc3257bc6a5f"
  ruff_measurement_execution_authorized: true
  report_artifact_creation_authorized: true
  sanitized_report_created: false
  raw_ruff_json_committed: false
  ci_change_authorized: false
  ruff_blocking_promotion_authorized: false
  ruff_autofix_authorized: false
  parser_behavior_change_authorized: false
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
```

## Codex C Continuation Status Check - 2026-06-29

## Role Performed

Codex C: Implementation continuation / status check.

## Local WIP Summary

The local WIP contains a contract clarification, helper/test updates, and this
handoff. The filename-normalization helper fix is present and focused tests
pass, but the lane is not ready for report adoption.

The branch is one commit behind `origin/main` after fetch. The additional
`origin/main` commit is unrelated to the scoped #584 WIP, so no branch sync,
stash, reset, or cleanup was performed.

## Continuation Finding

`RUFF-MEASURE-C-001`: the existing raw all-rules Ruff measurement still cannot
be converted into an adopted sanitized report under the current contract.

Evidence:

```text
python3 tools/generate_ruff_advisory_report.py ... --measured-checkout-root .
```

Result:

```text
ERROR: measurement_blocked_local_path_leak
```

A no-echo diagnostic pass over the ignored local raw Ruff JSON showed:

- 17,576 Ruff records inspected;
- 5 records still fail with `measurement_blocked_local_path_leak`;
- 76 records fail with `measurement_blocked_private_marker`;
- affected rule codes are limited to diagnostic metadata classification and
  are not an adopted report.

The remaining failure is not the Ruff diagnostic `filename` field fixed by
the D addendum. It is Ruff diagnostic message content. Because the current
contract still treats local-path text and private-marker vocabulary in Ruff
messages as a fail-closed condition, Codex C did not change the helper to
ignore, redact, hash, or omit messages beyond the existing contract.

## Continuation Validation Run

Passed:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q tests/test_ruff_advisory_report.py
python3 -m ruff check src tests tools --no-cache
python3 -m py_compile tools/generate_ruff_advisory_report.py tests/test_ruff_advisory_report.py
printf '%s\n' docs/contracts/quality_ruff_current_advisory_measurement_report.md docs/implementation_handoffs/quality_ruff_current_advisory_measurement_report.md tools/generate_ruff_advisory_report.py tests/test_ruff_advisory_report.py | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' docs/contracts/quality_ruff_current_advisory_measurement_report.md docs/implementation_handoffs/quality_ruff_current_advisory_measurement_report.md tools/generate_ruff_advisory_report.py tests/test_ruff_advisory_report.py | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
printf '%s\n' docs/contracts/quality_ruff_current_advisory_measurement_report.md docs/implementation_handoffs/quality_ruff_current_advisory_measurement_report.md tools/generate_ruff_advisory_report.py tests/test_ruff_advisory_report.py | python3 tools/select_validation.py --base origin/main --paths-from-stdin --format text
python3 tools/check_agent_docs.py
git diff --check
```

Results:

- helper tests: 34 passed;
- Ruff: passed;
- py_compile: passed;
- changed-file secret/private-marker scan: passed with `forbidden: 0`,
  `warnings: 0`;
- changed-file protected-surface gate: passed with `forbidden: 0`,
  `warnings: 0`;
- validation selector: `selection_status: ok`;
- agent docs checker: passed with `errors: 0`, `warnings: 0`;
- diff check: passed.

Advisory-only:

```bash
python3 tools/run_pyright_advisory_report.py
```

Result: advisory findings remain (`errors: 402`), with
`gate_behavior: advisory_non_blocking`.

Blocked as designed:

```bash
python3 tools/generate_ruff_advisory_report.py ... --measured-checkout-root .
```

Result: `ERROR: measurement_blocked_local_path_leak`.

## Files Changed In Local WIP

- `docs/contracts/quality_ruff_current_advisory_measurement_report.md`
- `docs/implementation_handoffs/quality_ruff_current_advisory_measurement_report.md`
- `tools/generate_ruff_advisory_report.py`
- `tests/test_ruff_advisory_report.py`

Ignored raw Ruff evidence remains local under `_review_*/` and is ignored by
Git. No sanitized report artifact was created or adopted.

## Updated Recommendation

Recommended next role: Codex B.

Reason: the remaining blocker is contract-level. To adopt a sanitized report,
the workflow must decide whether Ruff diagnostic message fields may be
excluded from public summaries, symbolically classified, or redacted when the
helper does not output messages. Without that clarification, the current
fail-closed behavior is correct and issue #584 remains blocked from producing
an adopted report.

## Pasteable Codex B Prompt

```text
Use the Mythic Edge workflow rules.

Act as Codex B: Module Contract Writer for issue #584.

Repository:
Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/584

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/567

Project roadmap:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Source contract:
docs/contracts/quality_ruff_current_advisory_measurement_report.md

Implementation handoff:
docs/implementation_handoffs/quality_ruff_current_advisory_measurement_report.md

Problem:
The bounded Ruff diagnostic filename normalization helper fix passes focused
tests, but the existing raw all-rules Ruff measurement still fails closed
before sanitized report adoption. Ruff diagnostic message content contains
local-path and private-marker vocabulary. The helper does not output messages,
but the current contract still treats those raw message values as stop
conditions.

Goal:
Clarify whether sanitized Ruff advisory reports may ignore, symbolically
classify, or redact diagnostic message fields that are not emitted in the
public summary, while still rejecting secrets, raw source snippets, fix edits,
paths outside the measured checkout, private/generated artifact paths, raw
logs, raw private payloads, and readiness/truth/assurance claims.

Do not:
- run a fresh all-rules Ruff measurement;
- create or adopt a sanitized report artifact;
- change CI;
- edit pyproject.toml;
- enable blocking Ruff rules;
- run autofix or unsafe-fix;
- perform broad cleanup;
- change parser behavior;
- activate #388/#381;
- claim parser truth, security/privacy assurance, release readiness, deploy
  readiness, production readiness, analytics truth, AI truth, or coaching
  truth.

Expected output:
- contract clarification or explicit decision to keep the current blocker;
- route to Codex D/C only if helper behavior should change;
- preserved advisory-only/report-only boundaries.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/584"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/567"
  project_roadmap: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/582"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/583"
  previous_merge_commit: "97f7d9ced74410d03fe4b94ba9f6dc3257bc6a5f"
  completed_thread: "C"
  next_thread: "B"
  source_artifact: "docs/contracts/quality_ruff_current_advisory_measurement_report.md"
  target_artifact: "docs/implementation_handoffs/quality_ruff_current_advisory_measurement_report.md"
  finding_id: "RUFF-MEASURE-C-001"
  verdict: "ruff_measurement_message_content_blocker_requires_contract_clarification"
  risk_tier: "High"
  branch: "codex/quality-ruff-current-advisory-measurement-584"
  sanitized_report_created: false
  raw_ruff_json_committed: false
  ci_change_authorized: false
  ruff_blocking_promotion_authorized: false
  ruff_autofix_authorized: false
  parser_behavior_change_authorized: false
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
```

## Codex D Fixer Addendum

## Role Performed

Codex D: Module Fixer.

## Contract Clarification Used

Codex B clarified that Ruff-native diagnostic `filename` values may be
normalized from absolute paths to repo-relative paths only when the measured
checkout root is known and the resolved diagnostic file is under that checkout.
The exception applies only to Ruff diagnostic filename fields.

The clarification does not authorize a fresh all-rules Ruff measurement, a
sanitized report artifact, CI changes, blocking Ruff promotion, Ruff autofix,
parser behavior changes, corpus promotion, or readiness/truth/assurance claims.

## Fix Summary

`tools/generate_ruff_advisory_report.py` now accepts an optional
`--measured-checkout-root` argument and uses it only to normalize Ruff
diagnostic `filename` fields. Absolute filenames that resolve under that root
become repo-relative forward-slash paths in helper output.

Codex D also addressed `RUFF-MEASURE-E-001`: the measured checkout root could
be too broad, allowing a sibling path under the same parent directory to
normalize into a public-looking relative path. The helper now requires the
measured root to look like the actual repository checkout root before it can
normalize absolute Ruff diagnostic filenames.

Codex D also addressed `RUFF-MEASURE-E-002`: double-slash and UNC-like Ruff
diagnostic filenames such as `//server/share/src/example.py` and
`\\server\share\src\example.py` were not treated as absolute/local paths and
could normalize into public-looking paths such as `server/share/src/example.py`.
The helper now rejects those path shapes before diagnostic filename
normalization, and the generic local-path detector treats double-slash and
UNC-like tokens as local/private path text.

Codex D also addressed `RUFF-MEASURE-E-003`: URI/scheme-like Ruff diagnostic
filenames were still treated as repo-relative input and could normalize into
public-looking pseudo paths. The helper now rejects scheme-shaped diagnostic
filename values before any repo-relative normalization or public report output.

Codex D follow-up also addressed `RUFF-MEASURE-E-004`: the URI/scheme detector
still missed single-colon scheme path separators. The helper now rejects
two-or-more-letter scheme path prefixes with one or more slashes before any
repo-relative normalization, while preserving one-letter Windows-drive handling
for the existing absolute-path branch.

Codex D follow-up also applied the clarified diagnostic-message boundary from
issue #584: raw Ruff diagnostic `message` text is required as input shape but
is no longer stored in public finding state or emitted in helper output.
Un-emitted messages that contain local-path wording or private-marker
vocabulary may be ignored, while diagnostic messages with secret-shaped text,
raw source/fix payloads, raw private payload markers, or readiness/truth/
assurance overclaims still fail closed symbolically without echoing submitted
message text.

Codex D follow-up also addressed `RUFF-MEASURE-E-005`: quoted secret-like
field shapes such as JSON-ish API-key, access-token, client-secret, and
webhook-URL assignments were not fully covered. The helper now detects
quoted secret-like assignment text in metadata or diagnostic messages, and it
recursively scans raw Ruff record payloads for secret-like field names before
known Ruff fields are parsed. Rejections stay symbolic through
`measurement_blocked_secret_like_output` and do not echo submitted values.

Codex D follow-up also addressed `RUFF-MEASURE-E-006`: the string-form
quoted API-key detector still accepted a spaced field label such as
`"api key": "<token-like value>"` in metadata command text and Ruff diagnostic
message text. The string-form assignment detector now treats a space between
`api` and `key` like the existing underscore and hyphen variants, while the
raw-record object-key path remains unchanged.

The helper still fails closed when:

- the measured checkout root is not the actual repo checkout root;
- a diagnostic filename is outside the measured checkout;
- a diagnostic filename uses a double-slash or UNC-like path shape;
- a diagnostic filename uses a URI/scheme-like path shape, including
  single-colon scheme paths;
- a diagnostic filename normalizes into generated/private artifact paths such
  as `_review_*/` or `data/`;
- a diagnostic message contains secret-like values, raw source snippets, fix
  edits, raw private payload markers, or readiness/truth/assurance overclaims;
- a diagnostic message, metadata command, or raw Ruff record contains quoted
  secret-like field assignments or secret-like extra field names;
- a metadata command or diagnostic message contains a quoted spaced API-key
  field assignment;
- metadata, commands, private markers, secret-like values, or autofix flags
  violate the existing public-safety rules.

No raw Ruff JSON was committed, no sanitized measurement report was created,
and the all-rules Ruff measurement was not rerun in this D pass.

## Files Changed By D

- `tools/generate_ruff_advisory_report.py`
- `tests/test_ruff_advisory_report.py`
- `docs/implementation_handoffs/quality_ruff_current_advisory_measurement_report.md`

## Focused Coverage Added

- absolute Ruff diagnostic filename under measured checkout normalizes to a
  repo-relative output path without echoing the checkout root;
- absolute Ruff diagnostic filename outside measured checkout fails closed with
  `measurement_blocked_path_outside_checkout`;
- too-broad measured checkout root fails closed with
  `measurement_blocked_path_normalization_unsupported`;
- diagnostic filename under generated/private `_review_*/` output fails closed;
- local-path wording and private-marker vocabulary in un-emitted Ruff
  diagnostic messages do not block and do not appear in rendered output;
- raw source snippets and fix-edit-shaped diagnostic messages fail closed with
  `measurement_blocked_raw_source_snippet_public` without echoing submitted
  message text;
- readiness/truth/assurance overclaim diagnostic messages fail closed with
  `measurement_blocked_raw_output_public` without echoing submitted message
  text;
- CLI normalization through `--measured-checkout-root` does not echo the raw
  absolute filename or checkout root.
- CLI output does not emit Ruff diagnostic message text, local paths embedded
  in messages, or private-marker vocabulary embedded in messages;
- double-slash and UNC-like diagnostic filenames fail closed before they can
  normalize into public-looking repo-relative paths;
- CLI rejection for double-slash diagnostic filenames stays symbolic and does
  not echo the unsafe submitted path.
- URI/scheme-like diagnostic filenames fail closed before they can normalize
  into public-looking pseudo repo-relative paths;
- direct helper and CLI rejection for URI/scheme-like diagnostic filenames
  stays symbolic and does not echo the unsafe submitted value.
- single-colon URI/scheme-like diagnostic filenames fail closed through direct
  helper and CLI paths;
- one-letter Windows-drive-like paths are not classified by the URI/scheme
  detector.
- quoted secret-like API-key, access-token, client-secret, and webhook-URL
  assignment shapes fail closed in metadata and diagnostic-message paths
  without echoing submitted values;
- extra raw Ruff JSON fields with secret-like names fail closed recursively
  before ignored fields can bypass validation.
- quoted spaced API-key assignment text fails closed in both metadata command
  and diagnostic-message paths without echoing the submitted field value.

## Validation Run By D

Passed:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q tests/test_ruff_advisory_report.py
python3 -m ruff check tools/generate_ruff_advisory_report.py tests/test_ruff_advisory_report.py
python3 -m py_compile tools/generate_ruff_advisory_report.py tests/test_ruff_advisory_report.py
python3 -m ruff check src tests tools --no-cache
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q
printf '%s\n' tools/generate_ruff_advisory_report.py tests/test_ruff_advisory_report.py | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' tools/generate_ruff_advisory_report.py tests/test_ruff_advisory_report.py | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
printf '%s\n' docs/contracts/quality_ruff_current_advisory_measurement_report.md docs/implementation_handoffs/quality_ruff_current_advisory_measurement_report.md tools/generate_ruff_advisory_report.py tests/test_ruff_advisory_report.py | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' docs/contracts/quality_ruff_current_advisory_measurement_report.md docs/implementation_handoffs/quality_ruff_current_advisory_measurement_report.md tools/generate_ruff_advisory_report.py tests/test_ruff_advisory_report.py | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
python3 tools/check_agent_docs.py
git diff --check
awk '/[ \t]$/ {print FILENAME ":" FNR ": trailing whitespace"; bad=1} END {exit bad}' docs/implementation_handoffs/quality_ruff_current_advisory_measurement_report.md
```

Results:

- helper tests: 38 passed;
- direct quoted secret-like field probes: passed;
- direct spaced quoted API-key assignment probes: passed;
- focused Ruff check: passed;
- py_compile: passed;
- repo Ruff check: passed;
- full pytest suite: 1987 passed;
- changed-code secret/private-marker scan: passed with `forbidden: 0`,
  `warnings: 0`;
- changed-code protected-surface scan: passed with `forbidden: 0`,
  `warnings: 0`;
- full visible-diff secret/private-marker scan: passed with `forbidden: 0`,
  `warnings: 0`;
- full visible-diff protected-surface scan: passed with `forbidden: 0`,
  `warnings: 0`;
- agent docs consistency check: passed with `errors: 0`, `warnings: 0`;
- diff check: passed.
- new handoff whitespace/final-newline check: passed.

## Still Not Performed

- no all-rules Ruff measurement rerun;
- no sanitized report artifact creation;
- no raw Ruff JSON commit;
- no CI change;
- no blocking Ruff rule promotion;
- no Ruff autofix;
- no parser behavior, corpus, workbook, webhook, Apps Script, analytics, AI,
  coaching, release, deploy, or production behavior change.

## Recommended Next Role

Codex E: Module Reviewer / contract-test mode for the D helper fix.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge workflow rules.

Act as Codex E: Module Reviewer for issue #584.

Repository:
Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/584

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/567

Branch:
codex/quality-ruff-current-advisory-measurement-584

Source contract:
docs/contracts/quality_ruff_current_advisory_measurement_report.md

Implementation handoff:
docs/implementation_handoffs/quality_ruff_current_advisory_measurement_report.md

Review scope:
Review only the Codex D helper/test fix for bounded Ruff diagnostic filename
normalization and the clarified diagnostic-message boundary. Confirm absolute
Ruff diagnostic filename fields under the measured checkout root normalize to
repo-relative output paths, while paths outside the checkout, double-slash or
UNC-like diagnostic filenames, URI/scheme-like diagnostic filenames including
single-colon scheme paths, and generated/private artifact paths still fail
closed. Confirm raw Ruff diagnostic messages are never emitted; local-path
wording and private-marker vocabulary inside un-emitted messages may be
ignored, while secret-shaped text, raw source/fix payloads, raw private payload
markers, and readiness/truth/assurance overclaims still fail closed
symbolically without unsafe value echo. Confirm quoted secret-like field
assignments in metadata or diagnostic messages, and secret-like extra raw Ruff
record field names, fail closed symbolically without unsafe value echo. Confirm
spaced quoted API-key field labels such as `"api key"` also fail closed in
string-form metadata and diagnostic-message paths.

Do not rerun the all-rules Ruff measurement unless explicitly authorized.
Do not create a sanitized report artifact.
Do not commit raw Ruff JSON.
Do not change CI, pyproject, blocking Ruff gates, parser behavior, corpus
status, workbook/webhook/Apps Script behavior, analytics, AI, coaching,
release, deploy, or production behavior.
Do not claim readiness, truth, privacy assurance, or security assurance.

Suggested validation:
- PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q tests/test_ruff_advisory_report.py
- python3 -m ruff check src tests tools --no-cache
- printf '%s\n' tools/generate_ruff_advisory_report.py tests/test_ruff_advisory_report.py docs/implementation_handoffs/quality_ruff_current_advisory_measurement_report.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
- printf '%s\n' tools/generate_ruff_advisory_report.py tests/test_ruff_advisory_report.py docs/implementation_handoffs/quality_ruff_current_advisory_measurement_report.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
- git diff --check

Output:
- Findings first.
- Whether the D fix satisfies the clarified filename-normalization and
  diagnostic-message contract.
- Any remaining blocker or non-blocking risk.
- Next recommended role.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/584"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/567"
  project_roadmap: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/582"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/583"
  previous_merge_commit: "97f7d9ced74410d03fe4b94ba9f6dc3257bc6a5f"
  completed_thread: "D"
  next_thread: "E"
  source_artifact: "docs/contracts/quality_ruff_current_advisory_measurement_report.md"
  target_artifact: "tools/generate_ruff_advisory_report.py; tests/test_ruff_advisory_report.py; docs/implementation_handoffs/quality_ruff_current_advisory_measurement_report.md"
  finding_id: "RUFF-MEASURE-E-006"
  verified_fixed:
    - "RUFF-MEASURE-E-001"
    - "RUFF-MEASURE-E-002"
    - "RUFF-MEASURE-E-003_for_scheme_double_slash_shapes"
    - "RUFF-MEASURE-E-004"
    - "RUFF-MEASURE-E-005"
  verdict: "ruff_measurement_spaced_quoted_api_key_assignment_fix_ready_for_review"
  risk_tier: "High"
  base_branch: "main"
  target_branch: "main"
  branch: "codex/quality-ruff-current-advisory-measurement-584"
  sanitized_report_created: false
  raw_ruff_json_committed: false
  ci_change_authorized: false
  ruff_blocking_promotion_authorized: false
  ruff_autofix_authorized: false
  ruff_measurement_execution_authorized: false
  report_artifact_creation_authorized: false
  parser_behavior_change_authorized: false
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
```
