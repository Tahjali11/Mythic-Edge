from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))


from mythic_edge_parser.app.hand_confirmations import main_sync


if __name__ == "__main__":
    json_path, markdown_path = main_sync()
    print(f"Hand confirmation file: {json_path}")
    print(f"Readable tracker: {markdown_path}")
