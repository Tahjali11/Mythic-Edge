from __future__ import annotations

import socket
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

GUARD_DIRECTORY = Path(__file__).resolve().parent / "offline_gate_guard"
sys.path.insert(0, str(GUARD_DIRECTORY))
from offline_guard import BOUNDARY_CLASSIFICATION, install_offline_guard  # noqa: E402


TEMP_ROOT = Path(tempfile.gettempdir()).resolve()


class OfflineGateGuardTests(unittest.TestCase):
    """Exercise common accidental paths; these are not adversarial escape tests."""

    @classmethod
    def setUpClass(cls) -> None:
        install_offline_guard(
            guard_directory=GUARD_DIRECTORY,
            write_roots_text=str(TEMP_ROOT),
        )

    def test_parent_network_and_unscoped_write_are_denied(self) -> None:
        with self.assertRaises(RuntimeError):
            socket.socket()
        prohibited = Path(__file__).resolve().parent / "offline-write-must-not-exist.tmp"
        with self.assertRaises(RuntimeError):
            prohibited.write_text("blocked", encoding="utf-8")
        self.assertFalse(prohibited.exists())

    def test_contract_identifies_guard_as_trusted_code_regression_only(self) -> None:
        self.assertEqual(
            BOUNDARY_CLASSIFICATION,
            "trusted-code regression guard; not a security or isolation boundary",
        )

    def test_os_temporary_write_is_allowed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "allowed.txt"
            path.write_text("offline fixture", encoding="utf-8")
            self.assertEqual(path.read_text(encoding="utf-8"), "offline fixture")

    def test_python_subprocess_inherits_network_and_write_guard(self) -> None:
        network = subprocess.run(
            [
                sys.executable,
                "-B",
                "-c",
                (
                    "import socket\n"
                    "try:\n socket.socket()\n"
                    "except RuntimeError:\n raise SystemExit(0)\n"
                    "raise SystemExit(1)\n"
                ),
            ],
            check=False,
            capture_output=True,
            timeout=30,
        )
        self.assertEqual(network.returncode, 0, network.stderr)

        prohibited = Path(__file__).resolve().parent / "child-write-must-not-exist.tmp"
        write = subprocess.run(
            [
                sys.executable,
                "-B",
                "-c",
                (
                    "from pathlib import Path\n"
                    f"path=Path({str(prohibited)!r})\n"
                    "try:\n path.write_text('blocked',encoding='utf-8')\n"
                    "except RuntimeError:\n raise SystemExit(0)\n"
                    "raise SystemExit(1)\n"
                ),
            ],
            check=False,
            capture_output=True,
            timeout=30,
        )
        self.assertEqual(write.returncode, 0, write.stderr)
        self.assertFalse(prohibited.exists())

    def test_process_escape_and_guard_disabling_flags_are_denied(self) -> None:
        with self.assertRaises(RuntimeError):
            subprocess.Popen(["cmd.exe", "/c", "exit", "0"])
        with self.assertRaises(RuntimeError):
            subprocess.Popen([sys.executable, "-I", "-c", "pass"])


if __name__ == "__main__":
    unittest.main()
