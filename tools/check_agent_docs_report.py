"""Report renderers for the agent docs consistency checker."""

from __future__ import annotations

import json
from dataclasses import asdict

try:
    from tools.check_agent_docs_contract import SEVERITY_ERROR
    from tools.check_agent_docs_models import CheckResult
except ModuleNotFoundError:
    from check_agent_docs_contract import SEVERITY_ERROR
    from check_agent_docs_models import CheckResult


def render_report(result: CheckResult) -> str:
    lines = [
        "Agent Docs Consistency Check",
        f"mode: {result.mode}",
        f"checked_files: {len(result.checked_files)}",
        f"errors: {len(result.errors)}",
        f"warnings: {len(result.warnings)}",
        "",
    ]
    if result.error:
        lines.append(f"ERROR configuration {result.error}")
    else:
        for finding in result.findings:
            label = "ERROR" if finding.severity == SEVERITY_ERROR else "WARNING"
            lines.append(
                f"{label} {finding.category_id} {finding.path} - {finding.reason}",
            )
    if lines[-1] != "":
        lines.append("")
    lines.append(f"result: {result.result}")
    return "\n".join(lines)


def render_json(result: CheckResult) -> str:
    return json.dumps(
        {
            "mode": result.mode,
            "checked_files": list(result.checked_files),
            "errors": len(result.errors),
            "warnings": len(result.warnings),
            "findings": [asdict(finding) for finding in result.findings],
            "error": result.error,
            "result": result.result,
        },
        indent=2,
        sort_keys=True,
    )
