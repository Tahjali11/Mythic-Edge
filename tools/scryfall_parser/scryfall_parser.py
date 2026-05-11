"""Thin wrapper around the integrated Mythic Edge card catalog sync."""

# ruff: noqa: E402, I001

import sys
from pathlib import Path


TOOLS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = TOOLS_DIR.parent.parent
SRC_ROOT = PROJECT_ROOT / "src"

if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from mythic_edge_parser.app.card_catalog import main


if __name__ == "__main__":
    raise SystemExit(main())
