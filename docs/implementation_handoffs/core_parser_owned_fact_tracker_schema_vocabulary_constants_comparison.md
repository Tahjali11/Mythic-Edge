# Parser-Owned Fact Tracker Schema Vocabulary Constants Comparison

## Issue

<https://github.com/Tahjali11/Mythic-Edge/issues/725>

## Contract

`docs/contracts/core_parser_owned_fact_tracker_decomposition_decision_packet.md`

Reviewed base commit: `d8e8a5c834bda3312a13cb149008435d8c435ea1`.

## Role Performed

Codex C: Module Implementer.

## Implementation Comparison

Before this slice, immutable parser-owned fact tracker schema and vocabulary
constants were defined alongside builders, validators, lifecycle rules, and
privacy helpers in `parser_owned_fact_tracker.py`.

This slice moves only immutable source-reference, object/schema, default,
ordered vocabulary, false-flag/non-claim, and required-field tuple constants
into `parser_owned_fact_tracker_schema.py`. The existing
`parser_owned_fact_tracker.py` module explicitly imports and re-exports those
same objects, so its public path and constant identities remain available.

The following deliberately remain in the original facade:

- mutable lifecycle and reference mappings;
- `ParserOwnedFactTrackerError`;
- every builder and validator;
- privacy/no-echo regex patterns and safe-key allowlist;
- lifecycle, platform-confirmation, report-summary, and copy-safe logic.

No parser or downstream behavior, schema value, vocabulary ordering, false
flag, non-claim, error category, function signature, or parser-truth ownership
changed.

## Files Changed

- `src/mythic_edge_parser/app/parser_owned_fact_tracker.py`
- `src/mythic_edge_parser/app/parser_owned_fact_tracker_schema.py`
- `tests/test_parser_owned_fact_tracker.py`
- `docs/implementation_handoffs/core_parser_owned_fact_tracker_schema_vocabulary_constants_comparison.md`

## Tests Added Or Updated

The focused tracker test now verifies that every moved constant is the same
object when reached through the existing facade and the new support module. It
also verifies that mutable transition mappings and privacy/no-echo state were
not relocated.

## Behavior-Preservation Evidence

The reviewed base and implementation produced identical SHA-256 values for:

- moved constant values and ordering:
  `449a403d14ae8e9ca6dcb18dabdf16a521824e6b834f99a571555511a1eb8f66`;
- default matrix, ledger, and coverage-report outputs:
  `9892ebf632b3d65a26279a3fd42b0a20a9423c251a869fbf512e6cd462c9e81b`;
- public builder and validator signatures:
  `31462702e453cf16d1a8f7f5b0327a82362075f62ae98f9b63527602abf20d2f`.

AST comparison also confirmed that every class/function definition and every
excluded mutable/privacy assignment is identical to the reviewed base.

## Validation Run

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest -q tests/test_parser_owned_fact_tracker.py
13 passed

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m pytest -q tests/test_parser_owned_fact_tracker.py tests/test_field_recovery_matrix.py
24 passed

PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q
2084 passed

python3 -m ruff check src tests tools
passed

PYTHONDONTWRITEBYTECODE=1 python3 -m compileall -q src/mythic_edge_parser/app/parser_owned_fact_tracker.py src/mythic_edge_parser/app/parser_owned_fact_tracker_schema.py
passed

python3 tools/check_agent_docs.py
passed: 0 errors, 0 warnings

path-scoped secret/private marker scan
passed: 4 paths, 0 forbidden, 0 warnings

path-scoped protected-surface gate
passed: 4 paths, 0 forbidden, 0 warnings

path-scoped validation selector
passed: selection_status ok; all required commands satisfied

python3 tools/run_pyright_advisory_report.py
advisory: 412 findings, identical to the reviewed-base count and rule breakdown

git diff --check
passed

public-interface smoke check
passed

before/after constant, output, signature, and AST comparisons
passed
```

## Governance Outcome

- Public-safe/no-echo boundary: unchanged; privacy helpers and patterns remain
  in the facade and focused tests pass.
- Vocabulary and schema coherence: unchanged; deterministic baseline hashes
  match exactly.
- Authority semantics: all readiness and authorization flags remain false in
  generated objects.
- Parser-truth boundary: unchanged; this remains metadata-only tracker support.
- Protected surfaces: no downstream, CI, raw-log, or parser behavior surface
  was changed.

## Remaining Risk

Review should confirm the explicit facade re-exports are the preferred local
style and that the constants-only boundary remains visually clear. Private
logs, live MTGA behavior, workbook/webhook/App Script behavior, and production
behavior were neither needed nor inspected. Pyright remains advisory with 412
pre-existing findings; the reviewed base and implementation reports are
identical by finding count and rule category.

## Recommended Next Role

Codex E: review the constants-only extraction against issue #725, the decision
packet, this handoff, and the focused identity/baseline evidence.

## Pasteable Codex E Prompt

```text
Use the Mythic Edge workflow rules.

Act as Codex E: Module Reviewer for Mythic-Edge issue #725.

Repository:
Tahjali11/Mythic-Edge

Issue:
https://github.com/Tahjali11/Mythic-Edge/issues/725

Contract:
docs/contracts/core_parser_owned_fact_tracker_decomposition_decision_packet.md

Implementation handoff:
docs/implementation_handoffs/core_parser_owned_fact_tracker_schema_vocabulary_constants_comparison.md

Review only the behavior-preserving first slice
extract_schema_vocabulary_constants. Verify that parser_owned_fact_tracker.py
remains the public facade; moved values, ordering, reachability, and object
identity are preserved; mutable transition/reference mappings and privacy
regex/allowlist state remain in the facade; builders, validators, errors,
lifecycle logic, schemas, false-authority flags, non-claims, output shapes, and
parser-truth ownership are unchanged; and tests cover the preservation claim.

Lead with findings ordered by severity. Do not edit files, run ARS/Refactor
Scout, inspect private evidence, change parser/downstream/CI behavior, or make
readiness, parser-truth, security, or privacy claims. Route to Codex D only for
concrete implementation findings; otherwise route to Codex F.
```

```yaml
instruction_context:
  required_for_risk_tier: "medium_or_high"
  deferred_for_low_risk: false
  role: "C"
  risk_tier: "High"
  global_router_read: true
  repo_agents_read: true
  repo_rules_read: true
  repo_constitution_read: true
  repo_workflow_read: true
  role_doc_read: true
  issue_or_tracker_read: true
  contract_or_handoff_read: true
  accepted_adrs_read: []
  protected_surfaces:
    - "parser truth ownership"
    - "parser-owned fact schema and vocabulary"
    - "privacy and no-echo validation"
    - "false-authority and non-claim fields"
    - "public module facade"
  authority_conflicts_found: false
  authority_conflict_notes: ""
  stop_conditions:
    - "Stop on target drift or any behavior-preservation mismatch."
    - "Stop before moving builders, validators, mutable lifecycle state, or privacy helpers."
    - "Stop before parser/downstream/CI changes or private evidence access."
    - "Stop before readiness, parser-truth, security, or privacy claims."
```

```yaml
workflow_handoff:
  repository: "Tahjali11/Mythic-Edge"
  repository_url: "https://github.com/Tahjali11/Mythic-Edge"
  issue: "https://github.com/Tahjali11/Mythic-Edge/issues/725"
  tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/568"
  related_decomposition_tracker: "https://github.com/Tahjali11/Mythic-Edge/issues/463"
  source_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/722"
  source_review_issue: "https://github.com/Tahjali11/Mythic-Edge/issues/724"
  completed_thread: "C"
  next_thread: "E"
  verdict: "parser_owned_fact_tracker_constants_only_extraction_ready_for_review"
  source_artifact: "docs/contracts/core_parser_owned_fact_tracker_decomposition_decision_packet.md"
  target_artifact: "docs/implementation_handoffs/core_parser_owned_fact_tracker_schema_vocabulary_constants_comparison.md"
  reviewed_base_commit: "d8e8a5c834bda3312a13cb149008435d8c435ea1"
  branch: "codex/parser-owned-fact-tracker-schema-vocabulary-725"
  risk_tier: "High"
  implementation_scope: "extract_schema_vocabulary_constants"
  parser_behavior_change_authorized: false
  parser_truth_ownership_change_authorized: false
  downstream_behavior_change_authorized: false
  ci_change_authorized: false
  ars_run_authorized: false
  refactor_scout_run_authorized: false
  private_evidence_read_authorized: false
  readiness_claimed: false
  parser_truth_claimed: false
  security_assurance_claimed: false
  privacy_assurance_claimed: false
```
