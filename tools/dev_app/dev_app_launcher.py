from __future__ import annotations

import argparse
import importlib.util
import os
import platform
import shutil
import socket
import subprocess
import sys
import threading
import time
import webbrowser
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import IO, Any, cast

APP_DATA_LABEL = "<app_data>"
REPO_ROOT_LABEL = "<repo_root>"
BACKEND_HOST = "127.0.0.1"
FRONTEND_HOST = "127.0.0.1"
BACKEND_PORT = 8765
FRONTEND_PORT = 5173
LOCAL_APP_DIR_NAME = "MythicEdgeDev"
REQUIRED_APP_SUBDIRS = ("config", "db", "logs", "imports", "jobs", "diagnostics")
REQUIRED_REPO_MARKERS = (
    "AGENTS.md",
    "pyproject.toml",
    "src/mythic_edge_parser/local_app/backend.py",
    "frontend/package.json",
)
SETUP_COMMAND = 'py -m pip install -e ".[dev,app]"'
FRONTEND_INSTALL_COMMAND = "npm --prefix frontend ci"
ALLOWED_HOSTS = {"127.0.0.1", "localhost"}


@dataclass(frozen=True, slots=True)
class LauncherConfig:
    repo_root: Path
    app_data_root: Path | None
    backend_host: str = BACKEND_HOST
    backend_port: int = BACKEND_PORT
    frontend_host: str = FRONTEND_HOST
    frontend_port: int = FRONTEND_PORT
    no_open: bool = False
    log_to_console: bool = False


@dataclass(frozen=True, slots=True)
class StatusEntry:
    name: str
    status: str
    message: str
    blocking: bool = False


@dataclass(frozen=True, slots=True)
class PreflightReport:
    entries: tuple[StatusEntry, ...]

    @property
    def has_blockers(self) -> bool:
        return any(entry.blocking and entry.status in {"failed", "missing", "unavailable"} for entry in self.entries)


@dataclass(slots=True)
class ManagedChild:
    name: str
    process: Any
    log_handle: IO[bytes] | None = None


@dataclass(frozen=True, slots=True)
class StartResult:
    status: str
    report: PreflightReport
    log_dir: Path | None
    frontend_url: str | None
    children: tuple[ManagedChild, ...]


ToolResolver = Callable[[str], str | None]
ModuleFinder = Callable[[str], object | None]
PortChecker = Callable[[str, int], bool]
ProcessLauncher = Callable[[Sequence[str], Path, Mapping[str, str], IO[bytes]], Any]
BrowserOpener = Callable[[str], bool]


class RedactingBinaryLog:
    def __init__(self, handle: IO[bytes], redactor: Callable[[object], str]) -> None:
        self._handle = handle
        self._redactor = redactor

    def write(self, data: bytes) -> int:
        text = data.decode("utf-8", errors="replace")
        redacted = self._redactor(text).encode("utf-8", errors="replace")
        self._handle.write(redacted)
        self._handle.flush()
        return len(data)

    def flush(self) -> None:
        self._handle.flush()


def discover_repo_root(start: Path) -> Path | None:
    current = start.resolve()
    if current.is_file():
        current = current.parent
    for candidate in (current, *current.parents):
        if all((candidate / marker).exists() for marker in ("AGENTS.md", "pyproject.toml")):
            return candidate
    return None


def default_app_data_root(env: Mapping[str, str] = os.environ) -> Path | None:
    local_app_data = env.get("LOCALAPPDATA")
    if not local_app_data:
        return None
    return Path(local_app_data) / LOCAL_APP_DIR_NAME


def build_config(
    *,
    repo_root: Path | None = None,
    app_data_root: Path | None = None,
    backend_port: int = BACKEND_PORT,
    frontend_port: int = FRONTEND_PORT,
    backend_host: str = BACKEND_HOST,
    frontend_host: str = FRONTEND_HOST,
    no_open: bool = False,
    log_to_console: bool = False,
    env: Mapping[str, str] = os.environ,
) -> LauncherConfig:
    resolved_repo = repo_root or discover_repo_root(Path.cwd())
    if resolved_repo is None:
        resolved_repo = Path.cwd()
    return LauncherConfig(
        repo_root=resolved_repo.resolve(),
        app_data_root=(app_data_root if app_data_root is not None else default_app_data_root(env)),
        backend_host=backend_host,
        backend_port=backend_port,
        frontend_host=frontend_host,
        frontend_port=frontend_port,
        no_open=no_open,
        log_to_console=log_to_console,
    )


def run_preflight(
    config: LauncherConfig,
    *,
    mode: str,
    tool_resolver: ToolResolver = shutil.which,
    module_finder: ModuleFinder = importlib.util.find_spec,
    platform_name: str | None = None,
) -> PreflightReport:
    entries: list[StatusEntry] = []
    system_name = platform_name or platform.system()
    entries.append(
        StatusEntry(
            "windows_platform",
            "ok" if system_name == "Windows" else "failed",
            "Windows platform detected" if system_name == "Windows" else "Windows platform required",
            blocking=True,
        ),
    )

    missing_markers = [marker for marker in REQUIRED_REPO_MARKERS if not (config.repo_root / marker).exists()]
    marker_message = (
        "Existing checkout markers found"
        if not missing_markers
        else f"Missing repo markers: {', '.join(missing_markers)}"
    )
    entries.append(
        StatusEntry(
            "repo_root",
            "ok" if not missing_markers else "failed",
            marker_message,
            blocking=True,
        ),
    )

    entries.extend(_app_data_status(config, mode=mode))
    entries.extend(_toolchain_status(config, tool_resolver=tool_resolver, module_finder=module_finder))
    entries.extend(_port_option_status(config))
    return PreflightReport(tuple(entries))


def start_dev_app(
    config: LauncherConfig,
    *,
    tool_resolver: ToolResolver = shutil.which,
    module_finder: ModuleFinder = importlib.util.find_spec,
    platform_name: str | None = None,
    port_checker: PortChecker | None = None,
    process_launcher: ProcessLauncher | None = None,
    browser_opener: BrowserOpener = webbrowser.open,
    run_id: str | None = None,
    wait_for_exit: bool = True,
    settle_seconds: float = 0.5,
) -> StartResult:
    port_checker = port_checker or is_port_available
    process_launcher = process_launcher or launch_process
    report = run_preflight(
        config,
        mode="start",
        tool_resolver=tool_resolver,
        module_finder=module_finder,
        platform_name=platform_name,
    )
    if report.has_blockers:
        return StartResult("failed", report, None, None, ())

    port_entries = _start_port_status(config, port_checker)
    if any(entry.status == "unavailable" for entry in port_entries):
        combined = PreflightReport((*report.entries, *port_entries))
        return StartResult("failed", combined, None, None, ())

    log_dir = prepare_app_data(config, run_id=run_id)

    def redactor(value: object) -> str:
        return redact_text(value, repo_root=config.repo_root, app_data_root=config.app_data_root)

    _write_launcher_log(
        log_dir,
        ["starting Mythic Edge dev app", f"repo={config.repo_root}", f"app_data={log_dir}"],
        redactor,
    )

    children: list[ManagedChild] = []
    try:
        backend_log = (log_dir / "backend.log").open("ab")
        backend_log_writer = cast(IO[bytes], RedactingBinaryLog(backend_log, redactor))
        backend_child = ManagedChild(
            "backend",
            process_launcher(
                build_backend_command(config, tool_resolver),
                config.repo_root,
                _backend_env(config),
                backend_log_writer,
            ),
            backend_log,
        )
        children.append(backend_child)

        frontend_log = (log_dir / "frontend.log").open("ab")
        frontend_log_writer = cast(IO[bytes], RedactingBinaryLog(frontend_log, redactor))
        frontend_child = ManagedChild(
            "frontend",
            process_launcher(
                build_frontend_command(config, tool_resolver),
                config.repo_root,
                _frontend_env(config),
                frontend_log_writer,
            ),
            frontend_log,
        )
        children.append(frontend_child)

        frontend_url = f"http://{config.frontend_host}:{config.frontend_port}"
        early_exit = _first_exited_child(children, settle_seconds=settle_seconds)
        if early_exit is not None:
            _write_launcher_log(log_dir, [f"{early_exit.name} failed during startup"], redactor)
            cleanup_children(children)
            failed_report = PreflightReport(
                (
                    *report.entries,
                    *port_entries,
                    StatusEntry(
                        f"{early_exit.name}_process",
                        "failed",
                        f"{early_exit.name} exited during startup",
                        blocking=True,
                    ),
                ),
            )
            return StartResult("failed", failed_report, log_dir, None, tuple(children))

        if not config.no_open:
            try:
                opened = browser_opener(frontend_url)
            except Exception:
                opened = False
            if not opened:
                _write_launcher_log(log_dir, ["browser open warning"], redactor)

        if config.log_to_console:
            print(redactor(f"running frontend at {frontend_url}; logs at {log_dir}"))

        if wait_for_exit:
            _wait_for_children(children)

        return StartResult(
            "running",
            PreflightReport((*report.entries, *port_entries)),
            log_dir,
            frontend_url,
            tuple(children),
        )
    except Exception:
        cleanup_children(children)
        raise
    finally:
        if wait_for_exit:
            _close_child_logs(children)


def prepare_app_data(config: LauncherConfig, *, run_id: str | None = None) -> Path:
    if config.app_data_root is None:
        raise RuntimeError("app data root unavailable")
    for subdir in REQUIRED_APP_SUBDIRS:
        (config.app_data_root / subdir).mkdir(parents=True, exist_ok=True)
    launcher_root = config.app_data_root / "logs" / "launcher"
    launcher_root.mkdir(parents=True, exist_ok=True)
    safe_run_id = run_id or datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    log_dir = launcher_root / safe_run_id
    log_dir.mkdir(parents=True, exist_ok=False)
    (log_dir / "launcher.log").touch()
    return log_dir


def build_backend_command(config: LauncherConfig, tool_resolver: ToolResolver = shutil.which) -> list[str]:
    python_cmd = "py" if tool_resolver("py") else sys.executable
    return [
        python_cmd,
        "-m",
        "uvicorn",
        "mythic_edge_parser.local_app.backend:create_app",
        "--factory",
        "--host",
        config.backend_host,
        "--port",
        str(config.backend_port),
    ]


def build_frontend_command(config: LauncherConfig, tool_resolver: ToolResolver = shutil.which) -> list[str]:
    npm_cmd = tool_resolver("npm.cmd") or tool_resolver("npm") or "npm"
    return [
        npm_cmd,
        "--prefix",
        "frontend",
        "run",
        "dev",
        "--",
        "--host",
        config.frontend_host,
        "--port",
        str(config.frontend_port),
    ]


def is_port_available(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        probe.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            probe.bind((host, port))
        except OSError:
            return False
    return True


def launch_process(
    command: Sequence[str],
    cwd: Path,
    env: Mapping[str, str],
    log_handle: IO[bytes],
) -> subprocess.Popen[bytes]:
    process = subprocess.Popen(  # noqa: S603 - command is constructed from contract-owned constants and local tool paths.
        list(command),
        cwd=cwd,
        env=dict(env),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if process.stdout is not None:
        thread = threading.Thread(
            target=_copy_child_output,
            args=(process.stdout, log_handle),
            daemon=True,
        )
        thread.start()
        setattr(process, "_mythic_edge_log_thread", thread)
    return process


def cleanup_children(children: Sequence[ManagedChild], *, timeout_seconds: float = 5.0) -> None:
    for child in children:
        if _poll_process(child.process) is None:
            child.process.terminate()
    for child in children:
        if _poll_process(child.process) is None:
            try:
                child.process.wait(timeout=timeout_seconds)
            except Exception:
                child.process.kill()
    _close_child_logs(children)


def redact_text(value: object, *, repo_root: Path, app_data_root: Path | None) -> str:
    text = str(value)
    replacements = [(repo_root, REPO_ROOT_LABEL)]
    if app_data_root is not None:
        replacements.append((app_data_root, APP_DATA_LABEL))
    home = Path.home()
    replacements.append((home, "<home>"))
    for path, label in replacements:
        for candidate in {str(path), path.as_posix()}:
            if candidate:
                text = text.replace(candidate, label)
    return text


def format_report(report: PreflightReport, config: LauncherConfig) -> str:
    lines = ["Mythic Edge dev app preflight"]
    for entry in report.entries:
        lines.append(f"{entry.status}: {entry.name} - {entry.message}")
    redacted = [redact_text(line, repo_root=config.repo_root, app_data_root=config.app_data_root) for line in lines]
    return "\n".join(redacted)


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    config = build_config(
        repo_root=args.repo_root,
        app_data_root=args.app_data_root,
        backend_port=args.backend_port,
        frontend_port=args.frontend_port,
        no_open=args.no_open,
        log_to_console=args.log_to_console,
    )
    if args.command == "check":
        report = run_preflight(config, mode="check")
        print(format_report(report, config))
        return 1 if report.has_blockers else 0

    result = start_dev_app(config)
    print(format_report(result.report, config))
    if result.log_dir is not None:
        print(redact_text(f"logs: {result.log_dir}", repo_root=config.repo_root, app_data_root=config.app_data_root))
    if result.frontend_url is not None:
        print(f"frontend: {result.frontend_url}")
    return 0 if result.status == "running" else 1


def _app_data_status(config: LauncherConfig, *, mode: str) -> list[StatusEntry]:
    if config.app_data_root is None:
        return [
            StatusEntry(
                "app_data_root",
                "unavailable",
                "%LOCALAPPDATA% is unavailable; pass an app-data root override for tests",
                blocking=mode == "start",
            ),
        ]
    app_data_message = (
        f"{APP_DATA_LABEL} exists"
        if config.app_data_root.exists()
        else f"{APP_DATA_LABEL} will be created in start mode"
    )
    entries = [
        StatusEntry(
            "app_data_root",
            "ok" if config.app_data_root.exists() else "missing",
            app_data_message,
            blocking=False,
        ),
    ]
    for subdir in REQUIRED_APP_SUBDIRS:
        path = config.app_data_root / subdir
        entries.append(
            StatusEntry(
                f"app_data_{subdir}",
                "ok" if path.exists() else "missing",
                f"{APP_DATA_LABEL}\\{subdir} exists" if path.exists() else f"{APP_DATA_LABEL}\\{subdir} missing",
                blocking=False,
            ),
        )
    return entries


def _toolchain_status(
    config: LauncherConfig,
    *,
    tool_resolver: ToolResolver,
    module_finder: ModuleFinder,
) -> list[StatusEntry]:
    python_available = bool(tool_resolver("py") or sys.executable)
    entries = [
        StatusEntry("python", "ok" if python_available else "missing", "Python launcher or executable available", True),
        _module_status("mythic_edge_parser", module_finder, blocking=True, missing_hint=SETUP_COMMAND),
        _module_status("fastapi", module_finder, blocking=True, missing_hint=SETUP_COMMAND),
        _module_status("uvicorn", module_finder, blocking=True, missing_hint=SETUP_COMMAND),
        _tool_status("node", tool_resolver, blocking=True, missing_hint="Install Node.js LTS"),
        _tool_status("npm", tool_resolver, blocking=True, missing_hint=FRONTEND_INSTALL_COMMAND),
        _tool_status(
            "git",
            tool_resolver,
            blocking=False,
            missing_hint="Git is recommended for existing checkout status",
        ),
    ]
    package_lock = config.repo_root / "frontend" / "package-lock.json"
    entries.append(
        StatusEntry(
            "frontend_lockfile",
            "ok" if package_lock.exists() else "missing",
            "frontend package lockfile present" if package_lock.exists() else f"Run: {FRONTEND_INSTALL_COMMAND}",
            blocking=True,
        ),
    )
    return entries


def _module_status(name: str, module_finder: ModuleFinder, *, blocking: bool, missing_hint: str) -> StatusEntry:
    available = module_finder(name) is not None
    return StatusEntry(
        f"module_{name}",
        "ok" if available else "missing",
        f"{name} importable" if available else f"{name} missing. Run: {missing_hint}",
        blocking=blocking,
    )


def _tool_status(name: str, tool_resolver: ToolResolver, *, blocking: bool, missing_hint: str) -> StatusEntry:
    available = tool_resolver(name) is not None
    return StatusEntry(
        f"tool_{name}",
        "ok" if available else "missing",
        f"{name} available" if available else f"{name} missing. {missing_hint}",
        blocking=blocking,
    )


def _port_option_status(config: LauncherConfig) -> list[StatusEntry]:
    entries = []
    for name, host, port in (
        ("backend", config.backend_host, config.backend_port),
        ("frontend", config.frontend_host, config.frontend_port),
    ):
        valid = host in ALLOWED_HOSTS and 1 <= port <= 65535
        entries.append(
            StatusEntry(
                f"{name}_port_option",
                "ok" if valid else "failed",
                f"{host}:{port} accepted" if valid else f"{name} host/port must be loopback with a valid port",
                blocking=True,
            ),
        )
    return entries


def _start_port_status(config: LauncherConfig, port_checker: PortChecker) -> tuple[StatusEntry, ...]:
    entries = []
    for name, host, port in (
        ("backend", config.backend_host, config.backend_port),
        ("frontend", config.frontend_host, config.frontend_port),
    ):
        available = port_checker(host, port)
        entries.append(
            StatusEntry(
                f"{name}_port_available",
                "ok" if available else "unavailable",
                f"{host}:{port} available" if available else f"{host}:{port} unavailable; no process was killed",
                blocking=True,
            ),
        )
    return tuple(entries)


def _backend_env(config: LauncherConfig) -> dict[str, str]:
    env = dict(os.environ)
    src_path = str(config.repo_root / "src")
    existing_pythonpath = env.get("PYTHONPATH")
    env["PYTHONPATH"] = src_path if not existing_pythonpath else os.pathsep.join((src_path, existing_pythonpath))
    env["MYTHIC_EDGE_LOCAL_APP_FRONTEND_ORIGIN"] = f"http://{config.frontend_host}:{config.frontend_port}"
    return env


def _frontend_env(config: LauncherConfig) -> dict[str, str]:
    env = dict(os.environ)
    env["VITE_MYTHIC_EDGE_API_BASE_URL"] = f"http://{config.backend_host}:{config.backend_port}"
    return env


def _write_launcher_log(log_dir: Path, lines: Sequence[str], redactor: Callable[[object], str]) -> None:
    with (log_dir / "launcher.log").open("a", encoding="utf-8") as handle:
        for line in lines:
            handle.write(redactor(line))
            handle.write("\n")


def _wait_for_children(children: Sequence[ManagedChild]) -> None:
    try:
        while True:
            for child in children:
                if _poll_process(child.process) is not None:
                    cleanup_children([other for other in children if other is not child])
                    return
            time.sleep(0.5)
    except KeyboardInterrupt:
        cleanup_children(children)


def _first_exited_child(children: Sequence[ManagedChild], *, settle_seconds: float) -> ManagedChild | None:
    if settle_seconds > 0:
        time.sleep(settle_seconds)
    for child in children:
        if _poll_process(child.process) is not None:
            return child
    return None


def _poll_process(process: Any) -> int | None:
    poll = getattr(process, "poll", None)
    if callable(poll):
        return poll()
    return None


def _close_child_logs(children: Sequence[ManagedChild]) -> None:
    for child in children:
        thread = getattr(child.process, "_mythic_edge_log_thread", None)
        if isinstance(thread, threading.Thread):
            thread.join(timeout=1.0)
        if child.log_handle is not None and not child.log_handle.closed:
            child.log_handle.close()


def _copy_child_output(output: IO[bytes], log_handle: IO[bytes]) -> None:
    try:
        for chunk in iter(output.readline, b""):
            if chunk:
                log_handle.write(chunk)
                log_handle.flush()
    finally:
        output.close()


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Mythic Edge local developer app launcher")
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command in ("check", "start"):
        subparser = subparsers.add_parser(command)
        subparser.add_argument("--repo-root", type=Path)
        subparser.add_argument("--app-data-root", type=Path)
        subparser.add_argument("--backend-port", type=int, default=BACKEND_PORT)
        subparser.add_argument("--frontend-port", type=int, default=FRONTEND_PORT)
        subparser.add_argument("--no-open", action="store_true")
        subparser.add_argument("--log-to-console", action="store_true")
    return parser.parse_args(argv)


if __name__ == "__main__":
    raise SystemExit(main())
