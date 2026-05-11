"""User-facing entrypoint for refreshing tier buckets from meta websites."""

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mythic_edge_parser.app.tier_sync import sync_tier_sources


if __name__ == "__main__":
    result = sync_tier_sources(post_to_webhook=True)
    print(result.summary_line())
