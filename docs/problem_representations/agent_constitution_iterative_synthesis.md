# Agent Constitution Iterative Synthesis

## Summary

Mythic Edge needs a repeatable way for local Codex threads to turn their visible workflow experience into structured constitution feedback packets, then route those packets to Codex H / Constitutional Lawyer for synthesis.

The goal is to improve the constitution from multiple thread experiences without committing every raw feedback packet to the repo or overfitting governance rules to one thread.

## What The Workflow Is Supposed To Do

Local Codex threads should be able to:

1. Review their visible local chat history and workflow experience.
2. Read the current repo authorities.
3. Read archived constitution drafts when relevant and available.
4. Produce a structured constitution feedback packet.
5. Include short direct evidence quotes when useful.
6. Preserve low-confidence suggestions in a watch list.
7. Avoid editing authority docs directly.
8. Hand packets to Codex H for synthesis.

Codex H should then synthesize multiple packets into amendment proposals, minority reports, watch lists, and next-role handoffs.

## What It Is Actually Doing

Before this workflow, constitution feedback lived mostly in chat history, ad hoc amendments, or the user's memory. Useful lessons could be lost, repeated friction could remain invisible, and one thread's local experience could accidentally over-influence the next constitution draft.

## Why This Matters

The constitution governs how agents handle parser truth ownership, GitHub workflow, protected surfaces, secrets, local artifacts, workbook drift, AI boundaries, and role handoffs.

Constitution amendments should be informed by real thread experience, but they should not depend on unstructured chat memory or raw transcript dumps.

## Project Layer

Primary layer:

- workflow / governance

Affected surfaces:

- `AGENTS.md`
- `docs/agent_constitution.md`
- `docs/agent_rules.yml`
- `docs/codex_module_workflow.md`
- `docs/agent_threads/`
- `docs/templates/`
- `docs/codex_skills/`
- accepted ADRs in `docs/decisions/`

## Policy Decisions

Individual constitution feedback packets should not be committed to the repo by default.

Preferred packet storage:

- dedicated GitHub issue comments for the feedback round
- pasted packets in the synthesis thread
- temporary ignored local scratch files when explicitly needed

Repo-committed artifacts should normally be limited to:

- packet templates
- skill instructions
- synthesis artifacts
- accepted ADRs when needed
- final reviewed constitution amendment PRs

Packets should include direct quotes from chat only when they materially support a recommendation. Quotes must be short, targeted, and redacted.

Each packet should identify:

- feedback round issue
- source workflow role
- related issue or PR when relevant
- project phase
- friction category

Codex H should run:

- after major suites
- before major governance changes
- after serious workflow failures

Low-confidence suggestions should be preserved in a watch list or minority report instead of being forced into the next constitution draft.

## Scope

In scope:

- Codex H role definition.
- Constitution feedback packet template.
- Repo-owned constitution-review skill.
- Skill installation support.
- Agent docs validation for the new role and skill.
- Role-scope checks that prevent H from directly mutating authority docs.

Out of scope:

- Directly rewriting the constitution from a feedback packet.
- Committing raw feedback packets by default.
- Treating local chat history as higher authority than repo docs.
- Changing parser behavior, workbook schema, webhook shape, Apps Script behavior, parser state final reconciliation, match/game identity, deduplication, secrets, local generated artifacts, runtime status files, failed posts, or workbook exports.

## Risks And Likely Breakpoints

- Packets become too verbose and reproduce full chat transcripts.
- Feedback packets get committed and bloat the repo.
- H overfits to one thread's experience instead of comparing multiple packets.
- H rewrites authority docs directly instead of producing synthesis and routing to a contract/implementation thread.
- Direct quotes accidentally include secrets, webhook URLs, raw logs, workbook IDs, or private local details.
- Low-confidence suggestions are silently discarded instead of preserved as watch-list items.
- Current repo authority, accepted ADRs, and active issues/contracts conflict with an older archived draft.

## Validation Evidence Needed

```powershell
py tools\check_agent_docs.py
py -m pytest -q tests\test_agent_hardening_tools.py
py tools\check_secret_patterns.py --all
git diff --check
```

When submitting the workflow update:

```powershell
py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite
.\tools\run_repo_checks.ps1
```

## Next Workflow Action

Next role:

- Codex B / Module Contract Writer if this workflow needs a formal contract before broader adoption.
- Codex H / Constitutional Lawyer when enough feedback packets exist for synthesis.

Pasteable prompt:

```text
Use $mythic-edge-workflow. If older context conflicts with the skill, AGENTS.md, docs/agent_rules.yml, docs/agent_constitution.md, docs/codex_module_workflow.md, the current GitHub issue, or the current contract, prefer the current repo artifacts. Act as Codex H: Constitutional Lawyer for the current constitution feedback round. Read the feedback packets supplied in the issue comments or prompt, current repo authorities, accepted ADRs, and archived drafts. Synthesize proposed amendments, proposed removals or consolidations, unresolved conflicts, and watch-list items. Do not rewrite the constitution directly.
```

```yaml
workflow_handoff:
  issue: ""
  completed_thread: "A"
  next_thread: "H"
  source_artifact: "docs/problem_representations/agent_constitution_iterative_synthesis.md"
  target_artifact: "feedback-round issue comment or docs/problem_representations/agent_constitution_next_synthesis.md"
  risk_tier: "Medium; High if authority docs are later changed"
  branch: "codex/code-hardening-suite"
  validation:
    - "py tools\\check_agent_docs.py"
    - "py -m pytest -q tests\\test_agent_hardening_tools.py"
    - "py tools\\check_secret_patterns.py --all"
    - "git diff --check"
  stop_conditions:
    - "Do not rewrite docs/agent_constitution.md directly."
    - "Do not commit raw feedback packets by default."
    - "Do not treat chat history as higher authority than current repo artifacts."
```
