from __future__ import annotations

# ruff: noqa: E402, I001

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mythic_edge_parser.app.log_drift_sensor import main


if __name__ == "__main__":
    raise SystemExit(main())
