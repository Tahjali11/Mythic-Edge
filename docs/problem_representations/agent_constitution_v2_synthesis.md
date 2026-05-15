# Problem Representation: Agent Constitution v2 Synthesis

Related issue: https://github.com/Tahjali11/Mythic-Edge/issues/1

## Summary

Synthesize the role-labeled Codex constitution v2 drafts into a new, more robust Mythic Edge agent constitution. The new constitution should preserve all V1 sacred safety rules while becoming easier for Codex to consume through terse, machine-readable, modular rule files.

## What The Code Is Supposed To Do

The repository should give any new Codex thread a compact, reliable operating system for Mythic Edge work.

In plain English, Codex should be able to quickly determine:

- which role it is playing
- which project layer owns truth
- which source artifact has priority
- which files it may read or change
- whether the work requires a problem representation, contract, implementation, review, submitter, or integrator step
- when an issue can close
- when a tracker should stay open
- when a pull request can be marked ready or merged
- what validation evidence is required
- what handoff artifact the next thread needs

The final adopted constitution should be the new authoritative constitution, but the synthesis should also evaluate whether a modular documentation package would serve Codex better than a single long Markdown file.

## What It Is Actually Doing

V1 already provides strong safety rules, truth ownership, risk tiers, role definitions, validation expectations, and handoff rules.

The current gap is operational and structural:

- multiple Codex role threads produced separate v2 Markdown drafts
- the v2 suggestions are not yet synthesized
- some suggestions overlap or conflict
- the live constitution is still prose-heavy
- issue lifecycle, tracker hygiene, PR readiness, merge/closure behavior, and current-status summaries are not fully formalized
- Codex may waste tokens reading long human-readable docs when it only needs a relevant role/rule section

Current v2 source files to use are the most recently generated v2 constitution Markdown files whose filenames include a Codex role marker:

- `docs/agent_constitution_v2_codex_a_thinker_draft.md`
- `docs/agent_constitution_v2_codex_f.md`
- `docs/v2_constitution_codex_a.md`
- `docs/v2_constitution_codex_b.md`
- `docs/v2_constitution_codex_c.md`
- `docs/v2_constitution_codex_d.md`
- `docs/v2_constitution_codex_e.md`

Generic v2 constitution drafts without a Codex role marker in the filename should not be used as source artifacts.

## Why This Matters

Mythic Edge now uses a real multi-thread, issue-to-contract-to-PR workflow. The constitution is no longer just guidance; it is the coordination layer that keeps separate Codex threads from drifting across branches, issues, parser modules, workbook assumptions, and GitHub state.

If V2 is too long, Codex may miss important rules due to token truncation or over-broad reading. If V2 is too fragmented, role threads may miss the authority order or duplicate conflicting rules. The synthesis needs to balance human readability with machine accessibility.

## Project Layer

Primary layer: repository coordination and agent workflow.

This is not parser behavior, webhook transport, workbook schema, Apps Script behavior, or dashboard logic. It governs how changes to those layers are proposed, contracted, implemented, reviewed, submitted, merged, and closed.

## First Bad Value

No single bad runtime value exists.

First coordination ambiguity:

```text
docs/agent_constitution.md is authoritative but not yet optimized for modular, machine-readable Codex consumption.
```

Inspection order:

1. `docs/agent_constitution.md`
2. `AGENTS.md`
3. `docs/codex_module_workflow.md`
4. `docs/agent_threads/*.md`
5. `docs/templates/*.md`
6. role-labeled v2 draft files listed above
7. `.github/pull_request_template.md`
8. `.github/ISSUE_TEMPLATE/module_workflow.yml`
9. recent issue and PR workflow examples, especially tracker #5 and constitution issue #1

## Inputs

Primary source artifacts:

- `docs/agent_constitution.md`
- `AGENTS.md`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/problem_representation.md`
- `docs/agent_threads/module_contract.md`
- `docs/agent_threads/implementation.md`
- `docs/agent_threads/module_fixer.md`
- `docs/agent_threads/review.md`
- `docs/agent_threads/contract_test.md`
- `docs/agent_threads/module_submitter.md`
- `docs/templates/problem_representation.md`
- `docs/templates/module_contract.md`
- `docs/templates/implementation_handoff.md`
- `docs/templates/contract_test_report.md`
- `docs/templates/workflow_handoff.md`
- `.github/pull_request_template.md`
- `.github/ISSUE_TEMPLATE/module_workflow.yml`

V2 suggestion artifacts:

- `docs/agent_constitution_v2_codex_a_thinker_draft.md`
- `docs/agent_constitution_v2_codex_f.md`
- `docs/v2_constitution_codex_a.md`
- `docs/v2_constitution_codex_b.md`
- `docs/v2_constitution_codex_c.md`
- `docs/v2_constitution_codex_d.md`
- `docs/v2_constitution_codex_e.md`

GitHub workflow examples:

- issue #1: original constitution issue
- issue #5: parser module audit tracker
- issue #11 / PR #12: Player.log evidence ledger planning/docs issue
- recently closed module audit issues and merged PRs

## Expected Output

The final synthesis should recommend and then produce a constitution package that is easy for Codex to read selectively.

Recommended target structure:

- `AGENTS.md`
  - short entrypoint and non-negotiable summary
- `docs/agent_constitution.md`
  - new authoritative global constitution
- `docs/agent_rules.yml`
  - machine-readable rule index for authority order, sacred rules, role routing, issue lifecycle, PR lifecycle, source priority, and validation gates
- `docs/agent_threads/*.md`
  - short human-readable role docs
- `docs/agent_threads/*.yml`
  - optional machine-readable role specs, if the contract writer agrees the added structure is worth maintaining
- `docs/templates/*.md`
  - human-usable artifact templates
- optional explanatory companion docs
  - longer prose explanations for the user, kept separate from Codex’s terse operating rules

The synthesis should explicitly compare:

- single long constitution file
- modular Markdown-only constitution
- Markdown plus machine-readable YAML rule index
- Markdown plus per-role YAML specs

## Scope

In scope:

- synthesizing the role-labeled v2 constitution drafts
- preserving all sacred V1 rules
- designing a machine-readable documentation structure
- defining issue lifecycle rules
- defining tracker hygiene rules
- defining pull request readiness and merge/closure rules
- defining source artifact priority
- defining conflict-resolution rules for contradictory Codex suggestions
- defining current-status summary blocks
- recommending whether to split Module Submitter into Submitter and Integration Deployer roles
- recommending where terse Codex rules should live versus longer user-facing explanations
- creating a handoff to a Module Contract Writer for the v2 constitution contract

Out of scope:

- changing parser behavior
- changing workbook schema
- changing webhook payload shape
- changing deployed Apps Script behavior
- changing match identity, game identity, deduplication, or final reconciliation
- adopting V2 directly without contract/review
- deleting V1 before a replacement is reviewed and accepted
- merging any constitution changes directly into `main` without explicit approval

## Risks And Likely Breakpoints

- V2 may become too long and trigger token truncation.
- V2 may become too modular and scatter authority across too many files.
- YAML and Markdown may drift if the same rule is duplicated.
- Role-specific files may conflict with the global constitution.
- Codex may follow a lower-priority draft file instead of the adopted constitution.
- Issue closing and PR merge rules may accidentally encourage premature closure of planning or tracker issues.
- A new Integration Deployer role may overlap with Module Submitter unless boundaries are explicit.
- Machine-readable rules may become terse enough that the user loses helpful explanations.
- Conflicting Codex suggestions may accidentally weaken V1 sacred rules.

## Validation Evidence Needed

Docs and workflow validation:

```bash
python3 -m pytest -q
python3 -m ruff check src tests
```

Review validation:

- A fresh Codex thread can identify the active role without reading every file.
- A fresh Codex thread can find the authority order and sacred rules quickly.
- A fresh Codex thread can decide whether an issue should close.
- A fresh Codex thread can decide whether a tracker should remain open.
- A fresh Codex thread can determine the correct PR target branch.
- A fresh Codex thread can identify which artifact outranks chat memory.
- The new rule package preserves every V1 non-negotiable.
- The machine-readable rule index does not contradict the human-readable constitution.

## Open Questions

- Should `docs/agent_rules.yml` be required in V2, or should YAML specs be introduced in a follow-up after the Markdown synthesis lands?
- Should per-role YAML files be created now, or should V2 first define the schema and leave implementation for another issue?
- Should `F2 Integration Deployer` be part of the adopted V2, or should it receive its own thread and contract?
- Should `docs/agent_constitution.md` remain moderately human-readable, with `docs/agent_rules.yml` as the terse Codex-optimized source?
- Should old role-labeled draft files remain as historical source artifacts after V2 is adopted, or move under an archive folder?
- Should issue #1 remain open until V2 lands, or should V2 synthesis get a separate GitHub issue linked to #1?

## Recommended Answers To Open Questions

### Require `docs/agent_rules.yml` In V2

Recommendation: yes.

V2 should introduce `docs/agent_rules.yml` as a required machine-readable rule index. This file should not duplicate the full constitution. It should encode the highest-value operational rules Codex needs to route work cheaply:

- authority order
- sacred safety rules
- role ids and routing
- issue lifecycle rules
- PR lifecycle rules
- tracker hygiene rules
- source artifact priority
- validation gates
- stop conditions

This directly serves the token-efficiency goal. Codex can read a terse YAML index first, then open only the relevant Markdown sections when needed.

### Define Per-Role YAML Schema Now, Implement Role YAML Later

Recommendation: define the schema in V2, but do not require every per-role YAML file in the first V2 adoption PR.

Initial V2 should avoid creating too many new files at once. The first synthesis should add `docs/agent_rules.yml` and update the existing Markdown role docs. It can also define the future role-spec schema, but per-role YAML files such as `docs/agent_threads/review.yml` or `docs/agent_threads/module_submitter.yml` should be a follow-up unless the contract writer finds they are needed immediately.

Reason: this reduces drift risk. A single YAML rule index is easier to keep consistent than a full YAML mirror of every role document.

### Add `F2 Integration Deployer` As A Formal Follow-Up

Recommendation: V2 should name the split between Submitter and Integration Deployer, but the full F2 role file/spec should get its own issue or thread.

V2 should clarify the boundary:

- `F1 Module Submitter`: stages, commits, pushes, and opens or updates a draft PR.
- `F2 Integration Deployer`: marks an approved PR ready, verifies CI/scope, merges into the approved non-production base, closes completed issues, and updates trackers.

The concept should be included in the V2 contract because it affects PR lifecycle rules. The full role document can be a follow-up so it does not block the constitution synthesis.

### Keep `docs/agent_constitution.md` Human-Readable And Add YAML For Codex

Recommendation: yes.

`docs/agent_constitution.md` should remain the authoritative human-readable constitution. `docs/agent_rules.yml` should become the terse Codex-optimized operational index.

Conflict policy:

```yaml
constitution_conflict_policy:
  if_agent_rules_conflicts_with_agent_constitution:
    action: "follow the stricter or safer rule, then route to Constitution Contract Writer"
  if_agent_rules_omits_context:
    action: "open docs/agent_constitution.md or the relevant role doc"
  if_rule_is_operational_and_not_explained:
    action: "treat docs/agent_rules.yml as the quick index, not the full rationale"
```

This gives Codex a fast path without making the user-facing explanation disappear.

### Archive Role-Labeled Drafts After Adoption

Recommendation: move old role-labeled drafts to an archive folder after V2 is adopted.

Suggested archive path:

```text
docs/archive/agent_constitution_v2_sources/
```

The drafts should remain available as source/provenance artifacts, but they should not remain beside the adopted constitution where a future Codex thread might confuse them for active instructions.

The archive should include a short README explaining that those files are historical source suggestions, not active rules.

### Create A Separate V2 Synthesis Issue Linked To #1

Recommendation: create a new GitHub issue for V2 synthesis, linked to issue #1.

Issue #1 is the V1 constitution design issue. V2 synthesis is a new coherent workflow problem with new acceptance criteria:

- preserve V1 sacred rules
- synthesize role-labeled drafts
- design machine-readable rule index
- define issue/PR/tracker lifecycle rules
- decide documentation architecture
- prepare adoption path

After the V2 issue exists, issue #1 can either:

- close as the completed V1 constitution issue, with a comment linking to the V2 synthesis issue; or
- remain open only as a parent/history tracker if the user wants one long-running constitution issue.

Preferred path: open a dedicated V2 synthesis issue and then close #1 as completed V1 once the user is comfortable with the handoff.

## Recommended Direction

Use a modular constitution package:

```yaml
recommended_structure:
  AGENTS.md:
    purpose: "short entrypoint and highest-signal reminders"
  docs/agent_constitution.md:
    purpose: "authoritative global human-readable constitution"
  docs/agent_rules.yml:
    purpose: "machine-readable source for Codex routing, gates, lifecycle rules, and sacred constraints"
  docs/agent_threads/*.md:
    purpose: "short human-readable role docs"
  docs/agent_threads/*.yml:
    purpose: "optional machine-readable role specs"
  docs/templates/*.md:
    purpose: "artifact templates"
```

Conflict resolution recommendation:

```yaml
suggestion_triage:
  - preserve active system and developer instructions
  - preserve explicit user instructions
  - preserve all V1 sacred safety rules
  - prefer parser truth ownership
  - prefer current repo workflow proven by successful issues and PRs
  - prefer machine-readable, short, testable rules
  - prefer modular rules over duplicated prose
  - preserve high-risk disagreements as open questions
```

## Next Workflow Action

Next role: Codex B: Module Contract Writer.

Pasteable prompt:

```text
Use the Mythic Edge agent constitution.

Act as Codex B: Module Contract Writer for the Constitution v2 synthesis problem representation:
docs/problem_representations/agent_constitution_v2_synthesis.md

Read:
- docs/agent_constitution.md
- AGENTS.md
- docs/codex_module_workflow.md
- docs/agent_threads/*.md
- docs/templates/*.md
- .github/pull_request_template.md
- .github/ISSUE_TEMPLATE/module_workflow.yml
- docs/agent_constitution_v2_codex_a_thinker_draft.md
- docs/agent_constitution_v2_codex_f.md
- docs/v2_constitution_codex_a.md
- docs/v2_constitution_codex_b.md
- docs/v2_constitution_codex_c.md
- docs/v2_constitution_codex_d.md
- docs/v2_constitution_codex_e.md

Create a module/workflow contract for Constitution v2 synthesis at:
docs/contracts/agent_constitution_v2_synthesis.md

The contract should define the target documentation architecture, source artifact priority, sacred V1 rules that must be preserved, machine-readable rule structure, issue lifecycle rules, PR lifecycle rules, tracker hygiene rules, current-status summary expectations, conflict triage rules, acceptance criteria, and validation obligations.

Do not adopt V2 yet.
Do not replace docs/agent_constitution.md yet.
Do not change parser behavior, workbook schema, webhook payload shape, Apps Script behavior, match/game identity, final reconciliation, secrets, raw logs, generated data, runtime status files, failed posts, or workbook exports.
Do not target main unless the user explicitly approves it.
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/1"
  completed_thread: "A"
  next_thread: "B"
  source_artifact: "docs/problem_representations/agent_constitution_v2_synthesis.md"
  target_artifact: "docs/contracts/agent_constitution_v2_synthesis.md"
  risk_tier: "Medium"
  branch: "codex/parser-module-audit-suite"
  validation:
    - "not run - problem representation and draft cleanup only"
  stop_conditions:
    - "Do not adopt V2 before a contract and review exist."
    - "Do not weaken V1 sacred safety rules."
    - "Do not use generic v2 constitution drafts without Codex role markers in their filenames as source artifacts."
```
