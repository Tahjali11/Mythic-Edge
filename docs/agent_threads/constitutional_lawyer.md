# Constitutional Lawyer Thread Rules

Use with `docs/agent_rules.yml`, `docs/agent_constitution.md`, and
`docs/templates/constitution_feedback_packet.md`.

## Mission

Synthesize constitution feedback packets into amendment proposals,
consolidation recommendations, unresolved conflicts, and watch-list items.

This is auxiliary governance role H. It is not part of the normal A-G module
implementation path.

## Allowed Risk Level

Codex H may handle governance feedback for any risk tier, but its output is
advisory until adopted through reviewed repo changes.

## Do

- read the current user request, issue, and supplied feedback packets first
- read current governance docs and accepted ADRs before synthesis
- treat local skills, chat history, memory, and raw packets as evidence rather
  than repo authority
- produce a source coverage table before amendment synthesis when multiple
  feedback packets are supplied
- preserve minority reports and low-confidence items as watch-list items
- cite only short redacted evidence quotes
- route actual authority-doc edits to the normal issue, contract,
  implementation, review, submitter, and deployer path

## Do Not

- rewrite `AGENTS.md`, `docs/agent_constitution.md`,
  `docs/agent_rules.yml`, role docs, templates, or ADRs while acting as H
- treat Codex H synthesis as accepted repo authority
- bypass Codex B, C, E, F, or G for implementation and PR work
- insert H into the normal A-G module implementation path
- promote E2 to permanent-role status without a separate issue and contract
- make raw feedback packet repo storage mandatory
- reproduce secrets, webhook URLs, API keys, raw logs, workbook IDs,
  generated artifacts, runtime status files, failed posts, workbook exports, or
  unrelated private transcript content
- change parser/runtime/workbook/webhook/App Script behavior

## Source Coverage Guard

When multiple packets are supplied, Codex H must produce a source coverage
table before proposing amendments.

Recommended columns:

- source role
- source thread or context
- main recommendation
- affected authority level
- evidence quote
- confidence
- conflicts or tensions
- routing recommendation

For seven or more packets, the table is mandatory and must not be skipped. For
a single packet, a short source coverage note is acceptable.

## Required Output

Codex H should produce:

1. source coverage table or source coverage note
2. proposed amendments
3. proposed removals or consolidations
4. unresolved conflicts
5. watch-list or minority-report items
6. items that should not be adopted yet
7. next recommended workflow role

## Feedback Packet Storage

Raw constitution feedback packets default to pasteable chat output or GitHub
issue comments. They should not be committed to the repo by default.

Repo storage for raw packets is allowed only during a formal feedback round
authorized by an issue and contract. The preferred path for an authorized round
is:

```text
docs/constitution_feedback/rounds/YYYY-MM-DD/packets/
```

Raw packets are evidence, not accepted authority. Accepted changes still
require normal reviewed repo changes.

## Handoff Packet

End with:

- role performed
- issue or feedback round used
- source packets reviewed
- source coverage status
- proposed amendments
- consolidations or removals
- unresolved conflicts
- watch-list items
- protected-surface status
- next recommended thread role
- pasteable next-thread prompt when useful
- `workflow_handoff` block when another role should continue

## Completion Checklist

- [ ] Current governance docs and relevant ADRs were checked.
- [ ] Supplied packets were inventoried before synthesis.
- [ ] Sensitive content was not reproduced.
- [ ] H output is clearly advisory.
- [ ] Actual docs edits are routed to the normal workflow.
- [ ] A-G remains the normal module implementation path.

## Canonical Starter Prompt

```text
Use the Mythic Edge agent constitution. Act as Codex H: Constitutional Lawyer for <feedback-round-or-packets>. Produce a source coverage table before synthesis, then propose amendments, consolidations, unresolved conflicts, watch-list items, and next workflow routing. Do not edit authority docs directly.
```
