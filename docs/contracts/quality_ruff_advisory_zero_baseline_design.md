# Quality Ruff Advisory Zero-Baseline Design Contract

## Module

Planning contract for issue #570, the Phase 0 Ruff all-rules advisory scan and
zero-baseline promotion design under quality tracker #567.

Plain English: this contract defines how Mythic Edge may later measure all
available Ruff rules in advisory mode, identify exact rule codes that currently
have zero findings, and route those clean rules toward a separate reviewed
blocking-promotion lane. It does not change CI, enable new blocking rules, run
autofix, fix lint findings, change parser behavior, or claim readiness.

## Source Issue

- Repository: `Tahjali11/Mythic-Edge`
- Repository URL: `https://github.com/Tahjali11/Mythic-Edge`
- Issue: https://github.com/Tahjali11/Mythic-Edge/issues/570
- Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/567
- Project roadmap: https://github.com/Tahjali11/Mythic-Edge/issues/568
- Active parser evidence tracker: https://github.com/Tahjali11/Mythic-Edge/issues/388
- Sibling Phase 0 issue: https://github.com/Tahjali11/Mythic-Edge/issues/569
- Base branch: `main`
- Target branch: `main`
- Working branch: `codex/quality-ruff-advisory-zero-baseline-design-570`
- Risk tier: High

Observed during this Codex B pass:

- The primary checkout contained unrelated local governance/parser-contract
  work, so this contract was written in a clean issue worktree.
- The issue worktree was based on `origin/main` at
  `1ad427447c595550c4d9679941e01b371577dab9`.
- Issue #570 was open.
- Tracker #567 was open.
- Roadmap #568 allowed read-only quality planning before #388 closes, provided
  the work does not mutate source behavior, CI, private evidence, or active
  parser-evidence lanes.

## Source Artifacts Inspected

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- Issue #570
- Tracker #567
- Project roadmap #568
- Active parser evidence tracker #388
- Sibling Phase 0 issue #569
- `pyproject.toml`
- `.github/workflows/repo-checks.yml`
- `tools/run_repo_checks.ps1`
- available top-level `tools/` helpers
- related confidence, corpus automation, and parser-evidence contracts as
  protected-surface references

No private Player.log, UTC_Log, app-data, live MTGA, network, workbook export,
SQLite database, generated runtime artifact, private report, secret, token, or
credential was read, copied, hashed, summarized, or committed.

## Observed Current Behavior

Current Ruff configuration in `pyproject.toml`:

```toml
[tool.ruff.lint]
select = ["E", "F", "I"]
```

Current GitHub Actions behavior runs the blocking repo check:

```text
py -m ruff check src tests tools
```

Current local PowerShell repo check runs:

```text
py -m ruff check src tests
```

There is no repo-owned all-rules Ruff advisory report format, no zero-baseline
candidate artifact, and no exact-code promotion policy in committed docs. The
current blocking Ruff gate is intentionally narrow.

Tracker #567 records an earlier exploratory all-rules advisory observation for
Ruff `0.15.12`:

- available Ruff rule count: `956`
- triggered rule codes: `115`
- zero-baseline rule codes: `841`
- advisory findings: `17312`

Those tracker numbers are planning context only. They are not a current
contract validation result, not a CI baseline, not a readiness claim, and not
authorization to enable or fix any rule.

## Problem

The first bad value is treating "Ruff can report this" as "Ruff should block
this now."

The second bad value is treating a broad family such as `S`, `PL`, `ANN`, or
`D` as clean because some exact codes in that family have zero findings.

The third bad value is treating autofix availability as approval to rewrite
source code.

Without a contract, Mythic Edge could accidentally move from measurement to
enforcement, produce noisy broad cleanup work, or let a style/tooling decision
touch parser truth, private evidence, CI gates, or active #388 work.

## Scope Decision

Selected scope:

```yaml
selected_scope: "phase_0_advisory_measurement_and_zero_baseline_design"
implementation_authorized: false
ci_change_authorized: false
ruff_blocking_promotion_authorized: false
ruff_autofix_authorized: false
parser_behavior_change_authorized: false
```

This contract authorizes only contract language for:

- read-only all-rules Ruff advisory commands;
- advisory exit-code behavior;
- public-safe advisory report shape;
- exact rule-code zero-baseline candidate selection;
- high-signal triggered rule recording;
- protected-surface review criteria;
- later split points for implementation, review, blocking promotion, and CI.

This contract does not authorize:

- a helper implementation;
- committed Ruff output artifacts;
- CI or GitHub Actions edits;
- `pyproject.toml` rule-selection edits;
- Ruff autofix or unsafe-fix execution;
- broad cleanup PRs;
- source edits;
- parser behavior changes;
- fixture promotion;
- corpus metadata changes;
- private harvest;
- #388 or #381 activation.

## Owning Layer

Owning layer: Quality / Governance.

Quality / Governance owns:

- static-analysis measurement vocabulary;
- advisory-vs-blocking policy;
- zero-baseline candidate semantics;
- exact-code promotion criteria;
- protected-surface review requirements;
- role routing and stop conditions.

Ruff owns static-analysis findings only. Ruff findings are not parser truth,
security assurance, privacy assurance, release readiness, deploy readiness, or
production readiness.

Parser remains the truth owner for parser interpretation, parser events,
router behavior, parser state reconciliation, match/game identity,
deduplication, workbook payloads, analytics inputs, and coaching inputs.

## Internal Project Area

Primary: Quality / Governance.

Supporting areas:

- CI / Tooling, only as a future separately authorized implementation surface.
- Protected-surface governance, only as a future separately reviewed stricter
  promotion surface.

This contract is not a parser module, analytics module, AI module, corpus
automation module, deployment module, release module, or production behavior
change.

## Advisory Command Boundary

Future implementation may define read-only commands equivalent to:

```bash
python3 -m ruff check src tests tools --select ALL --exit-zero --statistics
python3 -m ruff check src tests tools --select ALL --exit-zero --output-format json
```

Windows-oriented local examples may use:

```powershell
py -m ruff check src tests tools --select ALL --exit-zero --statistics
py -m ruff check src tests tools --select ALL --exit-zero --output-format json
```

Required command properties:

- include `src`, `tests`, and `tools`;
- use `--select ALL` only in advisory measurement mode;
- use `--exit-zero` so findings do not fail the command;
- never use `--fix`;
- never use `--unsafe-fixes`;
- never edit files as part of measurement;
- record the Ruff version, command arguments, scan scope, repository, branch or
  ref, and commit;
- fail closed if Ruff is missing, the JSON output is malformed, the scan emits
  local absolute paths, or the command fails for a reason other than findings.

Advisory scan success means "the measurement command completed." It does not
mean "the repo is clean" or "rules are ready to block."

## Advisory Output Handling

Future implementation may write local review output under a public-safe,
ignored review directory such as:

```text
_review_/quality_ruff_advisory/<run-id>/
```

Committed artifacts are not authorized by this contract. A later Codex C/E/F
lane may authorize a sanitized summary artifact, but raw Ruff JSON must not be
committed by default.

Allowed public-safe summary fields:

- repository;
- repository URL;
- branch or ref;
- commit;
- Ruff version;
- command arguments;
- scan scope;
- run id;
- generated timestamp in UTC;
- total finding count;
- total triggered exact rule-code count;
- total zero-baseline exact rule-code count;
- rule-code summaries;
- protected-surface impact classification;
- autofix metadata as evidence only;
- suggested disposition;
- non-claims.

Forbidden public or committed output:

- local absolute paths;
- private paths;
- raw private logs;
- generated runtime artifacts;
- workbook exports;
- SQLite databases;
- app-data contents;
- network traces;
- screenshots;
- secrets;
- credentials;
- tokens;
- API keys;
- webhook URLs;
- source patches generated by a tool;
- autofix diffs;
- any output implying parser truth or readiness.

## Advisory Report Envelope

If a future helper emits a machine-readable advisory summary, the envelope
should use this vocabulary:

```json
{
  "object": "mythic_edge_quality_ruff_advisory_report",
  "schema_version": "quality_ruff_advisory_report.v1",
  "repository": "Tahjali11/Mythic-Edge",
  "repository_url": "https://github.com/Tahjali11/Mythic-Edge",
  "branch_or_ref": "main",
  "commit": "<git-sha>",
  "ruff_version": "<ruff-version>",
  "scan_scope": ["src", "tests", "tools"],
  "commands": [],
  "exit_behavior": "advisory_exit_zero",
  "totals": {
    "findings": 0,
    "triggered_rule_codes": 0,
    "zero_baseline_rule_codes": 0
  },
  "rule_summaries": [],
  "zero_baseline_candidates": [],
  "non_claims": []
}
```

The envelope must be deterministic for the same Ruff version, same commit,
same configuration, and same scan scope.

## Rule Summary Schema

Each rule summary should include:

```json
{
  "rule_code": "S101",
  "rule_family": "S",
  "count": 0,
  "affected_file_count": 0,
  "affected_paths": [],
  "autofix_available": "unknown",
  "unsafe_fix_available": "unknown",
  "protected_surface_impact": "none",
  "disposition": "zero_baseline_candidate",
  "reason": "Exact rule code has zero findings for this scan scope."
}
```

Required field rules:

- `rule_code` must be an exact Ruff rule code, not a broad family.
- `count` must be the measured finding count for that exact rule code.
- `affected_paths` must be repo-relative if included.
- `autofix_available` and `unsafe_fix_available` are evidence only.
- `protected_surface_impact` must be conservative when uncertain.
- `disposition` must use the approved vocabulary below.

## Disposition Vocabulary

Allowed dispositions:

- `zero_baseline_candidate`: exact rule code has zero findings in the accepted
  branch/Ruff-version/scope tuple and has no known project-convention conflict.
- `blocker_candidate`: exact rule code may be proposed for a later blocking
  promotion after human review.
- `advisory`: rule has findings or needs review, and must not block.
- `watch_list`: rule may matter later but is noisy, immature, convention
  dependent, or not enough context exists.
- `cleanup_issue_candidate`: rule has real findings that need scoped
  behavior-preserving cleanup before it can be considered for blocking.
- `protected_surface_review_required`: rule touches parser truth, private
  evidence, CI, release, deployment, workbook, webhook, Apps Script, analytics,
  AI, coaching, or artifact-governance surfaces and needs a dedicated contract.
- `ignore_with_rationale`: rule is intentionally not pursued, with a written
  repo-specific reason.
- `unsupported`: rule cannot be interpreted safely by the current helper.
- `invalid`: the record is malformed or inconsistent.

Forbidden dispositions:

- `blocking_enabled`;
- `ci_ready`;
- `parser_ready`;
- `security_assured`;
- `privacy_assured`;
- `production_ready`;
- `auto_fixed`;
- `truth_confirmed`.

## Zero-Baseline Candidate Rules

An exact rule code may be listed as a zero-baseline candidate only when all of
these are true:

1. The rule count is `0` for the accepted branch, commit, Ruff version, and
   scan scope.
2. The record uses the exact Ruff rule code.
3. The rule is not inferred from a partially clean broad family.
4. The rule does not conflict with documented repo conventions.
5. The rule does not require source mutation to become clean.
6. The rule does not rely on private evidence, generated artifacts, local-only
   paths, or external runtime state.
7. The rule has a documented future promotion path.

A zero-baseline candidate is not a blocking rule. It is only a candidate for a
future Codex A/B/C/E/F/G lane.

## Triggered Rule Handling

Triggered rules with nonzero findings must remain advisory unless a later
issue fixes the existing findings through reviewed, behavior-preserving work.

High-signal triggered rules may be recorded as `cleanup_issue_candidate` or
`protected_surface_review_required`, but they must not be promoted directly to
blocking.

Examples of high-signal triggered categories include:

- broad exception handling;
- subprocess/path execution hazards;
- hardcoded secret-like strings;
- timezone or datetime ambiguity;
- risky SQL/string construction;
- unsafe assertions in runtime code;
- private-path or artifact-leak risks.

The existence of a high-signal advisory finding does not prove a vulnerability,
parser bug, privacy leak, or production risk. It proves only that Ruff reported
a static-analysis finding requiring human interpretation.

## Protected-Surface Impact Vocabulary

Allowed protected-surface impact labels:

- `none`
- `parser_truth_surface`
- `evidence_or_corpus_surface`
- `private_artifact_or_secret_surface`
- `eventbus_or_transport_surface`
- `workbook_webhook_or_appsscript_surface`
- `analytics_ai_or_coaching_surface`
- `ci_release_or_deploy_surface`
- `governance_or_workflow_surface`
- `unknown_review_required`

If a rule touches more than one surface, choose the most restrictive label or
record an ordered list of labels.

Protected-surface impact does not automatically make a rule blocking. It makes
promotion more cautious and usually requires a dedicated issue/contract.

## Autofix Policy

Autofix availability is evidence, not approval.

Forbidden in this issue and any direct Codex B follow-up:

- `ruff check --fix`
- `ruff check --unsafe-fixes`
- generated autofix patches
- bulk formatting or cleanup PRs
- source rewrites to satisfy a broad rule family

A future autofix lane must define:

- exact rule code;
- exact paths;
- whether fixes are safe or unsafe;
- expected behavior preservation;
- protected-surface impact;
- review plan;
- rollback plan;
- focused validation;
- non-claims.

## Rule Promotion Model

Later blocking promotion must be exact-code first.

Allowed future promotion inputs:

- accepted branch and commit;
- Ruff version;
- exact zero-baseline rule-code evidence;
- protected-surface review result;
- project-convention compatibility review;
- focused validation result;
- human approval in the relevant Codex role lane.

Forbidden future promotion inputs:

- broad family cleanliness assumptions;
- stale tracker-only counts;
- one local machine's unreviewed output;
- private logs or generated runtime artifacts;
- autofix availability alone;
- style preference alone;
- source-repo mutation from outside the authorized worktree;
- "Ruff says so" without repo-specific review.

Blocking promotion requires a later issue. It must update the explicit rule
code list only after review. It must not broaden to `ALL` in CI.

## Priority Layers

Future review may sort advisory findings into these planning layers:

1. Correctness, security-adjacent, privacy, subprocess, environment, parser
   truth, and artifact-leak risks.
2. Runtime reliability and maintainability.
3. Protected-surface stricter rules.
4. Type-shape and test-quality rules.
5. Style, docs, and formatting rules.

Priority is a triage aid only. It does not authorize fixes, CI changes, or
blocking gates.

## Failure And Refusal Vocabulary

Allowed failure/refusal states:

- `measurement_blocked_tool_missing`
- `measurement_blocked_command_failed`
- `measurement_blocked_malformed_json`
- `measurement_blocked_local_path_leak`
- `measurement_blocked_secret_like_output`
- `candidate_rejected_nonzero_count`
- `candidate_rejected_broad_family`
- `candidate_rejected_project_convention_conflict`
- `candidate_rejected_protected_surface_needs_contract`
- `promotion_blocked_no_human_review`
- `promotion_blocked_ci_change_not_authorized`
- `autofix_blocked_not_authorized`

All failure states are fail-closed. They must not silently become advisory
success, blocking promotion, or readiness claims.

## Relationship To #569 Coverage Baseline Design

Issue #569 and issue #570 are sibling Phase 0 quality lanes.

This contract owns Ruff advisory and exact-rule zero-baseline policy.

The #569 lane owns coverage baseline measurement and ratchet design.

Neither lane may:

- activate CI enforcement;
- claim parser truth;
- claim fixture promotion readiness;
- claim corpus readiness;
- claim release readiness;
- close #388;
- interfere with active parser-evidence work.

## Relationship To #388

The #388 parser-evidence tracker remains open and inactive for the purposes of
this contract.

Ruff advisory findings may identify code-quality work, but they do not:

- authorize private harvest;
- validate parser evidence;
- promote fixtures;
- update corpus metadata;
- prove parser behavior readiness;
- prove pipeline activation readiness;
- prove private smoke success.

## Future Split Points

Recommended future split points:

1. Codex C/E/F/G docs/tooling lane for a local advisory report helper, if
   approved.
2. Codex A/B lane to create a zero-baseline candidate review issue from a
   sanitized report.
3. Codex B/C/E lane for exact-code blocking promotion of a small candidate set.
4. Codex B/C/E lane for high-signal triggered-rule cleanup, one protected
   surface or exact rule at a time.
5. Codex B/C/E lane for any autofix trial, if explicitly approved.
6. Codex B/C/E lane for CI integration, only after exact-code promotion is
   reviewed.

## Validation Expectations

Codex B validation for this contract should be docs-only:

```bash
printf '%s\n' docs/contracts/quality_ruff_advisory_zero_baseline_design.md \
  | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin
printf '%s\n' docs/contracts/quality_ruff_advisory_zero_baseline_design.md \
  | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin
git diff --check
git diff --check --no-index /dev/null docs/contracts/quality_ruff_advisory_zero_baseline_design.md
```

Codex B must not run the all-rules Ruff advisory scan as validation. That scan
is a future measurement implementation surface.

Later implementation validation should include:

- helper unit tests, if a helper is implemented;
- deterministic fixture tests for advisory report parsing and classification;
- malformed Ruff JSON fail-closed tests;
- local path and secret-like output rejection tests;
- exact-code candidate selection tests;
- broad-family rejection tests;
- protected-surface classification tests;
- standard `python3 -m ruff check src tests tools`;
- `python3 tools/check_secret_patterns.py` on any public artifacts;
- `python3 tools/check_protected_surfaces.py` on changed paths;
- `git diff --check`.

## Non-Claims

This contract does not claim:

- parser behavior readiness;
- pipeline activation readiness for #388;
- parser truth;
- fixture promotion readiness;
- corpus readiness;
- private smoke success;
- CI readiness;
- release readiness;
- deploy readiness;
- production readiness;
- security assurance;
- privacy assurance;
- analytics truth;
- AI truth;
- coaching truth.

## Codex C Authorization Decision

Codex C implementation is not authorized by default from this contract alone.

Recommended next role: Codex E review for this contract. If Codex E finds no
contract blockers, route to Codex F/G for normal submission/merge. After merge,
a new Codex A issue may decide whether to authorize a tiny local advisory
report helper.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge workflow rules.

Act as Codex E: Module Reviewer for issue #570.

Repository:
Tahjali11/Mythic-Edge

Repository URL:
https://github.com/Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/570

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/567

Project roadmap:
https://github.com/Tahjali11/Mythic-Edge/issues/568

Active parser evidence tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/388

Source artifact:
docs/contracts/quality_ruff_advisory_zero_baseline_design.md

Goal:
Review the Phase 0 Ruff advisory and zero-baseline design contract for
overclaims, missing stop conditions, unsafe CI/autofix promotion language,
protected-surface gaps, and mismatch with the quality roadmap.

Protected boundaries:
- Do not implement code.
- Do not open a PR.
- Do not change CI.
- Do not run all-rules Ruff scans as evidence for readiness.
- Do not enable blocking Ruff rules.
- Do not run Ruff autofix or unsafe fixes.
- Do not change parser behavior.
- Do not claim parser truth, fixture promotion, corpus readiness, release
  readiness, security assurance, privacy assurance, analytics truth, AI truth,
  coaching truth, or production readiness.

Expected output:
- Findings first, if any.
- Contract approval or required fixes.
- Validation assessment.
- Recommended next role.
- workflow_handoff block.
```

## Workflow Handoff

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/570"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/567"
  project_roadmap: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  active_parser_evidence_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/388"
  sibling_phase_0_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/569"
  completed_thread: "B"
  next_thread: "E"
  verdict: "phase_0_ruff_advisory_zero_baseline_contract_ready_for_review"
  risk_tier: "High"
  base_branch: "main"
  target_branch: "main"
  branch: "codex/quality-ruff-advisory-zero-baseline-design-570"
  target_artifact: "docs/contracts/quality_ruff_advisory_zero_baseline_design.md"
  implementation_authorized: false
  ci_change_authorized: false
  ruff_blocking_promotion_authorized: false
  ruff_autofix_authorized: false
  parser_behavior_change_authorized: false
  parser_behavior_ready: false
  pipeline_activation_ready_for_issue_388: false
  validation:
    - "path-scoped secret-pattern check for docs/contracts/quality_ruff_advisory_zero_baseline_design.md"
    - "path-scoped protected-surface check for docs/contracts/quality_ruff_advisory_zero_baseline_design.md"
    - "git diff --check"
    - "git diff --check --no-index /dev/null docs/contracts/quality_ruff_advisory_zero_baseline_design.md"
  stop_conditions:
    - "Do not implement code."
    - "Do not open a PR without explicit routing."
    - "Do not change CI."
    - "Do not enable blocking Ruff rules."
    - "Do not run Ruff autofix or unsafe fixes."
    - "Do not run private evidence checks."
    - "Do not change parser behavior."
    - "Do not claim parser truth, fixture promotion, corpus readiness, release readiness, security assurance, privacy assurance, analytics truth, AI truth, coaching truth, or production readiness."
```
