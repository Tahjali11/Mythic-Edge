# Quality Ruff Advisory Report Helper Handoff

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/578

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/567

## Contract

`docs/contracts/quality_ruff_advisory_zero_baseline_design.md`

## Internal Project Area

Quality / Governance.

## Truth Owner

Ruff output is static-analysis evidence only. The helper does not own parser
truth, analytics truth, AI truth, coaching truth, CI readiness, release
readiness, deploy readiness, production readiness, security assurance, or
privacy assurance.

## Bridge-Code Status

`not_bridge_code`

## Role Performed

Codex C: Module Implementer.

Codex D: Module Fixer for `RUFF-ADVISORY-E-001`,
`RUFF-ADVISORY-E-002`, `RUFF-ADVISORY-E-003`, and
`RUFF-ADVISORY-E-004`.

## What Changed

Implemented a small local helper that consumes already-produced Ruff JSON and
emits a deterministic, sanitized advisory summary envelope. The helper does not
run Ruff, does not run autofix, does not edit source files, and does not enable
blocking rules.

## Files Changed

- `tools/generate_ruff_advisory_report.py`
- `tests/test_ruff_advisory_report.py`
- `docs/implementation_handoffs/quality_ruff_advisory_report_helper.md`

## Code Changed

Runtime product code did not change. The added helper is a local Quality /
Governance tool.

Implemented behavior:

- parses Ruff JSON diagnostics from `--input` or stdin;
- emits `mythic_edge_quality_ruff_advisory_report` with schema
  `quality_ruff_advisory_report.v1`;
- summarizes exact rule-code counts;
- records triggered rule-code totals and zero-baseline exact-code candidates;
- rejects broad-family candidate inference;
- rejects malformed Ruff JSON, unsupported rule records, local absolute paths,
  private markers, and secret-like output;
- preserves repo-relative paths only;
- classifies protected-surface impact conservatively;
- keeps autofix metadata as evidence only;
- includes explicit non-claims.

Codex D follow-up behavior:

- validates public report metadata before rendering it;
- rejects local absolute paths in scan scope, commands, repository metadata,
  branch/ref metadata, commit metadata, and Ruff-version metadata;
- rejects secret-like values and private markers in public metadata;
- rejects command metadata containing `--fix` or `--unsafe-fixes`;
- keeps failure output to reason codes only so rejected private values are not
  echoed to stderr.

Codex D rebound behavior for remaining `RUFF-ADVISORY-E-002` and
`RUFF-ADVISORY-E-003` blockers:

- local-path detection now blocks generic Unix absolute paths such as
  `/tmp/ruff.json` and generic Windows absolute paths such as
  `D:\tmp\ruff.json` in public command metadata;
- local-path detection remains token-based so safe `https://github.com/...`
  repository URLs are not misclassified as local paths;
- autofix metadata now rejects `--fix=...`, `--fix-only`, and
  `--unsafe-fixes=...` variants in addition to exact `--fix` and
  `--unsafe-fixes` flags.

Codex D second rebound behavior for remaining `RUFF-ADVISORY-E-003`:

- secret-like token detection now rejects bare bearer/basic/token credential
  forms, authorization headers, token-bearing command flags, common token
  assignments, and GitHub token prefixes in public metadata and Ruff message
  text;
- CLI rejection still prints only the fail-closed reason code and does not echo
  the rejected token value.

Codex D third rebound behavior for remaining `RUFF-ADVISORY-E-003`:

- secret-like token detection now rejects AWS-style access key ID shapes with
  common `AKIA` and `ASIA` prefixes in public metadata and Ruff message text;
- regression coverage constructs the synthetic key shapes from fragments so no
  raw credential-shaped literal is committed in the tests.

Codex D fourth rebound behavior for remaining `RUFF-ADVISORY-E-003`:

- secret-like token detection now rejects quoted assignment and quoted command
  flag values such as token/API-key/secret assignments in public metadata and
  Ruff message text;
- regression coverage constructs quoted token-shaped values from fragments so
  no raw secret-looking literal is committed in the tests.

Codex D fifth rebound behavior for remaining `RUFF-ADVISORY-E-003`:

- secret-like token detection now rejects credential/credentials assignments
  and webhook URL assignments in public metadata and Ruff message text;
- regression coverage constructs webhook-shaped field names from fragments so
  no raw webhook marker is committed in the tests.

Codex D sixth rebound behavior for remaining `RUFF-ADVISORY-E-003`:

- secret-like token detection now rejects `secret_key` assignment variants in
  public metadata and Ruff message text;
- regression coverage constructs the synthetic key field names from fragments
  so no raw secret-key-shaped example is committed in tests.

Codex D seventh rebound behavior for still-reproducing
`RUFF-ADVISORY-E-003`:

- secret-like token detection now rejects quoted `secret_key` keys and
  alternate assignment operators such as `:=` and `=>` in public metadata and
  Ruff message text;
- the focused secret-key regression was expanded with JSON-like quoted key
  shapes and alternate assignment operators.

Codex D behavior for `RUFF-ADVISORY-E-004`:

- unreadable `--input` paths now fail closed with the symbolic
  `measurement_blocked_input_unreadable` reason instead of printing the raw
  path-bearing operating-system error;
- unreadable `--rule-codes-file` paths use the same symbolic failure path;
- malformed rule-code files now fail closed with
  `candidate_rejected_broad_family` instead of printing raw JSON parser text.

## Tests Added Or Updated

- Added focused synthetic tests for:
  - valid Ruff JSON summary generation;
  - exact-code zero-baseline candidate selection;
  - nonzero advisory classification;
  - protected-surface classification;
  - broad-family candidate rejection;
  - malformed JSON rejection;
  - unsupported rule record rejection;
  - local absolute path rejection;
  - secret-like output rejection;
  - private marker rejection;
  - CLI output and failure behavior.
- Codex D added regression tests for:
  - metadata scan-scope local path rejection;
  - command metadata local path rejection;
  - generic Unix and Windows absolute paths in command metadata;
  - command metadata secret/private marker rejection;
  - command metadata autofix flag rejection;
  - command metadata autofix flag variant rejection;
  - bearer/token/GitHub-prefix secret-like token rejection in metadata and Ruff
    message text;
  - AWS-style access key ID shape rejection in metadata and Ruff message text;
  - quoted assignment/flag secret-like token rejection in metadata and Ruff
    message text;
  - credential assignment and webhook URL secret-like rejection in metadata and
    Ruff message text;
  - CLI metadata rejection without echoing the rejected private value.
  - CLI secret-like token rejection without echoing the rejected token value.
  - CLI Ruff input read errors without echoing the rejected input path.
  - CLI rule-code input read errors without echoing the rejected input path.

## Interface Changes

New local CLI:

```bash
python3 tools/generate_ruff_advisory_report.py --input <ruff-json-file>
```

Optional metadata flags:

- `--rule-code <EXACT_RULE_CODE>`
- `--rule-codes-file <json-list-file>`
- `--branch-or-ref <ref>`
- `--commit <sha>`
- `--ruff-version <version>`
- `--scan-scope <paths...>`
- `--command <command-text>`

The helper writes the sanitized summary to stdout only.

## Contracted Area Status

The implementation stayed inside the Quality / Governance contract boundary.
No CI, Ruff config, parser, runtime, workbook, webhook, Apps Script, analytics,
AI, coaching, fixture, corpus, or private-evidence surface was changed.

## Validation Run

Passed:

```bash
python3 -m pytest -q tests/test_ruff_advisory_report.py
```

Result: passed, 15 tests after Codex D public-safety rebound coverage.

```bash
python3 -m py_compile tools/generate_ruff_advisory_report.py tests/test_ruff_advisory_report.py
```

Result: passed.

```bash
python3 -m ruff check src tests tools
```

Result: passed.

```bash
printf '%s\n' tools/generate_ruff_advisory_report.py tests/test_ruff_advisory_report.py docs/implementation_handoffs/quality_ruff_advisory_report_helper.md | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
```

Result: passed; `forbidden: 0`, `warnings: 0`.

```bash
printf '%s\n' tools/generate_ruff_advisory_report.py tests/test_ruff_advisory_report.py docs/implementation_handoffs/quality_ruff_advisory_report_helper.md | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
```

Result: passed; `forbidden: 0`, `warnings: 0`.

```bash
printf '%s\n' tools/generate_ruff_advisory_report.py tests/test_ruff_advisory_report.py docs/implementation_handoffs/quality_ruff_advisory_report_helper.md | python3 tools/select_validation.py --base origin/main --paths-from-stdin --format text
```

Result: `selection_status: ok`.

```bash
python3 tools/check_agent_docs.py
```

Result: passed.

```bash
git diff --check
```

Result: passed.

Codex D focused validation:

```bash
python3 -m pytest -q tests/test_ruff_advisory_report.py
```

Result: passed, 14 tests.

Codex D rebound validation:

```bash
python3 -m pytest -q tests/test_ruff_advisory_report.py
```

Result: passed, 15 tests.

Codex D second rebound validation:

```bash
python3 -m pytest -q tests/test_ruff_advisory_report.py
```

Result: passed, 17 tests.

Codex D third rebound validation:

```bash
python3 -m pytest -q tests/test_ruff_advisory_report.py
```

Result: passed, 18 tests.

Codex D fourth rebound validation:

```bash
python3 -m pytest -q tests/test_ruff_advisory_report.py
```

Result: passed, 19 tests.

Codex D fifth rebound validation:

```bash
python3 -m pytest -q tests/test_ruff_advisory_report.py
```

Result: passed, 20 tests.

Codex D sixth rebound validation:

```bash
python3 -m pytest -q tests/test_ruff_advisory_report.py
```

Result: passed, 21 tests.

Codex D seventh rebound validation:

```bash
python3 -m pytest -q tests/test_ruff_advisory_report.py
```

Result: passed, 21 tests.

Codex D `RUFF-ADVISORY-E-004` validation:

```bash
python3 -m pytest -q tests/test_ruff_advisory_report.py
```

Result: passed, 23 tests.

Direct repros now fail closed with `measurement_blocked_secret_like_output`:

- bare `Bearer <token-shaped-value>`;
- `Authorization: Bearer <token-shaped-value>`;
- `--token <token-shaped-value>`;
- `--api-key <token-shaped-value>`;
- secret assignment-shaped token text;
- auth-token assignment-shaped token text;
- GitHub `github_pat_...`-shaped tokens;
- GitHub `gho_...`-shaped tokens.
- AWS-style `AKIA...` access key ID shapes;
- AWS-style `ASIA...` temporary access key ID shapes.
- quoted token assignment shapes;
- quoted API-key assignment shapes;
- quoted secret assignment shapes;
- quoted token command-flag shapes.
- credential and credentials assignment shapes;
- webhook URL assignment shapes.
- secret-key assignment shapes.
- quoted secret-key field shapes.
- secret-key alternate assignment operators.
- unreadable `--input` paths without echoing the input path.
- unreadable `--rule-codes-file` paths without echoing the input path.

Direct CLI repros now fail closed with `measurement_blocked_input_unreadable`:

- unreadable `--input`;
- unreadable `--rule-codes-file`.

Direct repros now fail closed:

- command metadata with `/tmp/ruff.json` -> `measurement_blocked_local_path_leak`;
- command metadata with `D:\tmp\ruff.json` -> `measurement_blocked_local_path_leak`;
- command metadata with `--fix=always` -> `autofix_blocked_not_authorized`;
- command metadata with `--unsafe-fixes=true` -> `autofix_blocked_not_authorized`;
- command metadata with `--fix-only` -> `autofix_blocked_not_authorized`.

```bash
python3 -m py_compile tools/generate_ruff_advisory_report.py tests/test_ruff_advisory_report.py
```

Result: passed.

```bash
python3 -m ruff check src tests tools
```

Result: passed.

```bash
python3 tools/check_agent_docs.py
```

Result: passed.

```bash
python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
```

Result: passed for:

- `tools/generate_ruff_advisory_report.py`
- `tests/test_ruff_advisory_report.py`
- `docs/implementation_handoffs/quality_ruff_advisory_report_helper.md`

```bash
python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
```

Result: passed for the same three paths.

```bash
git diff --check
```

Result: passed. Because the changed files are new and untracked, also ran a
direct changed-file trailing-whitespace/final-newline scan over the same three
paths. Result: passed.

```bash
python3 tools/select_validation.py --base origin/main --paths-from-stdin --format text
```

Result: selector status `ok`. Required checks matched the commands above.
Pyright was listed as advisory only and was not run in this Ruff-helper slice.

## Still Unverified

- No live all-rules Ruff advisory scan was run; issue #578 authorizes the helper
  implementation, not a measurement pass.
- No CI behavior was changed or verified.
- No blocking rule promotion was attempted.

## Reviewer Focus

Please verify:

- the helper cannot infer candidates from broad Ruff families;
- malformed, private, local-path, or secret-like Ruff output fails closed;
- summary output cannot be mistaken for CI readiness, parser truth, or security
  assurance;
- protected-surface classification is conservative enough for future review.

## Next Workflow Action

Next role: Codex E.

Pasteable prompt:

```text
Use the Mythic Edge workflow rules.

Act as Codex E: Module Reviewer for issue #578.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/578

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/567

Project roadmap:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Previous issue:
https://github.com/Tahjali11/Mythic-Edge/issues/570

Previous PR:
https://github.com/Tahjali11/Mythic-Edge/pull/571

Source contract:
docs/contracts/quality_ruff_advisory_zero_baseline_design.md

Implementation handoff:
docs/implementation_handoffs/quality_ruff_advisory_report_helper.md

Review goal:
Review the local Ruff advisory report helper, focused tests, and handoff
against issue #578 and the #570 contract. Lead with findings. Confirm the
implementation stays advisory-only and does not change CI, Ruff config, parser
behavior, autofix behavior, or readiness/truth claims.

Validation to review:
- python3 -m pytest -q tests/test_ruff_advisory_report.py
- python3 -m py_compile tools/generate_ruff_advisory_report.py tests/test_ruff_advisory_report.py
- python3 -m ruff check src tests tools
- path-scoped secret/private-marker scan
- path-scoped protected-surface gate
- git diff --check

If clean, route to Codex F. If findings are concrete, route to Codex D. If the
contract is ambiguous, route to Codex B.
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/578"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/567"
  project_roadmap: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  previous_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/570"
  previous_pr: "https://github.com/Tahjali11/Mythic-Edge/pull/571"
  previous_merge_commit: "395bbd36246f65be6639efd0426d356138e904c0"
  completed_thread: "D"
  next_thread: "E"
  verdict: "ruff_advisory_report_helper_ready_for_review"
  fixed_finding_id: "RUFF-ADVISORY-E-004"
  verified_fixed:
    - "RUFF-ADVISORY-E-003"
  risk_tier: "High"
  base_branch: "main"
  branch: "codex/quality-ruff-advisory-report-helper-578"
  source_artifact: "docs/contracts/quality_ruff_advisory_zero_baseline_design.md"
  target_artifact: "docs/implementation_handoffs/quality_ruff_advisory_report_helper.md"
  ci_change_authorized: false
  ruff_blocking_promotion_authorized: false
  ruff_autofix_authorized: false
  parser_behavior_change_authorized: false
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
```
