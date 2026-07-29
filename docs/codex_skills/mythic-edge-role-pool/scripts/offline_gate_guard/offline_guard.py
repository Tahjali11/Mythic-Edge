"""Trusted-code regression guard for common accidental offline-test escapes.

This process-local hook is not a security or isolation boundary. Native calls,
retained originals, and mutation paths without a covered Python audit event can
bypass it. Run only reviewed, trusted Python validation code under this guard.
Untrusted code and live behavioral proofs require a separately verified,
OS-enforced read-only/no-network isolation boundary.
"""

from __future__ import annotations

import os
import socket
import subprocess
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence


ACTIVATION_VARIABLE = "MYTHIC_EDGE_OFFLINE_GATE"
WRITE_ROOTS_VARIABLE = "MYTHIC_EDGE_OFFLINE_WRITE_ROOTS"
GUARD_DIRECTORY_VARIABLE = "MYTHIC_EDGE_OFFLINE_GUARD_DIRECTORY"
BOUNDARY_CLASSIFICATION = (
    "trusted-code regression guard; not a security or isolation boundary"
)
_INSTALLED = False
_ORIGINAL_POPEN = subprocess.Popen
_ORIGINAL_SOCKET = socket.socket
_ACTIVE_GUARD_DIRECTORY: Path | None = None
_ACTIVE_WRITE_ROOTS_TEXT: str | None = None
_WRITE_FLAG_MASK = (
    os.O_WRONLY
    | os.O_RDWR
    | os.O_APPEND
    | os.O_CREAT
    | os.O_TRUNC
    | getattr(os, "O_TMPFILE", 0)
)


def _deny_network(*args: object, **kwargs: object) -> object:
    raise RuntimeError("offline gate prohibits network sockets")


class OfflineSocket(_ORIGINAL_SOCKET):
    """Remain subclassable for ssl/asyncio imports but deny construction."""

    def __new__(cls, *args: object, **kwargs: object) -> "OfflineSocket":
        raise RuntimeError("offline gate prohibits network sockets")


def _deny_process_escape(*args: object, **kwargs: object) -> object:
    raise RuntimeError("offline gate prohibits process escape")


def _canonical_roots(text: str) -> tuple[Path, ...]:
    roots: list[Path] = []
    for item in text.split(os.pathsep):
        if item:
            roots.append(Path(item).resolve(strict=False))
    if not roots:
        raise RuntimeError("offline gate requires at least one write root")
    return tuple(roots)


def _is_contained(path_value: object, roots: tuple[Path, ...]) -> bool:
    if isinstance(path_value, int):
        return False
    try:
        path = Path(os.fsdecode(path_value)).resolve(strict=False)
    except (OSError, RuntimeError, TypeError, ValueError):
        return False
    return any(path == root or path.is_relative_to(root) for root in roots)


def _write_audit_hook(roots: tuple[Path, ...]):
    single_path_events = {
        "os.remove",
        "os.rmdir",
        "os.mkdir",
        "os.chmod",
        "os.truncate",
        "os.unlink",
    }
    double_path_events = {"os.rename", "os.replace", "os.link", "os.symlink"}

    def audit(event: str, args: tuple[Any, ...]) -> None:
        if event == "open" and args:
            mode = args[1] if len(args) > 1 else None
            flags = args[2] if len(args) > 2 else 0
            write_intent = (
                isinstance(mode, str) and any(marker in mode for marker in "wax+")
            ) or (isinstance(flags, int) and bool(flags & _WRITE_FLAG_MASK))
            if write_intent and not _is_contained(args[0], roots):
                raise RuntimeError("offline gate prohibits writes outside OS temporary roots")
        elif event in single_path_events and args:
            if not _is_contained(args[0], roots):
                raise RuntimeError("offline gate prohibits filesystem mutation outside OS temporary roots")
        elif event in double_path_events and len(args) >= 2:
            if not _is_contained(args[0], roots) or not _is_contained(args[1], roots):
                raise RuntimeError("offline gate prohibits filesystem mutation outside OS temporary roots")

    return audit


def _guarded_environment(
    source: Mapping[str, str] | None,
    *,
    guard_directory: Path,
    write_roots_text: str,
) -> dict[str, str]:
    environment = dict(os.environ if source is None else source)
    existing_pythonpath = environment.get("PYTHONPATH")
    environment["PYTHONPATH"] = (
        str(guard_directory)
        if not existing_pythonpath
        else str(guard_directory) + os.pathsep + existing_pythonpath
    )
    environment[ACTIVATION_VARIABLE] = "1"
    environment[WRITE_ROOTS_VARIABLE] = write_roots_text
    environment[GUARD_DIRECTORY_VARIABLE] = str(guard_directory)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    return environment


class OfflinePopen(_ORIGINAL_POPEN):
    """Remain subclassable for asyncio while enforcing guarded Python only."""

    def __init__(self, *args: object, **kwargs: object) -> None:
        command = kwargs.get("args", args[0] if args else None)
        executable = command[0] if isinstance(command, (list, tuple)) and command else None
        try:
            allowed_python = (
                executable is not None
                and Path(str(executable)).resolve() == Path(sys.executable).resolve()
            )
        except (OSError, RuntimeError, ValueError):
            allowed_python = False
        if not allowed_python:
            raise RuntimeError(
                "offline gate prohibits subprocesses other than the guarded Python interpreter"
            )
        arguments: Sequence[object] = command if isinstance(command, (list, tuple)) else ()
        if any(str(item) in {"-E", "-I", "-S"} for item in arguments[1:]):
            raise RuntimeError("offline gate prohibits Python flags that disable its guard")
        if kwargs.get("shell") is True:
            raise RuntimeError("offline gate prohibits shell subprocesses")
        if _ACTIVE_GUARD_DIRECTORY is None or _ACTIVE_WRITE_ROOTS_TEXT is None:
            raise RuntimeError("offline gate subprocess policy is not initialized")
        kwargs["env"] = _guarded_environment(
            kwargs.get("env") if isinstance(kwargs.get("env"), Mapping) else None,
            guard_directory=_ACTIVE_GUARD_DIRECTORY,
            write_roots_text=_ACTIVE_WRITE_ROOTS_TEXT,
        )
        super().__init__(*args, **kwargs)


def install_offline_guard(*, guard_directory: Path, write_roots_text: str) -> None:
    """Install one irreversible guard for the lifetime of this interpreter."""

    global _ACTIVE_GUARD_DIRECTORY, _ACTIVE_WRITE_ROOTS_TEXT, _INSTALLED
    if _INSTALLED:
        return
    roots = _canonical_roots(write_roots_text)
    _ACTIVE_GUARD_DIRECTORY = guard_directory
    _ACTIVE_WRITE_ROOTS_TEXT = write_roots_text

    socket.socket = OfflineSocket  # type: ignore[assignment]
    socket.create_connection = _deny_network  # type: ignore[assignment]
    if hasattr(socket, "create_server"):
        socket.create_server = _deny_network  # type: ignore[assignment]
    if hasattr(socket, "socketpair"):
        socket.socketpair = _deny_network  # type: ignore[assignment]
    if hasattr(socket, "fromfd"):
        socket.fromfd = _deny_network  # type: ignore[assignment]
    subprocess.Popen = OfflinePopen  # type: ignore[assignment]
    os.system = _deny_process_escape  # type: ignore[assignment]
    os.popen = _deny_process_escape  # type: ignore[assignment]
    for name in (
        "execl",
        "execle",
        "execlp",
        "execlpe",
        "execv",
        "execve",
        "execvp",
        "execvpe",
        "spawnl",
        "spawnle",
        "spawnlp",
        "spawnlpe",
        "spawnv",
        "spawnve",
        "spawnvp",
        "spawnvpe",
    ):
        if hasattr(os, name):
            setattr(os, name, _deny_process_escape)
    sys.addaudithook(_write_audit_hook(roots))
    _INSTALLED = True


def install_from_environment() -> None:
    if os.environ.get(ACTIVATION_VARIABLE) != "1":
        return
    guard_directory = Path(os.environ[GUARD_DIRECTORY_VARIABLE]).resolve(strict=True)
    install_offline_guard(
        guard_directory=guard_directory,
        write_roots_text=os.environ[WRITE_ROOTS_VARIABLE],
    )
