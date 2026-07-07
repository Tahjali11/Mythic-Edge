"""Report rendering for the protected-surface gate."""

from __future__ import annotations

try:
    from tools.check_protected_surfaces_models import GateResult
except ModuleNotFoundError:  # pragma: no cover - script-local import fallback.
    from check_protected_surfaces_models import GateResult


def render_report(result: GateResult) -> str:
    lines = [
        "Protected Surface Gate",
        f"base: {result.base}",
        f"head: {result.head}",
        f"changed_paths: {len(result.changed_paths)}",
        f"forbidden: {len(result.forbidden)}",
        f"warnings: {len(result.warnings)}",
        "",
    ]
    if result.error:
        lines.append(f"ERROR configuration {result.error}")
    else:
        for item in result.forbidden:
            lines.append(f"FORBIDDEN {item.category_id} {item.path} - {item.reason}")
        for item in result.warnings:
            lines.append(f"WARNING {item.category_id} {item.path} - {item.reason}")

    if lines[-1] != "":
        lines.append("")
    if result.error:
        lines.append("result: error")
    elif result.forbidden:
        lines.append("result: failed")
    else:
        lines.append("result: passed")
    return "\n".join(lines)
