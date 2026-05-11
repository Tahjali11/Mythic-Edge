# Problem Representation: Agent Constitution And Thread Rules

GitHub issue: https://github.com/Tahjali11/Mythic-Edge/issues/1

## Decision Log

- `AGENTS.md` should be concise, senior-engineer oriented, and act as the root entrypoint.
- The full constitution should live in `docs/agent_constitution.md`.
- GitHub issues should link to thread-rule docs rather than copying their full text.
- Material constitution changes should be tracked through GitHub issues. Issue #1 is the active v1 design issue.
- Each thread-role file should include a canonical starter prompt.
- AI/API analytics boundaries should be included now at a high level, with implementation details deferred to a future analytics contract.
- Risk tiers should guide workflow ceremony.
- Low-risk changes may skip the full four-thread workflow when obvious, local, and reversible.
- Ambiguity should be escalated based on risk.
- Every thread should end with a handoff packet.
- Constitution changes should follow an amendment process.

## Summary

Mythic Edge needs a durable agent constitution: a small set of repo-owned Markdown rules that every Codex thread can use consistently, regardless of which machine starts the work. The current guidance is strong but spread across `AGENTS.md`, workflow docs, templates, and this conversation, which makes it easy for future threads to miss the same assumptions.

## What The Code Is Supposed To Do

The repository should give every agent the same operating frame before it edits code, writes contracts, reviews pull requests, or tests workbook-facing behavior.

In plain English, a new Codex thread should be able to open the repo and quickly know:

- what Mythic Edge is
- which layer owns truth
- how to decide whether it is doing problem representation, contract work, implementation, or contract testing
- what it is allowed to change
- what it must verify
- how to communicate plainly without over-explaining
- what must never be committed, posted, deleted, or guessed

## What It Is Actually Doing

The project currently has useful instructions, but they are not separated by purpose.

Current state:

- `AGENTS.md` contains broad project rules and detailed layer guidance.
- `docs/codex_module_workflow.md` describes the four-thread workflow.
- `docs/templates/` contains handoff templates.
- `.github/ISSUE_TEMPLATE/module_workflow.yml` captures issue-shaping fields.
- Some durable decisions still live only in this conversation, not as repo-owned rules.

This means a new agent may read too much, read too little, or apply the wrong section to its role.

## Why This Matters

This project is becoming multi-threaded and multi-machine. Without a clear constitution, future agents can drift in small but expensive ways:

- implementation threads may skip the contract
- testing threads may quietly change code instead of reporting mismatches
- workbook display fixes may move truth away from the parser
- local logs or webhook URLs may accidentally be committed
- a laptop checkout may lack the same behavioral assumptions as this desktop checkout
- agents may over-focus on code and under-explain the data pipeline or layer ownership

The goal is not more paperwork. The goal is fewer confused handoffs.

## Project Layer

Primary layer: repository coordination and agent workflow.

This is not part of the MTGA parser truth layer, webhook transport layer, workbook layer, or dashboard layer. It is a cross-cutting development process layer that governs how changes to those layers are proposed, contracted, implemented, and verified.

## First Bad Value

The first bad value is the absence of a single declared source of truth for agent behavior.

Places where drift can currently appear:

1. A new Codex thread reads `AGENTS.md` but misses `docs/codex_module_workflow.md`.
2. A thread sees the workflow but does not know which role it owns.
3. A thread starts implementation before the problem representation and contract are stable.
4. A thread relies on this local conversation instead of repo-owned docs.
5. A thread on another machine lacks local generated data and behaves differently.

## Inputs

Inputs for the eventual constitution design:

- `AGENTS.md`
- `CONTRIBUTING.md`
- `docs/codex_module_workflow.md`
- `docs/templates/problem_representation.md`
- `docs/templates/module_contract.md`
- `docs/templates/implementation_handoff.md`
- `docs/templates/contract_test_report.md`
- `.github/ISSUE_TEMPLATE/module_workflow.yml`
- `.github/pull_request_template.md`
- the current project layer rules from the repo instructions
- the Manasight-style issue-to-PR workflow pattern

## Expected Output

The final design should produce a small set of Markdown files with clear ownership.

Recommended target shape:

- `AGENTS.md`
  - The root constitution entrypoint that Codex is most likely to read automatically.
  - Should be concise enough to follow, but strong enough to prevent unsafe behavior.
  - Should point to role-specific rule files.

- `docs/agent_constitution.md`
  - The full durable constitution.
  - Should define global principles, project truth layers, safety rules, validation policy, GitHub workflow, and cross-machine setup expectations.

- `docs/agent_threads/problem_representation.md`
  - Rules for the thread that turns a vague request into a clear issue.

- `docs/agent_threads/module_contract.md`
  - Rules for the thread that defines interfaces, invariants, and tests before implementation.

- `docs/agent_threads/implementation.md`
  - Rules for the thread that edits code against the contract.

- `docs/agent_threads/contract_test.md`
  - Rules for the thread that tests implementation against the contract.

- `docs/agent_threads/review.md`
  - Optional rules for fresh-context code review and PR feedback.

The visible effect should be that any new thread can be started with one sentence like:

```text
Use the Mythic Edge agent constitution and act as the module contract thread for issue #12.
```

## Scope

In scope:

- organizing durable agent behavior rules
- deciding which file is the constitution entrypoint
- splitting global rules from thread-role rules
- making rules portable across desktop, laptop, and GitHub checkouts
- defining how threads should reference issues, contracts, PRs, and validation evidence
- preserving plain-English user communication and project layer ownership
- preventing accidental secret, log, and workbook-drift mistakes

Out of scope:

- changing parser behavior
- changing workbook schema
- changing webhook payloads
- adding OpenAI API analytics
- redesigning the launcher
- replacing GitHub Actions
- deleting existing docs before a replacement exists

## Risks And Likely Breakpoints

- The constitution becomes too long, so agents skim or ignore important parts.
- `AGENTS.md` duplicates `docs/agent_constitution.md`, causing drift.
- Thread-role files conflict with the global constitution.
- Rules describe ideal behavior but do not include concrete validation commands.
- Agents on a laptop cannot find local generated data that exists on the desktop.
- Secret handling is under-specified and webhook URLs leak into commits.
- Contract-testing threads mutate implementation instead of reporting mismatches.
- Implementation threads over-refactor while trying to satisfy broad rules.
- Workbook-connected changes fail to distinguish repo state, live workbook state, and deployed Apps Script state.

## Validation Evidence Needed

Smallest useful checks:

```powershell
py -m pytest -q tests
py -m ruff check src tests
```

Documentation validation:

- A new thread can identify its role from the docs in under two minutes.
- A new thread can state which file contains global rules and which file contains role-specific rules.
- A new thread can explain where parser truth lives before touching workbook-facing logic.
- A new thread can name what must not be committed to GitHub.
- A new thread can list the required handoff artifact for its role.

GitHub validation:

- The files are committed and available after a fresh clone.
- GitHub Actions still passes after the docs are added.
- The issue template and PR template point to the same workflow vocabulary.

## Resolved Questions For v1

- `AGENTS.md` should be a concise senior-engineer entrypoint.
- GitHub issues should link to repo docs instead of copying full thread rules.
- Issue #1 should track v1 constitution work.
- Each thread-role file should include a canonical starter prompt.
- The constitution should include high-level AI/API analytics boundaries now, with implementation details deferred to a future module contract.
- Issue and PR templates should include short links to the relevant agent docs instead of copying full role rules.

## Remaining Open Questions

- Should future constitution updates require pull requests, or are direct commits acceptable for now while the repo is private?
- Should there be a dedicated `docs/contracts/agent_constitution.md` contract, or is the problem representation plus constitution enough?
