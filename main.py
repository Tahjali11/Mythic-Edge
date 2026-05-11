"""User-facing entrypoint for the Mythic Edge parser."""

# ruff: noqa: E402, I001
import asyncio
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mythic_edge_parser.app.runner import main as run_parser


if __name__ == "__main__":
    asyncio.run(run_parser())
