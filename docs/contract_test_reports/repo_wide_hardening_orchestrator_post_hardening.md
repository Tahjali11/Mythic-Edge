Hardening Orchestrator
schema_version: 1
profile: post-hardening
run_mode: run
base: origin/main
orchestrator_status: warning
merge_readiness: not_decided_by_orchestrator
deploy_readiness: not_decided_by_orchestrator
tracker_completion: not_decided_by_orchestrator

## Commands
- protected_surface_gate | priority=required | status=passed | exit_code=0 | source=tools/check_protected_surfaces.py | command=python3 tools/check_protected_surfaces.py --base origin/main | summary=Protected Surface Gate | base: origin/main | head: HEAD
- secret_private_marker_scan | priority=required | status=warning | exit_code=0 | source=tools/check_secret_patterns.py | command=python3 tools/check_secret_patterns.py --base origin/main | summary=Secret / Private Marker Scan | mode: changed-files | base: origin/main
- validation_selector | priority=required | status=passed | exit_code=0 | source=tools/select_validation.py | command=python3 tools/select_validation.py --base origin/main | summary=Validation Selector | mode: changed-files | base: origin/main
- surface_authorization | priority=recommended | status=skipped | exit_code=<not_executed> | source=tools/check_surface_authorization.py | command=python3 tools/check_surface_authorization.py --base origin/main | summary=authorization_files_not_supplied
- agent_docs_checker | priority=required | status=passed | exit_code=0 | source=tools/check_agent_docs.py | command=python3 tools/check_agent_docs.py | summary=Agent Docs Consistency Check | mode: repo | checked_files: 29
- diff_check | priority=required | status=passed | exit_code=0 | source=git diff --check | command=git diff --check | summary=<no output>
- full_pytest | priority=required | status=passed | exit_code=0 | source=pytest | command=python3 -m pytest -q tests | summary=........................................................................ [  9%] | ........................................................................ [ 18%] | ........................................................................ ...
- ruff | priority=required | status=passed | exit_code=0 | source=ruff | command=python3 -m ruff check src tests tools | summary=All checks passed!
- pyright_advisory | priority=advisory | status=passed | exit_code=0 | source=tools/run_pyright_advisory_report.py | command=python3 tools/run_pyright_advisory_report.py | summary=Pyright Advisory Report | mode: advisory | project: pyrightconfig.json
- hardening_report_generator | priority=required | status=passed | exit_code=0 | source=tools/generate_hardening_report.py | command=python3 tools/generate_hardening_report.py --output docs/contract_test_reports/repo_wide_hardening_status_report.md | summary=# Repo-Wide Hardening Status Report | report_kind: repo_wide_hardening_status | schema_version: 1

## Skipped Commands
- surface_authorization: authorization_files_not_supplied

## Warnings And Advisory Results
- secret_private_marker_scan: warning - Secret / Private Marker Scan | mode: changed-files | base: origin/main

## Missing Or Not Configured
- surface_authorization: skipped - authorization_files_not_supplied

## Summary
- The orchestrator reports command planning and local execution results only.
- It does not decide validation truth, merge readiness, deploy readiness, or tracker completion.
- Overall status: warning

## Workflow Handoff
- Next role depends on the surrounding issue workflow; this output is not a PR, merge, or deploy verdict.