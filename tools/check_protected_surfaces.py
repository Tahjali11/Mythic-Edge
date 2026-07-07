"""Path-based protected-surface diff gate for Mythic Edge."""

from __future__ import annotations

import subprocess
import sys

try:
    from tools.check_protected_surfaces_classification import (
        _is_documented_fixture,
        _is_token_credential_filename,
        _matches_pattern,
        _matches_rule,
        classify_path,
        classify_paths,
        evaluate_paths,
        normalize_path,
    )
    from tools.check_protected_surfaces_io import (
        build_parser,
        collect_changed_paths,
        main,
        run_gate,
    )
    from tools.check_protected_surfaces_models import (
        FORBIDDEN_RULES,
        PROTECTED_RULES,
        SEVERITY_ALLOWED,
        SEVERITY_FORBIDDEN,
        SEVERITY_WARNING,
        Classification,
        GateResult,
        Rule,
    )
    from tools.check_protected_surfaces_report import render_report
except ModuleNotFoundError:  # pragma: no cover - used when run from tools/.
    from check_protected_surfaces_classification import (
        _is_documented_fixture,
        _is_token_credential_filename,
        _matches_pattern,
        _matches_rule,
        classify_path,
        classify_paths,
        evaluate_paths,
        normalize_path,
    )
    from check_protected_surfaces_io import (
        build_parser,
        collect_changed_paths,
        main,
        run_gate,
    )
    from check_protected_surfaces_models import (
        FORBIDDEN_RULES,
        PROTECTED_RULES,
        SEVERITY_ALLOWED,
        SEVERITY_FORBIDDEN,
        SEVERITY_WARNING,
        Classification,
        GateResult,
        Rule,
    )
    from check_protected_surfaces_report import render_report

__all__ = (
    "FORBIDDEN_RULES",
    "PROTECTED_RULES",
    "SEVERITY_ALLOWED",
    "SEVERITY_FORBIDDEN",
    "SEVERITY_WARNING",
    "Classification",
    "GateResult",
    "Rule",
    "_is_documented_fixture",
    "_is_token_credential_filename",
    "_matches_pattern",
    "_matches_rule",
    "build_parser",
    "classify_path",
    "classify_paths",
    "collect_changed_paths",
    "evaluate_paths",
    "main",
    "normalize_path",
    "render_report",
    "run_gate",
    "subprocess",
    "sys",
)


if __name__ == "__main__":
    raise SystemExit(main())
