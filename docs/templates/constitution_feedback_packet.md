# Constitution Feedback Packet

Use this compact shape for pasteable constitution feedback packets and GitHub
issue comments. Raw packets are evidence for Codex H synthesis; they are not
accepted repo authority by themselves.

Do not include secrets, webhook URLs, API keys, tokens, workbook IDs, raw MTGA
logs, generated local artifacts, runtime status files, failed posts, workbook
exports, or unrelated private transcript content.

```md
## Constitution Feedback Packet

source_role: Codex <role or source>
source_thread_or_context: <short thread, issue, PR, or context label>
related_issue_or_pr: <issue/PR if known, otherwise N/A>
date_collected: YYYY-MM-DD
status: raw feedback packet
storage_recommendation: issue comment by default; repo file only during formal feedback round

### Original Constitutional Comment

<paste or summarize the prior constitutional review comment here>

### Proposed Constitutional Improvement

<state the concrete rule, clarification, removal, or consolidation>

### Why This Matters

<explain the failure, confusion, drift, or workflow problem this prevents>

### Suggested Authority Level

Choose one:

- AGENTS.md entrypoint
- docs/agent_constitution.md
- docs/agent_rules.yml
- docs/agent_threads/<role>.md
- docs/templates/<template>.md
- ADR
- watch-list only

### Affected Roles

<list A-G roles affected, Codex H if relevant, or say N/A>

### Affected Protected Surfaces

<list any protected surfaces affected, or say N/A>

### Conflict Or Tension

<state any conflict with current rules, ADRs, workflow docs, or role boundaries; if none, say None known>

### Confidence

Choose one:

- High: should become an amendment proposal
- Medium: should be considered but reviewed carefully
- Low: preserve as watch-list or minority-report item

### Evidence Quote

<short redacted quote; do not include secrets, raw logs, workbook IDs, webhook URLs, or transcript dumps>

### Routing Recommendation

<state whether Codex H should propose an amendment, consolidate/remove wording, preserve an unresolved conflict, or place it on the watch list>

### Later Synthesis Status

Optional Codex H annotation. Packet authors may leave this blank.

Choose one when synthesizing against current repo state:

- active
- partially_satisfied
- satisfied
- stale
- superseded
- conflict
- watch_list

### Later Amendment Quality Review

Optional Codex H annotation. Packet authors may leave this blank.

recommended_rule_type: <hard_rule | operating_default | role_procedure | template_field | machine_rule | adr_candidate | watch_list | no_action>
failure_mode_prevented: <real or credible failure mode, or N/A>
ceremony_impact: <lower | same | higher_justified | higher_not_justified>
best_practice_mapping: <authority hierarchy | critique-before-revision | risk-tiered oversight | auditability | tool-surface boundary | lifecycle governance | other | N/A>
tool_surface_impact: <tool/collaboration surfaces affected, or N/A>
```

Formal repo storage for raw packets is opt-in. It requires an explicit issue and
contract authorizing a feedback round and storage path such as:

```text
docs/constitution_feedback/rounds/YYYY-MM-DD/packets/
```
