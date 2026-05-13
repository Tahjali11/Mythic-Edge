# Agent Constitution V2 Synthesis Implementation Handoff

## Issue

https://github.com/Tahjali11/Mythic-Edge/issues/18

## Tracker

https://github.com/Tahjali11/Mythic-Edge/issues/1

## Contract

`docs/contracts/agent_constitution_v2_synthesis.md`

## Role Performed

Codex C: Module Implementer.

## What Changed

Implemented the V2 documentation package required by the synthesis contract.
The package keeps `docs/agent_constitution.md` human-readable, adds
`docs/agent_rules.yml` as the terse machine-readable rule index, defines Codex
roles A through G, and separates Module Submitter work from Integration
Deployer merge/close/tracker duties.

Created GitHub issue #18 for V2 adoption and linked it to tracker issue #1.

## Files Changed

- `AGENTS.md`
- `.github/ISSUE_TEMPLATE/module_workflow.yml`
- `.github/pull_request_template.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/problem_representation.md`
- `docs/agent_threads/module_contract.md`
- `docs/agent_threads/implementation.md`
- `docs/agent_threads/module_fixer.md`
- `docs/agent_threads/review.md`
- `docs/agent_threads/contract_test.md`
- `docs/agent_threads/module_submitter.md`
- `docs/agent_threads/integration_deployer.md`
- `docs/templates/problem_representation.md`
- `docs/templates/module_contract.md`
- `docs/templates/implementation_handoff.md`
- `docs/templates/contract_test_report.md`
- `docs/templates/workflow_handoff.md`
- `docs/templates/current_status.md`
- `docs/archive/agent_constitution_v2_drafts/`
- `docs/implementation_handoffs/agent_constitution_v2_synthesis.md`

## Code Changed

No runtime code changed.

No parser, workbook, webhook, Apps Script, match/game identity, final
reconciliation, secrets, raw logs, generated data, runtime status files, failed
posts, or workbook export surfaces changed.

## Tests Added Or Updated

No code tests were added or updated because this is a documentation-only
constitution/workflow package.

## Interface Changes

Documentation and workflow interfaces changed:

- `docs/agent_rules.yml` now defines the machine-readable V2 rule index.
- Codex G: Integration Deployer is now the merge, issue-close, and
  tracker-update role.
- Codex F: Module Submitter is limited to staging, committing, pushing, and
  opening or updating draft PRs.
- `workflow_handoff` now includes `tracker`.
- Templates now include tracker, source artifact, target artifact, branch,
  protected-surface, PR lifecycle, issue lifecycle, and status-summary fields
  where relevant.
- Per-role YAML schema is defined in `docs/agent_rules.yml`, but per-role YAML
  files are not required in the first adoption package.

## Draft Archive

Archived the contract-required role-labeled V2 drafts under:

`docs/archive/agent_constitution_v2_drafts/`

Archived files:

- `agent_constitution_v2_codex_a_thinker_draft.md`
- `agent_constitution_v2_codex_f.md`
- `v2_constitution_codex_a.md`
- `v2_constitution_codex_b.md`
- `v2_constitution_codex_c.md`
- `v2_constitution_codex_d.md`
- `v2_constitution_codex_e.md`

## Validation Run

```bash
gh issue view 18 --json number,title,body,labels,state,url
# Pass: issue #18 is open and its body says it is linked to #1.

git diff --check
# Pass: no output.

ruby -e 'require "yaml"; YAML.load_file("docs/agent_rules.yml"); YAML.load_file(".github/ISSUE_TEMPLATE/module_workflow.yml"); puts "yaml ok"'
# Pass: yaml ok.

ruby -e 'require "yaml"; data=YAML.load_file("docs/agent_rules.yml"); required=%w[version status authority_order source_priority sacred_rules protected_surfaces roles routing risk_tiers issue_lifecycle pr_lifecycle tracker_hygiene branch_policy validation_gates prompt_schema handoff_schema current_status_schema archive_policy]; missing=required.reject{|k| data.key?(k)}; roles=%w[A B C D E F G].reject{|k| data.fetch("roles",{}).key?(k)}; abort("missing keys: #{missing.join(",")}") unless missing.empty?; abort("missing roles: #{roles.join(",")}") unless roles.empty?; puts "agent rules shape ok"'
# Pass: agent rules shape ok.

ruby -e 'bad=[]; ARGV.each{|p| File.readlines(p, chomp: true).each_with_index{|line,i| bad << "#{p}:#{i+1}" if line =~ /[ \t]+$/ }}; if bad.empty? then puts "whitespace ok" else warn bad.join("\n"); exit 1 end' AGENTS.md .github/ISSUE_TEMPLATE/module_workflow.yml .github/pull_request_template.md docs/agent_constitution.md docs/agent_rules.yml docs/codex_module_workflow.md docs/agent_threads/problem_representation.md docs/agent_threads/module_contract.md docs/agent_threads/implementation.md docs/agent_threads/module_fixer.md docs/agent_threads/review.md docs/agent_threads/contract_test.md docs/agent_threads/module_submitter.md docs/agent_threads/integration_deployer.md docs/templates/problem_representation.md docs/templates/module_contract.md docs/templates/implementation_handoff.md docs/templates/contract_test_report.md docs/templates/workflow_handoff.md docs/templates/current_status.md docs/implementation_handoffs/agent_constitution_v2_synthesis.md
# Pass: whitespace ok.

python3 -m pytest -q
# Pass: 396 passed in 0.91s.

python3 -m ruff check src tests
# Pass: All checks passed!

git diff --name-only -- src tools main.py live_print_filtered_v11_match_summary.py
# Pass: no output.
```

## Still Unverified

- GitHub Actions were not checked because no PR exists yet.
- The tracker issue #1 was not edited in this implementer thread.
- The Module Fixer follow-up has not yet received fresh-context contract-test
  review.

## Module Fixer Follow-Up

Codex D addressed the contract-test blocker reported in
`docs/contract_test_reports/agent_constitution_v2_synthesis.md`.

Finding classification: implementation bug under existing contract.

The contract at `docs/contracts/agent_constitution_v2_synthesis.md` requires
explicit conflict-triage rules. The fix preserved the contract's ordered
triage semantics and did not require a contract change.

Files changed by the fixer follow-up:

- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/implementation_handoffs/agent_constitution_v2_synthesis.md`
- `docs/contract_test_reports/agent_constitution_v2_synthesis.md`

Fix summary:

- Added a top-level `conflict_triage` section to `docs/agent_rules.yml`.
- Added a human-readable `Conflict Triage` section to
  `docs/agent_constitution.md`.
- Preserved the contract's order for contradictory Codex suggestions.
- Did not change parser/runtime/workbook/App Script behavior.

Post-fix validation:

```bash
git diff --check
# Pass: no output.

ruby -e 'require "yaml"; YAML.load_file("docs/agent_rules.yml"); YAML.load_file(".github/ISSUE_TEMPLATE/module_workflow.yml"); puts "yaml ok"'
# Pass: yaml ok.

ruby -e 'require "yaml"; data=YAML.load_file("docs/agent_rules.yml"); required=%w[version status authority_order source_priority conflict_triage sacred_rules protected_surfaces roles routing risk_tiers issue_lifecycle pr_lifecycle tracker_hygiene branch_policy validation_gates prompt_schema handoff_schema current_status_schema archive_policy]; missing=required.reject{|k| data.key?(k)}; roles=%w[A B C D E F G].reject{|k| data.fetch("roles",{}).key?(k)}; abort("missing keys: #{missing.join(",")}") unless missing.empty?; abort("missing roles: #{roles.join(",")}") unless roles.empty?; puts "agent rules shape ok"'
# Pass: agent rules shape ok.

git diff --name-only -- src tools main.py live_print_filtered_v11_match_summary.py
# Pass: no output.

python3 -m pytest -q
# Pass: 396 passed in 0.90s.

python3 -m ruff check src tests
# Pass: All checks passed!
```

## Reviewer Focus

Ask Codex E to verify:

- `docs/agent_rules.yml` includes all contract-required top-level rule areas.
- `docs/agent_constitution.md` preserves V1 sacred rules without weaker
  wording.
- Codex G owns merge, issue closure, and tracker updates.
- Codex F cannot merge, close issues, or mark trackers completed.
- Issue lifecycle, PR lifecycle, tracker hygiene, current-status schema,
  prompt schema, handoff schema, branch policy, and archive policy are present
  and consistent across YAML and Markdown.
- Role-labeled V2 draft files are archived and no longer beside active rule
  files.
- No parser/runtime/workbook/App Script files changed.

## Next Workflow Action

Next role: Codex E, Module Reviewer in contract-test mode.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution. Act as Codex E: Module Reviewer in contract-test mode for the Constitution V2 synthesis package.

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/18

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/1

Use:
- docs/problem_representations/agent_constitution_v2_synthesis.md
- docs/contracts/agent_constitution_v2_synthesis.md
- docs/implementation_handoffs/agent_constitution_v2_synthesis.md
- AGENTS.md
- docs/agent_rules.yml
- docs/agent_constitution.md
- docs/codex_module_workflow.md
- docs/agent_threads/problem_representation.md
- docs/agent_threads/module_contract.md
- docs/agent_threads/implementation.md
- docs/agent_threads/module_fixer.md
- docs/agent_threads/review.md
- docs/agent_threads/contract_test.md
- docs/agent_threads/module_submitter.md
- docs/agent_threads/integration_deployer.md
- docs/templates/problem_representation.md
- docs/templates/module_contract.md
- docs/templates/implementation_handoff.md
- docs/templates/contract_test_report.md
- docs/templates/workflow_handoff.md
- docs/templates/current_status.md
- .github/pull_request_template.md
- .github/ISSUE_TEMPLATE/module_workflow.yml
- docs/archive/agent_constitution_v2_drafts/

Goal:
Verify the Module Implementer documentation package against docs/contracts/agent_constitution_v2_synthesis.md.

Confirm:
- docs/agent_rules.yml exists and parses as YAML.
- docs/agent_rules.yml includes the required rule areas: version, status, authority_order, source_priority, sacred_rules, protected_surfaces, roles A-G, routing, risk_tiers, issue_lifecycle, pr_lifecycle, tracker_hygiene, branch_policy, validation_gates, prompt_schema, handoff_schema, current_status_schema, and archive_policy.
- docs/agent_constitution.md remains human-readable and does not weaken V1 sacred safety rules.
- Per-role YAML schema is defined, but per-role YAML files are not required in the first adoption package.
- Codex G: Integration Deployer owns merge, issue closure, and tracker updates.
- Codex F: Module Submitter cannot merge, close issues, or mark trackers completed.
- Issue lifecycle, PR lifecycle, tracker hygiene, current-status summary, source priority, and conflict triage are explicit.
- Role-labeled V2 draft files are archived under docs/archive/agent_constitution_v2_drafts/ and not left beside active rule files.
- Issue #18 exists and is linked to #1, or document any blocker found.
- No parser/runtime/workbook/App Script behavior files changed.
- No workbook schema, webhook payload shape, Apps Script behavior, match/game identity, final reconciliation, secrets, raw logs, generated data, runtime status files, failed posts, or workbook exports changed.

Validation:
Run:
git diff --check
ruby -e 'require "yaml"; YAML.load_file("docs/agent_rules.yml"); YAML.load_file(".github/ISSUE_TEMPLATE/module_workflow.yml"); puts "yaml ok"'
python3 -m pytest -q
python3 -m ruff check src tests

Output:
- Findings first, if any.
- Contract-test verdict.
- Validation results.
- Remaining non-blocking gaps.
- Next recommended role: Codex F: Module Submitter if no blocking findings, otherwise Codex D: Module Fixer or Codex B: Module Contract Writer.
- A workflow_handoff block.

Do not change parser behavior, workbook schema, webhook payload shape, Apps Script behavior, parser state, match/game identity, final reconciliation, secrets, raw logs, generated data, runtime status files, failed posts, or workbook exports.
Do not merge, close issue #18, mark tracker #1 completed, or target main.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/18"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/1"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/agent_constitution_v2_synthesis.md"
  target_artifact: "docs/implementation_handoffs/agent_constitution_v2_synthesis.md"
  risk_tier: "High"
  branch: "codex/parser-module-audit-suite"
  validation:
    - "git diff --check"
    - "ruby -e 'require \"yaml\"; YAML.load_file(\"docs/agent_rules.yml\"); YAML.load_file(\".github/ISSUE_TEMPLATE/module_workflow.yml\"); puts \"yaml ok\"'"
    - "python3 -m pytest -q"
    - "python3 -m ruff check src tests"
    - "git diff --name-only -- src tools main.py live_print_filtered_v11_match_summary.py"
  stop_conditions:
    - "Route to Module Contract Writer if the V2 synthesis contract is ambiguous or contradicts itself."
    - "Route to Module Fixer if docs/agent_rules.yml and docs/agent_constitution.md disagree."
    - "Do not change parser behavior, workbook schema, webhook payload shape, Apps Script behavior, match/game identity, final reconciliation, secrets, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not target main unless explicitly approved."
```
