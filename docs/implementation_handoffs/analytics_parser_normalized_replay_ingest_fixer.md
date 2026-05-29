# Analytics Parser-Normalized Replay Ingest Fixer Handoff

## Role Performed

Codex D: Module Fixer.

## Source Finding

Codex E requested an implementation fix:

- P1: fractional numeric values were silently truncated by `_optional_int()`,
  including `Game Number 1.5` becoming `game_id :g1`.
- P2: negative parser-owned counts were accepted for fields such as
  `Mulligans`, `Opening Hand Size`, `Turn Count`, `Games Won`, and
  `Total Games`.

## Source Artifacts

- Contract: `docs/contracts/analytics_parser_normalized_replay_ingest.md`
- Implementation handoff:
  `docs/implementation_handoffs/analytics_parser_normalized_replay_ingest_comparison.md`
- Branch: `codex/analytics-foundation`
- Role guide: `docs/agent_threads/module_fixer.md`
- Constitution: `docs/agent_constitution.md`

## Fault Category

Implementation mismatch against the parser-normalized replay ingest contract.

The ingest helper accepted values with Python's broad `int(...)` conversion,
which truncates floats and accepts negative values unless separately guarded.
Those behaviors are not valid for parser-owned integer facts.

## Fix Produced

Updated `_optional_int()` in `src/mythic_edge_parser/app/analytics_ingest.py`
to:

- preserve empty optional values as unavailable
- reject booleans
- reject fractional floats such as `1.5`
- reject non-integer strings such as `1.5`
- accept integer objects and integer text such as `1`
- enforce non-negative integers by default
- keep `Game Number` positive through `_required_positive_int()`

No parser behavior, parser row shape, workbook schema, webhook payload, Apps
Script behavior, live ingest, replay runner, CLI, or production behavior was
changed.

## Files Changed

- `src/mythic_edge_parser/app/analytics_ingest.py`
- `tests/test_analytics_parser_normalized_replay_ingest.py`
- `docs/implementation_handoffs/analytics_parser_normalized_replay_ingest_fixer.md`

Existing C-thread files remain present in the working tree:

- `docs/contracts/analytics_parser_normalized_replay_ingest.md`
- `docs/implementation_handoffs/analytics_parser_normalized_replay_ingest_comparison.md`

## Tests Added Or Updated

Updated `tests/test_analytics_parser_normalized_replay_ingest.py` with focused
regression coverage:

- fractional `Game Number`, `Mulligans`, `Opening Hand Size`, `Turn Count`,
  `Games Won`, and `Total Games` fail without partial fact rows
- negative `Mulligans`, `Opening Hand Size`, `Turn Count`, `Games Won`, and
  `Total Games` fail without partial fact rows

Focused result before the implementation fix:

```text
py -m pytest -q tests\test_analytics_parser_normalized_replay_ingest.py
11 failed, 13 passed
```

Focused result after the implementation fix:

```text
py -m pytest -q tests\test_analytics_parser_normalized_replay_ingest.py
24 passed
```

## Validation Evidence

```text
py -m pytest -q tests\test_analytics_parser_normalized_replay_ingest.py tests\test_analytics_schema.py tests\test_analytics_migration_loader.py
51 passed
```

```text
py -m pytest -q tests\test_app_models.py tests\test_golden_replay_harness.py
29 passed
```

```text
py -m pytest -q tests\test_gameplay_actions.py tests\test_opponent_card_observations.py
26 passed
```

```text
py -m ruff check src tests tools
All checks passed!
```

```text
git diff --check
passed
```

```text
py tools\check_agent_docs.py
passed; errors 0; warnings 0
```

```text
path-scoped secret/private-marker scan over contract, comparison handoff,
fixer handoff, ingest module, and ingest tests
result: warning; forbidden 0; warnings 1 on existing contract protected-surface wording
```

```text
path-scoped protected-surface scan over contract, comparison handoff, fixer
handoff, ingest module, and ingest tests
result: passed; forbidden 0; warnings 0
```

## Generated Artifact Status

Tests use in-memory SQLite connections. No SQLite database, journal, WAL, SHM,
raw log, failed-post, runtime status, generated data, or workbook export
artifacts were intentionally created.

## Forbidden Scope Status

No forbidden scope was intentionally touched. This is a local analytics ingest
validation fix only.

## Remaining Review Focus

- Confirm fractional integer inputs fail instead of truncating.
- Confirm negative parser-owned counts fail before partial facts remain.
- Confirm optional empty numeric fields still remain unavailable rather than
  becoming zero.

## Still Unverified

- GitHub Actions.
- PR diff after staging/submission.
- Clean installed-wheel import.
- Deferred gameplay action, opponent observation, and field-evidence ingest.
- Live workbook and deployed Apps Script state.
- Production behavior.

## Next Recommended Role

Codex E: Module Reviewer / confirmation thread.

```yaml
workflow_handoff:
  role_performed: "Codex D: Module Fixer"
  completed_thread: "D"
  next_thread: "E"
  next_role: "Codex E: Module Reviewer / confirmation thread"
  branch: "codex/analytics-foundation"
  contract_artifact: "docs/contracts/analytics_parser_normalized_replay_ingest.md"
  implementation_handoff: "docs/implementation_handoffs/analytics_parser_normalized_replay_ingest_comparison.md"
  fixer_handoff: "docs/implementation_handoffs/analytics_parser_normalized_replay_ingest_fixer.md"
  findings_fixed:
    - "P1: _optional_int() no longer truncates fractional numeric values."
    - "P2: parser-owned integer counts now reject negative values."
  validation:
    - "py -m pytest -q tests\\test_analytics_parser_normalized_replay_ingest.py tests\\test_analytics_schema.py tests\\test_analytics_migration_loader.py -> 51 passed"
    - "py -m pytest -q tests\\test_app_models.py tests\\test_golden_replay_harness.py -> 29 passed"
    - "py -m pytest -q tests\\test_gameplay_actions.py tests\\test_opponent_card_observations.py -> 26 passed"
    - "py -m ruff check src tests tools -> passed"
    - "git diff --check -> passed"
    - "py tools\\check_agent_docs.py -> passed"
    - "path-scoped secret/private-marker scan -> warning, forbidden 0, warning 1 on existing contract wording"
    - "path-scoped protected-surface scan -> passed"
  forbidden_scope_touched: false
```
