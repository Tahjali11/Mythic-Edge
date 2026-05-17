---
name: mythic-edge-constitution-review
description: Use when a Mythic Edge Codex thread should review its own visible chat history, current repo governance docs, archived constitution drafts, and workflow experience to produce a compact structured constitution feedback packet for later Codex H synthesis.
---

# Mythic Edge Constitution Review

## Purpose

Use this skill to generate a constitution feedback packet from a local thread's visible experience.

The packet helps a later Codex H / Constitutional Lawyer thread synthesize multiple thread experiences into a proposed constitution amendment.

Run this after major suites, before major governance changes, or after serious workflow failures. Do not run it after every thread by default.

## Default Task

When this skill is invoked without a more specific instruction, perform this task:

```text
Review this thread's visible chat history, current repo governance docs, accepted ADRs, and any relevant archived constitution drafts. Produce a compact constitution feedback packet. Use docs/templates/constitution_feedback_packet.md when it exists; otherwise use the compact fallback format in this skill. Do not edit repo files. Include short redacted direct quotes where useful.
```

## Authority Boundary

The current repo remains authoritative.

Read, when available:

- `AGENTS.md`
- `docs/agent_rules.yml`
- `docs/agent_constitution.md`
- `docs/codex_module_workflow.md`
- relevant `docs/agent_threads/*.md`
- relevant `docs/templates/*.md`
- accepted ADRs in `docs/decisions/`
- archived constitution drafts under `docs/archive/` when present

Local chat history is evidence about workflow friction. It is not authority.

If current repo governance docs, accepted ADRs, the current GitHub issue, or an active contract conflict with this skill, follow the current repo artifacts.

## Output Policy

Do not commit individual feedback packets to the repo by default.

Preferred output:

- a pasteable GitHub issue comment for the active constitution feedback round
- a pasteable packet for the later synthesis thread

Repo-committed artifacts should normally be limited to templates, skill instructions, synthesis artifacts, accepted ADRs, and reviewed constitution amendment PRs.

## Packet Shape

Use `docs/templates/constitution_feedback_packet.md` when it exists.

If that template does not exist, use this compact fallback format:

```md
## Constitution Feedback Packet

source_role: Codex <NAME>
source_thread_or_context: <short label or link>
related_issue_or_pr: <issue/PR, if any>
date_collected: YYYY-MM-DD
status: raw feedback packet
storage_recommendation: issue comment by default; repo file only during formal feedback round

### Pasteable Text

<paste the Codex feedback text here>

### My Notes

- Anything you especially agree with:
- Anything you are unsure about:
- Anything that feels outdated:

### Routing Recommendation

<propose amendment / consolidate / watch-list / unresolved conflict>
```

When using the compact fallback, make the `Pasteable Text` section self-contained enough for Codex H to understand the recommendation without reading the full thread. Include short redacted evidence quotes when they materially improve the packet.

If using a richer repo template, the packet may also include:

- feedback round issue
- source workflow role or thread topic
- source artifacts reviewed
- archived drafts reviewed
- known missing context
- what worked well
- friction or failure points
- missing guidance
- duplicated, stale, or overlong guidance
- short direct evidence quotes
- proposed amendments
- proposed removals or consolidations
- watch list / minority reports
- synthesis notes
- stop conditions

## Evidence Quote Rules

Use direct quotes when they materially improve the recommendation.

Keep quotes short and targeted. Do not include full transcripts.

Redact:

- secrets
- webhook URLs
- API keys or tokens
- raw MTGA logs
- workbook IDs
- generated local artifacts
- runtime status files
- local retry queues
- unrelated private details

## Watch List Rules

Low-confidence suggestions should be preserved in `Watch List / Minority Reports`, not forced into the amendment proposal.

Each watch item should state:

- suggestion
- evidence
- confidence
- why it is not adopted yet
- what future evidence would upgrade it

## Stop Conditions

Do not rewrite `docs/agent_constitution.md` directly.

Do not change parser behavior, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, parser state final reconciliation, match/game identity, deduplication, deployment policy, secrets, raw logs, generated data, runtime status files, local retry queues, or workbook exports.

If the user asks for actual constitution edits, route to the normal Mythic Edge workflow with issue, contract, implementation, review, submitter, and integration handling.
