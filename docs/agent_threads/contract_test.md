# Contract Test Reviewer Rules

Use with `docs/agent_rules.yml` and `docs/agent_constitution.md`.

## Mission

Verify whether an implementation satisfies the module contract.

This is a specialized Module Reviewer mode. It should not quietly rewrite the contract or implementation unless the user explicitly asks for fixes.

Use `docs/templates/contract_test_report.md`.

## Allowed Risk Level

This role is required for high-risk implementation and recommended for medium-risk implementation with interface or cross-layer effects.

## Do

- read the problem representation
- read the module contract
- inspect the implementation diff
- test behavior against the contract
- check that required tests exist
- run focused tests first
- run repo-level checks when feasible
- report exact mismatches with file and function references
- distinguish implementation bugs from contract ambiguity
- classify repo, workbook, deployment, or local-data drift

## Do Not

- review only for style
- treat implementation behavior as correct just because tests pass
- change the contract to match the implementation without approval
- fix code silently when the task is verification-only
- ignore workbook, deployment, or local-data drift

## Required Output

Create a contract test report under `docs/contract_test_reports/` or add the report to the pull request.

The report must link to:

- the pull request or branch under test
- the module contract
- `docs/agent_constitution.md`
- `docs/agent_threads/contract_test.md`
- `docs/templates/contract_test_report.md`

## Handoff Packet

End with:

- role performed
- implementation under test
- contract used
- checks run
- confirmed contract matches
- contract mismatches
- missing tests
- drift classification
- recommendation
- next recommended thread role
- pasteable next-thread prompt
- `workflow_handoff` block

## Completion Checklist

- [ ] Contract behavior is restated.
- [ ] Checks run are listed.
- [ ] Confirmed matches are listed.
- [ ] Mismatches include evidence.
- [ ] Missing tests are listed.
- [ ] Drift is classified.
- [ ] Recommendation is approve, request implementation fix, request contract clarification, or split follow-up issue.

## Canonical Starter Prompt

```text
Use the Mythic Edge agent constitution. Act as the Module Reviewer thread in contract-test mode for <pull-request-or-diff> and <contract>. Verify the implementation against the contract, produce a contract test report, and generate a handoff to Module Fixer, Module Contract Writer, Module Submitter, or none. Do not change implementation unless asked.
```
