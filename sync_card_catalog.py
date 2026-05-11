"""User-facing entrypoint for the full card-catalog refresh pipeline."""

# ruff: noqa: E402, I001

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mythic_edge_parser.app.card_catalog_refresh import main


if __name__ == "__main__":
    raise SystemExit(main())
