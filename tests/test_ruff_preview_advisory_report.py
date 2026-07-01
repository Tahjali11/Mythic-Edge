from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "generate_ruff_preview_advisory_report.py"
sys.path.insert(0, str(MODULE_PATH.parent))
SPEC = importlib.util.spec_from_file_location("generate_ruff_preview_advisory_report", MODULE_PATH)
assert SPEC is not None
preview_reporter = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = preview_reporter
assert SPEC.loader is not None
SPEC.loader.exec_module(preview_reporter)


def _finding(code: str, filename: str = "tools/example.py") -> dict:
    return {
        "code": code,
        "filename": filename,
        "message": "Synthetic advisory finding.",
        "location": {"row": 1, "column": 1},
    }


def _rule(code: str, *, preview: bool, linter: str = "synthetic") -> dict:
    return {
        "code": code,
        "name": f"synthetic-{code.lower()}",
        "linter": linter,
        "summary": "Synthetic rule metadata.",
        "preview": preview,
    }


def _write_checkout_markers(checkout: Path) -> None:
    checkout.mkdir(parents=True, exist_ok=True)
    (checkout / "pyproject.toml").write_text("[tool.ruff]\n", encoding="utf-8")
    (checkout / "AGENTS.md").write_text("# Synthetic checkout\n", encoding="utf-8")
    (checkout / ".git").write_text("gitdir: synthetic\n", encoding="utf-8")


def test_preview_report_uses_preview_specific_schema_and_non_claims(tmp_path: Path) -> None:
    checkout = tmp_path / "checkout"
    _write_checkout_markers(checkout)

    report = preview_reporter.build_preview_report(
            [
                _finding("LOG004", "tools/logging_case.py"),
                _finding("S101", "tests/test_example.py"),
                _finding("D103", "src/mythic_edge_parser/app/state.py"),
            ],
        rule_metadata={
            "LOG004": _rule("LOG004", preview=True, linter="flake8-logging"),
            "S101": _rule("S101", preview=False, linter="flake8-bandit"),
            "D103": _rule("D103", preview=False, linter="pydocstyle"),
        },
        measured_checkout_root=checkout,
    )

    by_code = {item["rule_code"]: item for item in report["rule_summaries"]}
    rendered = preview_reporter.render_json(report)

    assert report["object"] == "mythic_edge_quality_ruff_preview_advisory_report"
    assert report["schema_version"] == "quality_ruff_preview_advisory_report.v1"
    assert report["preview_enabled_for_measurement"] is True
    assert report["preview_enabled_in_pyproject"] is False
    assert report["preview_enabled_in_ci"] is False
    assert report["blocking_promotion_authorized"] is False
    assert report["autofix_authorized"] is False
    assert report["unsafe_fix_authorized"] is False
    assert report["totals"]["findings"] == 3
    assert report["totals"]["preview_only_rule_codes"] == 1
    assert report["totals"]["triggered_preview_only_rule_codes"] == 1
    assert report["totals"]["zero_baseline_preview_rule_codes"] == 0
    assert by_code["LOG004"]["primary_classification"] == "watch_list"
    assert by_code["LOG004"]["secondary_labels"] == ["logging_visibility", "preview_only"]
    assert by_code["S101"]["primary_classification"] == "watch_list"
    assert by_code["D103"]["primary_classification"] == "protected_surface_review_required"
    assert "not CI readiness" in report["non_claims"]
    assert "affected_paths" not in rendered
    assert str(checkout) not in rendered


def test_zero_baseline_preview_rules_defer_until_stable() -> None:
    report = preview_reporter.build_preview_report(
        [],
        rule_metadata={
            "LOG004": _rule("LOG004", preview=True, linter="flake8-logging"),
        },
    )

    summary = report["rule_summaries"][0]

    assert summary["rule_code"] == "LOG004"
    assert summary["count"] == 0
    assert summary["preview_only_rule"] is True
    assert summary["primary_classification"] == "defer_until_stable"
    assert report["log004_classification"]["primary_classification"] == "defer_until_stable"


def test_preview_report_summarizes_path_families_instead_of_raw_affected_paths(
    tmp_path: Path,
) -> None:
    checkout = tmp_path / "checkout"
    _write_checkout_markers(checkout)
    source_file = checkout / "src" / "mythic_edge_parser" / "local_app" / "example.py"
    source_file.parent.mkdir(parents=True)
    source_file.write_text("print('synthetic')\n", encoding="utf-8")

    report = preview_reporter.build_preview_report(
        [_finding("LOG004", str(source_file))],
        rule_metadata={"LOG004": _rule("LOG004", preview=True, linter="flake8-logging")},
        measured_checkout_root=checkout,
    )
    rendered = preview_reporter.render_json(report)

    summary = report["rule_summaries"][0]

    assert summary["affected_path_families"] == ["src"]
    assert "affected_paths" not in summary
    assert str(source_file) not in rendered
    assert str(checkout) not in rendered


def test_malformed_rule_metadata_fails_closed() -> None:
    with pytest.raises(
        preview_reporter.RuffPreviewAdvisoryError,
        match="measurement_blocked_malformed_rule_metadata",
    ):
        preview_reporter.load_rule_metadata('{"code": "LOG004"}')


def test_cli_outputs_preview_report_without_private_checkout_path(tmp_path: Path) -> None:
    checkout = tmp_path / "checkout"
    _write_checkout_markers(checkout)
    ruff_json = tmp_path / "ruff.json"
    metadata_json = tmp_path / "rules.json"
    source_file = checkout / "tools" / "example.py"
    source_file.parent.mkdir(parents=True)
    source_file.write_text("print('synthetic')\n", encoding="utf-8")
    ruff_json.write_text(json.dumps([_finding("LOG004", str(source_file))]), encoding="utf-8")
    metadata_json.write_text(json.dumps([_rule("LOG004", preview=True)]), encoding="utf-8")

    completed = subprocess.run(
        [
            sys.executable,
            str(MODULE_PATH),
            "--input",
            str(ruff_json),
            "--rule-metadata-input",
            str(metadata_json),
            "--branch-or-ref",
            "origin/main",
            "--commit",
            "abc123",
            "--ruff-version",
            "ruff 0.15.12",
            "--measured-checkout-root",
            str(checkout),
        ],
        check=True,
        text=True,
        capture_output=True,
    )

    report = json.loads(completed.stdout)

    assert report["object"] == "mythic_edge_quality_ruff_preview_advisory_report"
    assert report["branch_or_ref"] == "origin/main"
    assert report["commit"] == "abc123"
    assert str(source_file) not in completed.stdout
    assert str(checkout) not in completed.stdout
