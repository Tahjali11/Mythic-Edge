from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "run_pyright_advisory_report.py"
SPEC = importlib.util.spec_from_file_location("run_pyright_advisory_report", MODULE_PATH)
assert SPEC is not None
reporter = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = reporter
assert SPEC.loader is not None
SPEC.loader.exec_module(reporter)


def test_clean_pyright_output_renders_stable_advisory_fields() -> None:
    python_executable = Path.home() / "example" / "python.exe"
    report = reporter.build_report(
        project="pyrightconfig.json",
        repo_root=".",
        python_executable=python_executable,
        pyright_version="1.1.409",
        pyright_exit_code=0,
        output="0 errors, 0 warnings, 0 informations",
        platform_name="win32",
    )

    rendered = reporter.render_text(report)

    assert "Pyright Advisory Report" in rendered
    assert "mode: advisory" in rendered
    assert "project: pyrightconfig.json" in rendered
    assert "python: <resolved-python>" in rendered
    assert "platform: windows" in rendered
    assert "command: pyright --project pyrightconfig.json --pythonpath <python>" in rendered
    assert "status: clean" in rendered
    assert "gate_behavior: advisory_non_blocking" in rendered
    assert str(Path.home()) not in rendered


def test_local_resolver_noise_is_classified_without_type_findings() -> None:
    raw_output = "\n".join(
        [
            "repo/tests/test_api_common.py",
            (
                '  repo/tests/test_api_common.py:3:8 - error: Import "pytest" could not be resolved '
                "(reportMissingImports)"
            ),
            "1 error, 0 warnings, 0 informations",
            "Python was not found; run without arguments to install from the Microsoft Store",
        ],
    )

    report = reporter.build_report(
        project="pyrightconfig.json",
        repo_root=".",
        python_executable=Path.home() / ".pyenv" / "shims" / "python3",
        pyright_version="1.1.409",
        pyright_exit_code=1,
        output=raw_output,
        platform_name="darwin",
    )

    assert report.status == "local_resolver_noise"
    assert report.type_findings == 0
    assert report.local_resolver_noise >= 1
    assert report.helper_exit_code == 0


def test_type_findings_are_advisory_not_blocking() -> None:
    output = "\n".join(
        [
            "src/example.py",
            '  src/example.py:1:1 - error: Argument of type "str" cannot be assigned (reportArgumentType)',
            "1 error, 0 warnings, 0 informations",
        ],
    )

    report = reporter.build_report(
        project="pyrightconfig.json",
        repo_root=".",
        python_executable="/usr/bin/python3",
        pyright_version="1.1.409",
        pyright_exit_code=1,
        output=output,
        platform_name="linux",
    )

    assert report.status == "advisory_findings"
    assert report.type_findings == 1
    assert report.local_resolver_noise == 0
    assert report.helper_exit_code == 0
    assert "Type Findings:" in reporter.render_text(report)


def test_tooling_config_blocker_exits_two_and_redacts_reason() -> None:
    private_config_path = Path.home() / "repo" / "pyrightconfig.json"
    private_python_path = Path.home() / "python.exe"
    report = reporter.build_tooling_blocker_report(
        project="pyrightconfig.json",
        repo_root=".",
        reason=f"{private_config_path} could not be read",
        python_executable=private_python_path,
        platform_name="win32",
    )

    rendered = reporter.render_text(report)

    assert report.status == "tooling_config_blocker"
    assert report.tooling_config_blockers == 1
    assert report.helper_exit_code == 2
    assert "Tooling / Config Blockers:" in rendered
    assert str(Path.home()) not in rendered


def test_json_report_exposes_summary_and_classification_blocks() -> None:
    report = reporter.build_report(
        project="pyrightconfig.json",
        repo_root=".",
        python_executable="/usr/bin/python3",
        pyright_version="1.1.409",
        pyright_exit_code=0,
        output="0 errors, 0 warnings, 0 informations",
        platform_name="linux",
    )

    rendered = reporter.render_json(report)

    assert '"object": "mythic_edge_pyright_advisory_report"' in rendered
    assert '"summary": {' in rendered
    assert '"classification": {' in rendered
