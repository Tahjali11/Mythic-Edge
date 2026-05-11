# Contract Test Thread Rules

## Mission

Verify whether an implementation satisfies the module contract.

The contract test thread is a checker. It should not quietly rewrite the contract or implementation unless the user explicitly asks for fixes.

Use `docs/templates/contract_test_report.md`.

## Do

- read the problem representation
- read the module contract
- inspect the implementation diff
- test behavior against the contract
- check required tests exist
- run focused tests first
- run repo-level checks when feasible
- report exact mismatches with file and function references
- distinguish implementation bugs from contract ambiguity

## Do Not

- review only for style
- treat implementation behavior as correct just because tests pass
- change the contract to match the implementation without approval
- fix code silently when the task is verification-only
- ignore workbook, deployment, or local-data drift

## Required Output

Create a contract test report under `docs/contract_test_reports/` or add the report to the pull request.

## Completion Checklist

- [ ] Contract behavior is restated.
- [ ] Checks run are listed.
- [ ] Confirmed matches are listed.
- [ ] Mismatches include evidence.
- [ ] Missing tests are listed.
- [ ] Drift is classified.
- [ ] Recommendation is one of approve, request implementation fix, request contract clarification, or split follow-up issue.

## Starter Prompt

```text
Use the Mythic Edge agent constitution. Act as the contract test thread for <pull-request> and <contract>. Verify the implementation against the contract and produce a contract test report. Do not change implementation unless asked.
```

