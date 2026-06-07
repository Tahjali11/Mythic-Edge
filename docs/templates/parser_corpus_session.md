# Parser Corpus Session Template

Use this template for planning or reviewing a parser corpus session. Keep it
metadata-only. Do not paste source log lines, payload objects, private paths,
account identifiers, opponent identifiers, credentials, decklists, generated
runtime artifacts, failed delivery artifacts, workbook exports, or local
database files.

## Session Metadata

- session_id:
- title:
- source_kind:
- commit_status:
- privacy_class:
- format_family:
- match_shape:
- linked_issue:
- authorized_by_contract:

## Scenario Families

- scenario_family:
- coverage_status:
- coverage_basis:

## Parser Coverage Summary

- parser_event_families:
- parser_claim_families:
- unknown_entries:
- truncation_count:
- degradation_labels:

## Game Rows

- count:
- result_shape:
- expected_blank_fields:

## Known Gaps

- gap:
- recommended_next_step:
- blocked_by:

## Redaction Checklist

- raw_log_lines_included: false
- raw_payloads_included: false
- private_paths_included: false
- private_identifiers_included: false
- deck_contents_included: false
- local_artifacts_included: false

## Reviewer Notes

- notes:

## Boundary Statement

This session record is corpus planning metadata. It does not decide parser
truth, merge readiness, deploy readiness, tracker completion, gameplay advice,
analytics truth, workbook truth, or AI truth.
