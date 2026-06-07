# Parser Corpus Parity Expansion Implementation Comparison

## Metadata

- issue: https://github.com/Tahjali11/Mythic-Edge/issues/291
- tracker: https://github.com/Tahjali11/Mythic-Edge/issues/158
- source_artifact: docs/contracts/parser_corpus_parity_expansion.md
- target_artifact: docs/implementation_handoffs/parser_corpus_parity_expansion_comparison.md
- branch: codex/parser-corpus-parity-expansion
- base_commit: 9cb5f5b9805f530edad827378d14bf3b373b526d
- risk_tier: High
- role: Codex C / Module Implementer
- implementation_status: ready_for_review

## Codex D Fixer Addendum

CPC-E-001 is fixed pending Codex E confirmation. Codex D added
checker-verifiable category-specific authorization evidence for the protected
`workflow_authority_docs` surface at
`docs/templates/parser_corpus_session.md`.

Protected-surface authorization: Authorized drift - workflow_authority_docs -
docs/templates/parser_corpus_session.md - issue #291 and
docs/contracts/parser_corpus_parity_expansion.md.

Codex D validation:

- `python3 -m pytest -q tests/test_corpus_parity_report.py` -> `7 passed`
- `python3 -m pytest -q tests` -> `1697 passed`
- `python3 -m ruff check src tests tools` -> passed
- `python3 tools/check_agent_docs.py` -> passed
- untracked package whitespace scan -> passed
- package-scoped secret/private-marker scan -> passed, `forbidden: 0`,
  `warnings: 0`
- package-scoped protected-surface gate -> passed, `forbidden: 0`,
  `warnings: 1`
- protected-surface authorization checker -> `authorization_status: ok`,
  `authorized: 1`, `missing_authorization: 0`

## Findings

No parser behavior, parser state, event classes, workbook/webhook/App Script
surfaces, analytics truth, AI behavior, local app behavior, Match Journal
behavior, SQLite behavior, runtime status schema, generated artifacts, raw logs,
  or private evidence were changed.

One implementation detail needed tightening during focused tests: the report
privacy detector originally treated the required session-ledger redaction flag
name as forbidden content. The detector now distinguishes explicit raw payload
fields from the required false-valued redaction checklist.

The contract validation command that pipes `git diff --name-only
origin/main...HEAD` into hardening tools sees zero paths while the Codex C files
remain untracked and unstaged. An explicit changed-file path list was run in
addition to the literal command so the new files were actually scanned.

## Confirmed Matches

- Added a metadata/report-only corpus parity builder at
  `src/mythic_edge_parser/app/corpus_parity_report.py`.
- Added committed corpus metadata at
  `tests/fixtures/parser_corpus/corpus_manifest.v1.json`.
- Added committed session-ledger metadata at
  `tests/fixtures/parser_corpus/session_ledger.v1.json`.
- Added a human reviewer session template at
  `docs/templates/parser_corpus_session.md`.
- Added focused tests at `tests/test_corpus_parity_report.py`.
- The report builder uses explicit inputs only and does not read private logs,
  fetch external corpora, clone repositories, call model providers, or inspect
  generated runtime artifacts.
- The manifest covers the contracted scenario-family taxonomy and maps current
  safe Mythic Edge evidence to committed, synthetic, partial, missing, and
  external-boundary coverage states.
- The report preserves category-level coverage only. It does not claim parser
  correctness, semantic equivalence to external corpora, merge readiness,
  deploy readiness, tracker completion, analytics truth, workbook truth, AI
  truth, gameplay advice, hidden-card inference, archetype labels, or
  player-mistake labels.
- Privacy checks reject private source flags, unsafe local paths, forbidden
  artifact path suffixes, external log artifact paths, raw payload markers, and
  secret-style assignments. Report strings redact local absolute paths and
  secret-style assignments before returning output.
- Protected-surface booleans in the report are summary-only and all false.

## Contract Mismatches Fixed

- Missing corpus parity implementation module: fixed.
- Missing machine-readable corpus manifest fixture: fixed.
- Missing machine-readable session ledger fixture: fixed.
- Missing session review template: fixed.
- Missing compatibility report schema builder and CLI entrypoint: fixed.
- Missing focused validation for taxonomy, report vocabulary, privacy blocking,
  external-boundary blocking, CLI output, and no-parser-truth claims: fixed.

## Still Open

- Most scenario families remain missing, partial, or external-boundary blocked
  because the contract explicitly scoped V1 to metadata/report scaffolding, not
  new parser fixtures.
- No private Player.log report-only evidence was added. That remains
  approval-gated and outside this implementation.
- External Manasight material remains category reference only. No external
  logs, manifests, sessions, hashes, compressed artifacts, or parser source
  were copied.
- The report is not wired into golden replay, diagnostics, feature-equity,
  analytics, local app UI, CI, workbook export, webhook delivery, Apps Script,
  Match Journal, overlay, SQLite, or Google Sheets.

## Files Changed

- `src/mythic_edge_parser/app/corpus_parity_report.py`
- `tests/test_corpus_parity_report.py`
- `tests/fixtures/parser_corpus/corpus_manifest.v1.json`
- `tests/fixtures/parser_corpus/session_ledger.v1.json`
- `docs/templates/parser_corpus_session.md`
- `docs/implementation_handoffs/parser_corpus_parity_expansion_comparison.md`

Existing untracked contract from Codex B remains present:

- `docs/contracts/parser_corpus_parity_expansion.md`

Protected-surface authorization: Authorized drift - workflow_authority_docs -
docs/templates/parser_corpus_session.md - issue #291 and
docs/contracts/parser_corpus_parity_expansion.md.

## Tests Added

- Manifest and session-ledger validation for object/schema/taxonomy coverage.
- Compatibility report mapping for committed, synthetic, partial, missing, and
  external-boundary states.
- Private metadata blocker that proves local paths are not echoed.
- External artifact path blocker for external-reference boundary enforcement.
- Session-ledger redaction flag validation.
- CLI behavior for explicit output and required manifest input.

## Validation Run

- `python3 -m pytest -q tests/test_corpus_parity_report.py`
  - passed: 7 passed
- `python3 -m pytest -q tests/test_golden_replay_harness.py tests/test_feature_equity_corpus_ratchet.py`
  - passed: 20 passed
- `python3 -m pytest -q tests`
  - passed: 1697 passed
- `python3 -m ruff check src tests tools`
  - passed
- `python3 tools/check_agent_docs.py`
  - passed
- `git diff --name-only origin/main...HEAD | python3 tools/check_secret_patterns.py --base origin/main --paths-from-stdin`
  - passed with scanned_paths: 0 because implementation files are untracked
- `git diff --name-only origin/main...HEAD | python3 tools/check_protected_surfaces.py --base origin/main --paths-from-stdin`
  - passed with changed_paths: 0 because implementation files are untracked
- `git diff --name-only origin/main...HEAD | python3 tools/select_validation.py --base origin/main --paths-from-stdin`
  - selection_status: ok, advisory zero_changed_paths

- explicit changed-file secret/private marker scan:
  - passed: scanned_paths: 7, forbidden: 0, warnings: 0
- explicit changed-file protected-surface gate:
  - passed: changed_paths: 7, forbidden: 0, warnings: 1
  - warning: `docs/templates/parser_corpus_session.md` is a protected workflow
    authority surface; the contract authorizes this template.
- explicit changed-file validation selector:
  - selection_status: warning
  - required checks included focused corpus test, Ruff, agent docs checker,
    diff check, secret/private marker scan, and protected-surface gate.
  - recommended checks included full pytest and protected-surface
    authorization review.
  - advisory check: Pyright advisory report.
- `git diff --check`
  - passed with no output. Note: implementation files are untracked/unstaged,
    so this literal command does not inspect their content until they are added
    to a tracked diff.

## Residual Risks

- The manifest is intentionally coverage metadata, so a green report cannot be
  interpreted as parser correctness or fixture sufficiency.
- Future fixture expansion still needs separate contracts for each missing or
  private-report-only scenario family.
- External reference categories may drift over time; this module stores only a
  small Mythic Edge taxonomy and does not mirror an external corpus.
- The current implementation is not integrated into CI or downstream reports.
  That is intentional for this contract.

## Next Recommended Role

Codex E / Module Reviewer.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge agent constitution.
Use $mythic-edge-workflow.

Act as Codex E: Module Reviewer for issue #291, parser corpus parity expansion.

Review branch:
codex/parser-corpus-parity-expansion

Source contract:
docs/contracts/parser_corpus_parity_expansion.md

Implementation handoff:
docs/implementation_handoffs/parser_corpus_parity_expansion_comparison.md

Focus:
- Confirm the implementation remains metadata/report-only.
- Confirm no parser behavior, parser state, event class, workbook, webhook,
  Apps Script, runtime status, analytics, AI, Match Journal, SQLite, local app,
  or generated/private artifact behavior changed.
- Review src/mythic_edge_parser/app/corpus_parity_report.py.
- Review tests/test_corpus_parity_report.py.
- Review tests/fixtures/parser_corpus/corpus_manifest.v1.json.
- Review tests/fixtures/parser_corpus/session_ledger.v1.json.
- Review docs/templates/parser_corpus_session.md.
- Confirm external corpus material remains category reference only and no
  external logs, session rows, hashes, compressed files, or parser source were
  copied.
- Confirm report statuses and residual risks do not overclaim parser
  correctness, release readiness, merge readiness, tracker completion,
  analytics truth, workbook truth, or AI truth.

Validation to review or rerun:
- python3 -m pytest -q tests/test_corpus_parity_report.py
- python3 -m pytest -q tests/test_golden_replay_harness.py tests/test_feature_equity_corpus_ratchet.py
- python3 -m ruff check src tests tools
- python3 tools/check_agent_docs.py
- path-scoped secret/private marker scan for changed files
- path-scoped protected-surface gate for changed files
- path-scoped validation selector for changed files
- git diff --check

Do not:
- Target main directly.
- Add parser behavior changes or protected-surface changes.
- Import Manasight logs/source or raw/private Player.log content.
- Commit generated/private/runtime artifacts.
- Mark tracker #158 complete.
```

## workflow_handoff

```yaml
workflow_handoff:
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/291"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/158"
  completed_thread: "C"
  next_thread: "E"
  source_artifact: "docs/contracts/parser_corpus_parity_expansion.md"
  target_artifact: "docs/implementation_handoffs/parser_corpus_parity_expansion_comparison.md"
  verdict: "implementation_ready_for_module_review"
  risk_tier: "High"
  branch: "codex/parser-corpus-parity-expansion"
  base_commit: "9cb5f5b9805f530edad827378d14bf3b373b526d"
  validation:
    - "python3 -m pytest -q tests/test_corpus_parity_report.py"
    - "python3 -m pytest -q tests/test_golden_replay_harness.py tests/test_feature_equity_corpus_ratchet.py"
    - "python3 -m pytest -q tests"
    - "python3 -m ruff check src tests tools"
    - "python3 tools/check_agent_docs.py"
    - "explicit changed-file secret/private marker scan for changed files"
    - "explicit changed-file protected-surface gate for changed files"
    - "explicit changed-file validation selector for changed files"
    - "git diff --check"
  stop_conditions:
    - "Do not target main directly."
    - "Do not close tracker #158."
    - "Do not change parser behavior, parser state final reconciliation, parser event classes, router semantics, workbook schema, webhook payload shape, Apps Script behavior, output transport, runtime status schema, Match Journal behavior, overlay behavior, SQLite behavior, Google Sheets behavior, analytics truth, AI truth, OpenAI/model-provider behavior, CI gates, merge policy, deploy policy, match/game identity, deduplication, secrets, environment variables, raw logs, generated data, runtime status files, failed delivery artifacts, workbook exports, or production behavior."
    - "Do not import, copy, mirror, or commit external corpus logs, compressed files, raw session rows, hashes, parser source, private Player.log excerpts, local diagnostics artifacts, local runtime artifacts, API keys, tokens, credentials, webhook URLs, or generated data."
    - "Do not let corpus coverage become parser truth, merge readiness, deploy readiness, public-release readiness, tracker completion, gameplay advice, hidden-card inference, archetype classification, player-mistake labeling, analytics truth, workbook truth, or AI truth."
```
