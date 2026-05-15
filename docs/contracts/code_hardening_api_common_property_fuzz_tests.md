# Code Hardening API Common Property/Fuzz Test Contract

Source issue: https://github.com/Tahjali11/Mythic-Edge/issues/58

Tracker: https://github.com/Tahjali11/Mythic-Edge/issues/33

Module/surface:

- `src/mythic_edge_parser/parsers/api_common.py`
- `tests/test_api_common.py`

Branch target: `codex/code-hardening-suite`

Agent docs:

- `docs/agent_constitution.md`
- `docs/agent_rules.yml` from `origin/main`, because the current
  `codex/code-hardening-suite` branch inspected for this contract does not
  contain `docs/agent_rules.yml`
- `docs/agent_threads/module_contract.md`
- `docs/templates/module_contract.md`
- `docs/codex_module_workflow.md`

Parser API common artifacts read from `origin/main` because they are not
present on the current hardening branch:

- `docs/contracts/parser_api_common.md`
- `docs/implementation_handoffs/parser_api_common_comparison.md`
- `docs/contract_test_reports/parser_api_common.md`

Hardening context:

- Tracker #33: Code Hardening suite
- Issue #45 / PR #57: Pyright advisory type-checking completed and merged into
  `codex/code-hardening-suite` at `1481b027`
- `pyproject.toml` currently contains `pyright>=1.1,<2` in the dev optional
  dependency group
- `pyrightconfig.json` exists and Pyright remains advisory only

This contract defines a test-only hardening rollout for narrow property/fuzz
tests around `api_common.py`. It is a contract artifact only. It does not
implement tests, add Hypothesis, add any dependency, open a PR, target `main`,
or mark tracker #33 complete.

## Module

API common property/fuzz hardening tests.

The target runtime module is `src/mythic_edge_parser/parsers/api_common.py`.
The target test surface is `tests/test_api_common.py`, plus related parser
consumer tests for compatibility validation.

Plain English: this rollout should make the shared parser helper layer harder
to accidentally break by testing broad input invariants. It should not redesign
the helper behavior.

## Owning Layer

Parser and state interpretation, with Code Hardening test infrastructure.

Truth boundary:

- MTGA `Player.log` remains the raw evidence source.
- `api_common.py` owns shared raw-body helper behavior for JSON discovery,
  dict-only body parsing, API marker matching, and strict integer-list
  normalization.
- Individual parser modules own event-specific prefilters, payload extraction,
  and typed event payload semantics.
- Parser state owns live match/game interpretation and final reconciliation
  after parser events exist.
- Property/fuzz tests may assert the existing `api_common.py` contract. They
  must not move parser truth into tests, workbook formulas, dashboard logic,
  Apps Script, webhook transport, or AI analysis.
- Test failures may reveal contract drift, but this issue does not authorize
  parser behavior changes.

## Files Owned By This Contract

- `docs/contracts/code_hardening_api_common_property_fuzz_tests.md`

Expected future implementation files owned by this contract:

- `tests/test_api_common.py`
- `docs/implementation_handoffs/code_hardening_api_common_property_fuzz_tests_comparison.md`
- `docs/contract_test_reports/code_hardening_api_common_property_fuzz_tests.md`

Optional implementation file if Hypothesis is introduced:

- `pyproject.toml`, dev optional dependency only

Related files referenced but not owned by this contract:

- `src/mythic_edge_parser/parsers/api_common.py`
- `docs/contracts/parser_api_common.md`
- `docs/implementation_handoffs/parser_api_common_comparison.md`
- `docs/contract_test_reports/parser_api_common.md`
- `tests/test_client_actions_parser.py`
- `tests/test_gre_connect_resp_parser.py`
- `tests/test_gre_game_state_parser.py`
- `tests/test_match_state_parser.py`
- `tests/test_parsers.py`
- `tests/test_parser_regressions.py`
- `tests/test_connection_parsers.py`
- parser modules under `src/mythic_edge_parser/parsers/`
- `pyproject.toml`
- `pyrightconfig.json`
- `.github/workflows/repo-checks.yml`
- `tools/check_protected_surfaces.py`

## Branch And Baseline Expectations

Required branch target:

```text
codex/code-hardening-suite
```

Observed current branch state during this contract pass:

- The branch includes Pyright advisory work from PR #57.
- The branch has `pyrightconfig.json`.
- The branch has `pyright>=1.1,<2` in `pyproject.toml`.
- The branch does not contain `docs/agent_rules.yml`.
- The branch does not contain the parser-audit `parser_api_common` contract,
  implementation handoff, or contract-test report from `origin/main`.
- The branch-local `tests/test_api_common.py` has only the older four focused
  tests.
- `origin/main` contains the parser-audit `parser_api_common` artifacts and
  expanded deterministic test coverage recorded as 17 focused tests.

Implementation precondition:

- Codex C must verify whether `codex/code-hardening-suite` has been synced with
  the parser-audit/main `api_common` artifacts before adding property/fuzz
  tests.
- If the branch still lacks `docs/contracts/parser_api_common.md`,
  `docs/implementation_handoffs/parser_api_common_comparison.md`,
  `docs/contract_test_reports/parser_api_common.md`, and the expanded
  deterministic `tests/test_api_common.py` baseline, Codex C must stop and
  route to Codex G or an explicit branch-sync/integration thread before
  implementing property/fuzz tests.
- Codex C may read `origin/main` for comparison, but it must not silently
  implement tests against stale branch-local expectations.

Reason:

- Property/fuzz tests should harden the accepted parser API common contract,
  not rediscover or conflict with parser-audit decisions that already landed on
  `main`.

## Public Interface Under Test

This contract does not change public runtime interfaces. It tests the public
helpers defined by the parser API common contract:

```python
find_json_value(text: str) -> Any | None
parse_json_from_body(body: str, context: str = "") -> dict[str, Any] | None
is_api_request(body: str, name: str) -> bool
is_api_response(body: str, name: str) -> bool
normalize_int_list(value: Any) -> list[int]
```

Required compatibility:

- Keep helper names and signatures stable.
- Keep `api_common` exported through `mythic_edge_parser.parsers.__all__`.
- Preserve the existing parser API common contract unless a future parser
  issue and contract explicitly change it.

## Test-Only Scope

In scope:

- Add deterministic table-driven fuzz cases and/or property tests around
  `api_common.py`.
- Assert existing invariants for:
  - JSON discovery
  - dict-only parsing
  - API request/response marker matching
  - integer-list normalization
  - consumer parser compatibility
- Add a dev-only property-test dependency if the contract constraints below are
  followed.
- Record any property-found behavior ambiguity as follow-up rather than fixing
  parser code in this issue.

Out of scope:

- redesigning `api_common.py`
- changing first-decodable JSON precedence
- changing `parse_json_from_body()` dict-only behavior
- changing marker regex semantics or allowed-name capture rules
- changing integer-list normalization behavior
- aligning `normalize_int_list()` with parser-specific scalar numeric helpers
- changing GRE, client-action, match-state, collection, inventory, rank,
  session, connection, parser state, workbook, webhook, Apps Script, dashboard,
  or AI behavior
- adding runtime dependencies
- making property tests flaky, unbounded, or expensive

## Property/Fuzz Scope

### JSON Discovery

Target helper:

```python
find_json_value(text: str) -> Any | None
```

Allowed properties:

- For bounded string input, the helper should not raise for ordinary `str`
  values.
- For constructed text containing malformed JSON candidates before a valid JSON
  object or array, the first decodable candidate wins.
- For constructed text containing valid JSON followed by trailing noise, the
  valid JSON is returned.
- For constructed text with no decodable candidate, `None` is returned.
- Array values are valid `find_json_value()` outputs.

Required limits:

- Generated strings must be bounded in size.
- Generated valid JSON values should be JSON-serializable with standard
  `json.dumps()` without NaN/Infinity.
- Do not generate extremely deep or huge nested JSON.
- Do not require `find_json_value()` to parse non-string direct inputs.

### Dict-Only Parsing

Target helper:

```python
parse_json_from_body(body: str, context: str = "") -> dict[str, Any] | None
```

Allowed properties:

- Dict values returned by `find_json_value()` are returned as dicts.
- First decodable non-dict values produce `None`, even if a later dict exists.
- No decodable JSON produces `None`.
- `context` does not affect return values.

Required limits:

- Do not change or test for diagnostic side effects from `context`.
- Do not make `parse_json_from_body()` skip earlier arrays to find later dicts.

### API Marker Matching

Target helpers:

```python
is_api_request(body: str, name: str) -> bool
is_api_response(body: str, name: str) -> bool
```

Allowed properties:

- Generated API names from `[A-Za-z0-9_]+` match exactly when placed after the
  correct marker.
- Mismatched names return `False`.
- Matching remains case-sensitive.
- Whitespace and newlines between marker and name are accepted.
- Only the first marker match controls the result.
- Punctuation after an allowed-name prefix follows the existing partial-capture
  behavior.

Required limits:

- Do not broaden allowed API name characters.
- Do not make matching case-insensitive.
- Do not change first-match behavior to any-match behavior.
- Keep generated names bounded and non-empty.

### Integer-List Normalization

Target helper:

```python
normalize_int_list(value: Any) -> list[int]
```

Allowed properties:

- Non-list input returns `[]`.
- Returned values are `int` instances and never booleans.
- Non-bool integer objects are accepted as-is, including `0` and negative
  integer objects.
- ASCII digit strings are accepted after whitespace stripping.
- Signed strings, decimal strings, floats, bools, dicts, nested lists, empty
  strings, and `None` are skipped.
- Accepted values preserve order and duplicates.
- The returned list is independent from the input list.

Required limits:

- First rollout should restrict generated digit strings to ASCII digits unless
  Codex C explicitly chooses to document current Unicode digit behavior as an
  accepted open risk.
- Do not use property tests to redefine negative-string or Unicode-digit
  behavior.
- Do not align this helper with parser-specific `_maybe_int()` helpers.

### Consumer Compatibility

Consumer compatibility validation should cover existing parser suites rather
than adding broad property tests to every consumer module.

Required related checks after implementation:

- client actions
- GRE connect response
- GRE game state
- match state
- parser smoke/regression tests
- connection/parser tests when present on the synced branch

Property tests should stay centered on `api_common.py`; consumer tests should
prove the added hardening did not move behavior downstream.

## Hypothesis Policy

Hypothesis is allowed for Codex C only if these constraints are met.

Dependency constraints:

- Add Hypothesis only to `[project.optional-dependencies].dev` in
  `pyproject.toml`.
- Suggested range: `hypothesis>=6,<7`, unless Codex C records a reason to pin
  differently.
- Do not add Hypothesis as a runtime dependency.
- Do not add npm, npx, package-lock files, or a second package-manager
  ecosystem.
- Do not add Hypothesis in this Codex B contract writer pass.

If Codex C decides Hypothesis is not necessary:

- It may implement deterministic table-driven fuzz cases instead.
- It must explain why deterministic fuzz cases are enough for the first
  hardening rollout.
- It must not add any new dependency.

Stop condition:

- If adding Hypothesis causes install, CI, runtime, or Pyright advisory
  ambiguity that Codex C cannot keep bounded, route back to Codex B or the
  user before implementation.

## Deterministic And Non-Flaky Execution

Property/fuzz tests must be deterministic enough for local and GitHub Actions
execution.

Required settings if Hypothesis is used:

- Use bounded strategies.
- Use a bounded example count.
- Recommended first setting:

```python
@settings(max_examples=50, derandomize=True, deadline=None)
```

- Avoid tests that depend on wall-clock timing, network access, local files,
  local Hypothesis example databases, environment variables, or raw logs.
- Avoid unbounded Unicode text unless the test explicitly constrains or
  documents Unicode behavior.
- Avoid huge nested JSON structures.
- Prefer helper strategy functions with readable names over dense inline
  strategy expressions.

Database policy:

- Do not commit `.hypothesis/` or generated example databases.
- Property tests must pass from a clean clone without relying on a local
  example database.
- If Hypothesis reports a failing minimized example, Codex C should convert it
  into a deterministic regression example when possible.

Runtime budget:

- `py -m pytest -q tests\test_api_common.py` should remain fast enough for
  focused local use.
- The related parser validation slice should remain appropriate for routine
  hardening PR review.
- If property tests make full-suite runtime materially worse, reduce example
  counts or switch to deterministic table-driven fuzz cases.

## Expected Test Design

Recommended layout in `tests/test_api_common.py` after branch sync:

- Keep existing deterministic examples from the parser API common audit.
- Add a small, clearly named property/fuzz section.
- Prefer names that say the invariant, for example:
  - `test_find_json_value_property_valid_json_after_noise_round_trips`
  - `test_parse_json_from_body_property_non_dict_first_value_returns_none`
  - `test_api_marker_property_exact_ascii_names_match`
  - `test_normalize_int_list_property_returns_only_non_bool_ints`
- Keep property tests independent; one failure should point to one helper and
  one invariant.

Required behavior when a property test exposes a mismatch:

- If the mismatch violates the existing parser API common contract, route to
  Codex D or a focused bug issue only after reviewer confirmation.
- If the mismatch exposes contract ambiguity, route back to Codex B.
- If the mismatch requires parser behavior changes, stop. This issue is
  test-only and does not authorize behavior changes.

## Validation Requirements

Codex B contract-only validation:

```powershell
git diff --check
```

Codex C/E focused validation after test or dev-dependency changes:

```powershell
py -m pytest -q tests\test_api_common.py
py -m pytest -q tests\test_api_common.py tests\test_client_actions_parser.py tests\test_gre_connect_resp_parser.py tests\test_gre_game_state_parser.py
py -m pytest -q tests\test_parsers.py tests\test_match_state_parser.py
py -m ruff check src tests
git diff --check
```

Additional validation when the synced branch includes these tests:

```powershell
py -m pytest -q tests\test_connection_parsers.py tests\test_parser_regressions.py
```

Hardening validation:

```powershell
py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite
```

Pyright validation:

```powershell
pyright --project pyrightconfig.json
```

Interpretation:

- Pyright remains advisory under issue #45 / PR #57.
- Zero Pyright findings is not required by this issue.
- If Hypothesis is added, tests and Ruff must still pass.
- If Hypothesis is not added, Codex C must state that deterministic fuzz cases
  were chosen and no dependency was changed.

Before Codex F submitter work:

```powershell
py -m pytest -q
py -m ruff check src tests tools
git diff --check
py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite
```

## Protected Surfaces

This issue must preserve:

- parser behavior outside test-only hardening scope
- parser state final reconciliation
- workbook schema
- webhook payload shape
- Apps Script behavior
- parser event classes
- match identity
- game identity
- production deduplication semantics
- secrets, credentials, API keys, environment variables, tokens, or webhook
  URLs
- raw local logs
- generated card/tier data
- runtime status files
- failed posts
- workbook exports
- `main` or production branches

Allowed hardening surfaces:

- `tests/test_api_common.py`
- dev-only test dependency metadata in `pyproject.toml`, if Hypothesis is
  introduced under this contract
- hardening docs under `docs/contracts/`, `docs/implementation_handoffs/`, and
  `docs/contract_test_reports/`

## Stop Conditions

Stop and route back to Codex B, Codex A, Codex G, or the user if:

- `codex/code-hardening-suite` is still stale relative to the parser API common
  artifacts on `origin/main` and implementation would add tests against the
  stale branch-local baseline.
- Hypothesis requires runtime dependency changes.
- property tests require parser behavior changes to pass.
- property tests become flaky, unbounded, or too slow for routine CI.
- generated tests require raw local logs, runtime files, failed posts, workbook
  exports, or generated private data.
- implementation would touch parser state, final reconciliation, workbook
  schema, webhook payload shape, Apps Script behavior, parser event classes,
  match/game identity, deduplication, secrets, environment variables, raw logs,
  generated data, runtime status files, failed posts, or workbook exports.
- implementation would target `main`.
- implementation would close tracker #33.

## Side Effects

Allowed side effects for future implementation:

- Add or update tests.
- Add a dev-only Hypothesis dependency if chosen and justified.
- Write implementation handoff and contract-test report artifacts.

Forbidden side effects:

- Do not mutate runtime parser code in this hardening test rollout.
- Do not change parser events, state, workbook rows, webhook payloads, Apps
  Script, match/game identity, deduplication, environment variable semantics,
  secrets, raw logs, generated data, runtime status, failed posts, or workbook
  exports.
- Do not write local generated artifacts.
- Do not open a PR from the implementer unless explicitly asked.
- Do not mark tracker #33 complete.

## Dependency Order

Future Codex C should proceed in this order:

1. Confirm branch is `codex/code-hardening-suite`.
2. Fetch `origin/main` and `origin/codex/code-hardening-suite`.
3. Verify branch-sync state for:
   - `docs/agent_rules.yml`
   - `docs/contracts/parser_api_common.md`
   - `docs/implementation_handoffs/parser_api_common_comparison.md`
   - `docs/contract_test_reports/parser_api_common.md`
   - expanded deterministic `tests/test_api_common.py`
4. If the hardening branch is stale, stop and route to Codex G or an explicit
   integration sync before test implementation.
5. Compare current `api_common.py` and tests against the parser API common
   contract.
6. Decide whether Hypothesis is justified or deterministic fuzz cases are
   enough.
7. Add only focused tests and optional dev-only dependency metadata.
8. Run focused and related validation.
9. Produce implementation handoff.
10. Route to Codex E for contract-test review.

## Compatibility

Must remain stable:

- `api_common.py` public helper names and signatures
- first-decodable JSON precedence
- dict-only `parse_json_from_body()`
- exact, case-sensitive, first-match API marker matching
- `[A-Za-z0-9_]` API name capture behavior
- `normalize_int_list()` bool rejection
- `normalize_int_list()` ASCII digit-string acceptance
- `normalize_int_list()` signed-string and float rejection
- accepted order and duplicate preservation
- distinction between shared list normalization and parser-specific scalar
  numeric helpers
- Pyright advisory-only policy from issue #45 / PR #57
- hardening branch target: `codex/code-hardening-suite`

Breaking changes requiring a new contract:

- changing runtime parser behavior
- changing helper signatures
- changing marker regexes
- changing integer normalization semantics
- adding Hypothesis as a runtime dependency
- making property tests broad enough to destabilize CI
- requiring zero Pyright findings
- changing protected parser/runtime/workbook/App Script surfaces

## Acceptance Criteria

- `docs/contracts/code_hardening_api_common_property_fuzz_tests.md` exists.
- The contract defines a test-only hardening rollout.
- The contract names branch/base expectations and the branch-sync requirement.
- The contract preserves the parser API common contract as the behavior source.
- The contract defines property/fuzz scope for JSON discovery, dict-only
  parsing, marker matching, and integer-list normalization.
- The contract states whether Hypothesis is allowed and under what constraints.
- The contract defines deterministic/non-flaky settings and runtime budgets.
- The contract defines validation evidence and protected-surface checks.
- The contract forbids parser behavior changes and protected-surface changes.
- The contract routes next work to Codex C: Module Implementer / comparison
  thread.

## Handoff Packet

Role performed: Codex B: Module Contract Writer.

Source problem representation: https://github.com/Tahjali11/Mythic-Edge/issues/58

Tracker issue: https://github.com/Tahjali11/Mythic-Edge/issues/33

Contract produced:
`docs/contracts/code_hardening_api_common_property_fuzz_tests.md`

Risk tier: Medium.

Owning truth layer: parser and state interpretation, with Code Hardening test
infrastructure.

Public interface:

- No runtime interface changes.
- Test surface: `tests/test_api_common.py`.
- Optional dev-only dependency: Hypothesis, only if Codex C chooses it under
  this contract.

Invariants:

- Preserve parser API common behavior.
- Keep rollout test-only.
- Keep property/fuzz tests deterministic and bounded.
- Keep Pyright advisory-only.
- Do not change protected parser/runtime/workbook/App Script surfaces.
- Do not implement against a stale hardening branch baseline.

Required tests and validation: listed above.

Acceptance criteria: listed above.

Open questions or contract risks:

- Whether Codex G or another integration step should sync `origin/main`
  parser-audit artifacts into `codex/code-hardening-suite` before Codex C.
- Whether Hypothesis is worth the new dev dependency, or deterministic fuzz
  cases are enough for the first hardening pass.
- Whether Unicode digit behavior should stay an open risk or become a focused
  deterministic test.
- Whether consumer compatibility should expand beyond the named parser suites
  after branch sync.

Next recommended thread role: Codex C: Module Implementer / comparison thread.

Pasteable next-thread prompt:

```text
Use the Mythic Edge agent constitution.

Act as Codex C: Module Implementer / comparison thread for https://github.com/Tahjali11/Mythic-Edge/issues/58.

Tracker:
https://github.com/Tahjali11/Mythic-Edge/issues/33

Branch target:
codex/code-hardening-suite

Use:
- docs/agent_constitution.md
- docs/agent_rules.yml, or origin/main:docs/agent_rules.yml if still absent on the hardening branch
- docs/agent_threads/implementation.md
- docs/codex_module_workflow.md
- docs/contracts/code_hardening_api_common_property_fuzz_tests.md
- docs/contracts/parser_api_common.md from the synced branch or origin/main
- docs/implementation_handoffs/parser_api_common_comparison.md from the synced branch or origin/main
- docs/contract_test_reports/parser_api_common.md from the synced branch or origin/main
- pyproject.toml
- pyrightconfig.json
- src/mythic_edge_parser/parsers/api_common.py
- tests/test_api_common.py
- tests/test_client_actions_parser.py
- tests/test_gre_connect_resp_parser.py
- tests/test_gre_game_state_parser.py
- tests/test_match_state_parser.py
- tests/test_parsers.py
- tests/test_parser_regressions.py
- issue #33
- issue #58
- issue #45 / PR #57 Pyright advisory context

Goal:
Compare the current hardening branch and api_common test surface against docs/contracts/code_hardening_api_common_property_fuzz_tests.md. Implement only the smallest test-only hardening changes needed to satisfy the contract, then produce docs/implementation_handoffs/code_hardening_api_common_property_fuzz_tests_comparison.md.

Before editing:
- Confirm the branch is codex/code-hardening-suite.
- Verify whether the hardening branch includes the parser API common contract artifacts and expanded deterministic tests from origin/main.
- If the branch is stale, stop and route to Codex G or an explicit integration sync before adding property/fuzz tests.
- State whether you will use Hypothesis or deterministic table-driven fuzz cases, and why.

Do:
- Preserve the parser API common contract.
- Prefer test additions over behavior changes.
- Keep property/fuzz tests narrow, deterministic, bounded, and non-flaky.
- Add Hypothesis only as a dev optional dependency if justified by the contract.
- Run focused and related parser validation.
- Keep Pyright advisory-only.
- Produce the implementation handoff with branch-sync status, files changed, tests added, dependency decision, validation, residual risks, and next recommended role.

Do not:
- Implement against a stale branch baseline.
- Change parser behavior.
- Change parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports.
- Add Hypothesis as a runtime dependency.
- Make property tests flaky, unbounded, or slow.
- Require zero Pyright findings.
- Target main.
- Mark tracker #33 complete.
- Stage, commit, open a PR, or merge unless explicitly asked.

Validation:
py -m pytest -q tests\test_api_common.py
py -m pytest -q tests\test_api_common.py tests\test_client_actions_parser.py tests\test_gre_connect_resp_parser.py tests\test_gre_game_state_parser.py
py -m pytest -q tests\test_parsers.py tests\test_match_state_parser.py
py -m ruff check src tests
git diff --check
py tools\check_protected_surfaces.py --base origin/codex/code-hardening-suite
pyright --project pyrightconfig.json
```

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/58"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/33"
  completed_thread: "B"
  next_thread: "C"
  next_role: "Codex C: Module Implementer / comparison thread"
  source_artifact: "docs/contracts/code_hardening_api_common_property_fuzz_tests.md"
  target_artifact: "docs/implementation_handoffs/code_hardening_api_common_property_fuzz_tests_comparison.md"
  risk_tier: "Medium"
  branch: "codex/code-hardening-suite"
  validation:
    - "git diff --check"
  stop_conditions:
    - "Do not implement against a stale hardening branch baseline; sync or route before adding tests."
    - "Do not change parser behavior."
    - "Do not change parser state final reconciliation, workbook schema, webhook payload shape, Apps Script behavior, parser event classes, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed posts, or workbook exports."
    - "Do not add Hypothesis as a runtime dependency."
    - "Do not make property/fuzz tests flaky, unbounded, or slow."
    - "Do not require zero Pyright findings."
    - "Do not target main; hardening work belongs on codex/code-hardening-suite."
    - "Do not mark tracker #33 complete."
```
