"""CLI wrapper for the Player.log evidence-ledger schema drift report builder."""

# ruff: noqa: E402, I001

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"

if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from mythic_edge_parser.app.evidence_schema_drift_report import main


if __name__ == "__main__":
    raise SystemExit(main())
