from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import IO, Mapping, Sequence

from tools.dev_app import dev_app_launcher as launcher


def test_check_mode_is_dry_run_and_does_not_create_app_data(tmp_path) -> None:
    repo_root = _make_repo_root(tmp_path)
    app_root = tmp_path / "app-data"
    config = launcher.build_config(repo_root=repo_root, app_data_root=app_root)

    report = launcher.run_preflight(
        config,
        mode="check",
        tool_resolver=_tool_resolver,
        module_finder=_module_finder,
        platform_name="Windows",
    )

    assert not report.has_blockers
    assert not app_root.exists()
    assert any(entry.name == "app_data_config" and entry.status == "missing" for entry in report.entries)


def test_start_mode_creates_only_app_dirs_and_launcher_logs(tmp_path) -> None:
    repo_root = _make_repo_root(tmp_path)
    app_root = tmp_path / "app-data"
    recorder = ProcessRecorder()
    config = launcher.build_config(repo_root=repo_root, app_data_root=app_root, no_open=True)

    result = launcher.start_dev_app(
        config,
        tool_resolver=_tool_resolver,
        module_finder=_module_finder,
        platform_name="Windows",
        port_checker=lambda _host, _port: True,
        process_launcher=recorder.launch,
        browser_opener=lambda _url: False,
        run_id="run-001",
        wait_for_exit=False,
        settle_seconds=0,
    )
    launcher.cleanup_children(result.children)

    assert result.status == "running"
    assert {path.name for path in app_root.iterdir()} == set(launcher.REQUIRED_APP_SUBDIRS)
    assert (app_root / "logs" / "launcher" / "run-001" / "launcher.log").is_file()
    assert (app_root / "logs" / "launcher" / "run-001" / "backend.log").is_file()
    assert (app_root / "logs" / "launcher" / "run-001" / "frontend.log").is_file()
    assert not (app_root / "db" / "mythic_edge.sqlite3").exists()
    assert not (app_root / "db" / "match_journal.sqlite3").exists()


def test_start_mode_uses_expected_commands_and_process_local_frontend_env(tmp_path) -> None:
    repo_root = _make_repo_root(tmp_path)
    recorder = ProcessRecorder()
    config = launcher.build_config(repo_root=repo_root, app_data_root=tmp_path / "app-data", no_open=True)

    result = launcher.start_dev_app(
        config,
        tool_resolver=_tool_resolver,
        module_finder=_module_finder,
        platform_name="Windows",
        port_checker=lambda _host, _port: True,
        process_launcher=recorder.launch,
        browser_opener=lambda _url: False,
        run_id="run-002",
        wait_for_exit=False,
        settle_seconds=0,
    )
    launcher.cleanup_children(result.children)

    backend_command = recorder.calls[0].command
    backend_call = recorder.calls[0]
    frontend_call = recorder.calls[1]

    assert backend_command == [
        "py",
        "-m",
        "uvicorn",
        "mythic_edge_parser.local_app.backend:create_app",
        "--factory",
        "--host",
        "127.0.0.1",
        "--port",
        "8765",
    ]
    assert backend_call.env["MYTHIC_EDGE_LOCAL_APP_FRONTEND_ORIGIN"] == "http://127.0.0.1:5173"
    assert backend_call.env["MYTHIC_EDGE_LOCAL_APP_DATA_ROOT"] == str(config.app_data_root)
    assert frontend_call.command == [
        "npm.cmd",
        "--prefix",
        "frontend",
        "run",
        "dev",
        "--",
        "--host",
        "127.0.0.1",
        "--port",
        "5173",
    ]
    assert frontend_call.env["VITE_MYTHIC_EDGE_API_BASE_URL"] == "http://127.0.0.1:8765"


def test_port_conflict_reports_unavailable_without_launching_or_creating_logs(tmp_path) -> None:
    repo_root = _make_repo_root(tmp_path)
    app_root = tmp_path / "app-data"
    recorder = ProcessRecorder()
    config = launcher.build_config(repo_root=repo_root, app_data_root=app_root, no_open=True)

    result = launcher.start_dev_app(
        config,
        tool_resolver=_tool_resolver,
        module_finder=_module_finder,
        platform_name="Windows",
        port_checker=lambda _host, port: port != 8765,
        process_launcher=recorder.launch,
        browser_opener=lambda _url: False,
        run_id="run-003",
        wait_for_exit=False,
        settle_seconds=0,
    )

    assert result.status == "failed"
    assert not recorder.calls
    assert not app_root.exists()
    assert any(
        entry.name == "backend_port_available" and entry.status == "unavailable"
        for entry in result.report.entries
    )


def test_cleanup_only_touches_children_started_by_launcher() -> None:
    started = FakeProcess()
    unrelated = FakeProcess()

    launcher.cleanup_children([launcher.ManagedChild("backend", started)])

    assert started.terminated is True
    assert unrelated.terminated is False


def test_launcher_log_redacts_repo_and_app_data_paths(tmp_path) -> None:
    repo_root = _make_repo_root(tmp_path)
    app_root = tmp_path / "app-data"
    recorder = ProcessRecorder()
    config = launcher.build_config(repo_root=repo_root, app_data_root=app_root, no_open=True)

    result = launcher.start_dev_app(
        config,
        tool_resolver=_tool_resolver,
        module_finder=_module_finder,
        platform_name="Windows",
        port_checker=lambda _host, _port: True,
        process_launcher=recorder.launch,
        browser_opener=lambda _url: False,
        run_id="run-004",
        wait_for_exit=False,
        settle_seconds=0,
    )
    launcher.cleanup_children(result.children)

    launcher_log = (app_root / "logs" / "launcher" / "run-004" / "launcher.log").read_text(encoding="utf-8")

    assert str(repo_root) not in launcher_log
    assert str(app_root) not in launcher_log
    assert launcher.REPO_ROOT_LABEL in launcher_log
    assert launcher.APP_DATA_LABEL in launcher_log


def test_child_process_logs_redact_repo_app_data_and_home_paths(tmp_path) -> None:
    repo_root = _make_repo_root(tmp_path)
    app_root = tmp_path / "app-data"
    home_path = Path.home() / "private_launcher_marker"
    recorder = ProcessRecorder(
        child_outputs=(
            f"backend repo={repo_root} repo_posix={repo_root.as_posix()}\n".encode(),
            f"frontend app={app_root} app_posix={app_root.as_posix()} home={home_path}\n".encode(),
        ),
    )
    config = launcher.build_config(repo_root=repo_root, app_data_root=app_root, no_open=True)

    result = launcher.start_dev_app(
        config,
        tool_resolver=_tool_resolver,
        module_finder=_module_finder,
        platform_name="Windows",
        port_checker=lambda _host, _port: True,
        process_launcher=recorder.launch,
        browser_opener=lambda _url: False,
        run_id="run-004-child-logs",
        wait_for_exit=False,
        settle_seconds=0,
    )
    launcher.cleanup_children(result.children)

    log_dir = app_root / "logs" / "launcher" / "run-004-child-logs"
    backend_log = (log_dir / "backend.log").read_text(encoding="utf-8")
    frontend_log = (log_dir / "frontend.log").read_text(encoding="utf-8")

    assert str(repo_root) not in backend_log
    assert repo_root.as_posix() not in backend_log
    assert str(app_root) not in frontend_log
    assert app_root.as_posix() not in frontend_log
    assert str(home_path) not in frontend_log
    assert launcher.REPO_ROOT_LABEL in backend_log
    assert launcher.APP_DATA_LABEL in frontend_log
    assert "<home>" in frontend_log


def test_powershell_wrapper_is_thin_and_routes_to_python_helper() -> None:
    wrapper = Path("tools/dev_app/start_mythic_edge_dev_app.ps1").read_text(encoding="utf-8")

    assert "dev_app_launcher.py" in wrapper
    assert "-Check" in wrapper
    assert "-Start" in wrapper
    assert "git pull" not in wrapper.lower()
    assert "reset" not in wrapper.lower()


def test_root_cmd_shortcut_is_thin_and_routes_to_powershell_wrapper() -> None:
    shortcut = Path("Start Mythic Edge Dev App.cmd").read_text(encoding="utf-8")
    shortcut_lower = shortcut.lower()

    assert "tools\\dev_app\\start_mythic_edge_dev_app.ps1" in shortcut
    assert "-Start" in shortcut
    assert "git pull" not in shortcut_lower
    assert "reset" not in shortcut_lower
    assert "del " not in shortcut_lower
    assert "rmdir" not in shortcut_lower


def test_immediate_frontend_exit_cleans_up_started_backend(tmp_path) -> None:
    repo_root = _make_repo_root(tmp_path)
    recorder = ProcessRecorder(exit_on_call=2)
    config = launcher.build_config(repo_root=repo_root, app_data_root=tmp_path / "app-data", no_open=True)

    result = launcher.start_dev_app(
        config,
        tool_resolver=_tool_resolver,
        module_finder=_module_finder,
        platform_name="Windows",
        port_checker=lambda _host, _port: True,
        process_launcher=recorder.launch,
        browser_opener=lambda _url: False,
        run_id="run-005",
        wait_for_exit=False,
        settle_seconds=0,
    )

    assert result.status == "failed"
    assert result.children[0].process.terminated is True
    assert any(entry.name == "frontend_process" and entry.status == "failed" for entry in result.report.entries)


@dataclass(frozen=True, slots=True)
class ProcessCall:
    command: list[str]
    cwd: Path
    env: Mapping[str, str]


class ProcessRecorder:
    def __init__(
        self,
        *,
        exit_on_call: int | None = None,
        child_outputs: Sequence[bytes] = (),
    ) -> None:
        self.calls: list[ProcessCall] = []
        self.exit_on_call = exit_on_call
        self.child_outputs = tuple(child_outputs)

    def launch(self, command: Sequence[str], cwd: Path, env: Mapping[str, str], log_handle: IO[bytes]) -> "FakeProcess":
        output = self.child_outputs[len(self.calls)] if len(self.calls) < len(self.child_outputs) else b"started\n"
        log_handle.write(output)
        self.calls.append(ProcessCall(list(command), cwd, dict(env)))
        return FakeProcess(exited=len(self.calls) == self.exit_on_call)


class FakeProcess:
    def __init__(self, *, exited: bool = False) -> None:
        self.terminated = False
        self.killed = False
        self.waited = False
        self.exited = exited

    def poll(self) -> int | None:
        return 0 if self.exited or self.terminated or self.killed else None

    def terminate(self) -> None:
        self.terminated = True

    def wait(self, timeout: float | None = None) -> int:
        self.waited = True
        self.terminated = True
        return 0

    def kill(self) -> None:
        self.killed = True


def _make_repo_root(tmp_path) -> Path:
    repo_root = tmp_path / "repo"
    (repo_root / "src" / "mythic_edge_parser" / "local_app").mkdir(parents=True)
    (repo_root / "frontend").mkdir()
    (repo_root / "AGENTS.md").write_text("agent rules", encoding="utf-8")
    (repo_root / "pyproject.toml").write_text("[project]\nname = 'test'\n", encoding="utf-8")
    (repo_root / "src" / "mythic_edge_parser" / "local_app" / "backend.py").write_text("", encoding="utf-8")
    (repo_root / "frontend" / "package.json").write_text("{}", encoding="utf-8")
    (repo_root / "frontend" / "package-lock.json").write_text("{}", encoding="utf-8")
    return repo_root


def _tool_resolver(name: str) -> str | None:
    tools = {
        "py": "py",
        "node": "node",
        "npm": "npm",
        "npm.cmd": "npm.cmd",
        "git": "git",
    }
    return tools.get(name)


def _module_finder(name: str) -> object | None:
    return object() if name in {"mythic_edge_parser", "fastapi", "uvicorn"} else None
