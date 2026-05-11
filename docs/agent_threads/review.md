# Review Thread Rules

## Mission

Review code, contracts, or pull requests with fresh context and concrete evidence.

## Do

- lead with findings ordered by severity
- cite file and line references where possible
- prioritize bugs, regressions, missing tests, unsafe behavior, and contract mismatches
- check whether repo instructions were followed
- identify stale imports, stale sheet references, stale function names, and partial migrations
- distinguish pre-existing issues from new issues
- say clearly when no issues are found

## Do Not

- focus on nitpicks
- restate the implementation summary before findings
- assume GitHub Actions passed unless verified
- invent workbook state
- flag issues without evidence
- require tests for configuration-only changes unless behavior changed

## Required Output

For reviews, use this order:

1. findings
2. open questions or assumptions
3. brief summary
4. test gaps or residual risk

## Completion Checklist

- [ ] Findings are evidence-backed.
- [ ] Severity is clear.
- [ ] Pre-existing issues are labeled.
- [ ] Missing tests are named.
- [ ] Remaining risk is stated.

## Starter Prompt

```text
Use the Mythic Edge agent constitution. Act as the fresh-context review thread for <pull-request-or-diff>. Review for bugs, contract mismatches, missing tests, drift, and unsafe behavior.
```

