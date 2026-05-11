from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))


from mythic_edge_parser.app.arena_id_validation import refresh_grp_id_overrides_from_logs


if __name__ == "__main__":
    result = refresh_grp_id_overrides_from_logs(format_key="arena")
    print(result.summary_line())
    print(f"Override file: {result.override_file_path}")
    if result.fingerprint_report_path is not None:
        print(f"Fingerprint report: {result.fingerprint_report_path}")
    if result.fingerprint_markdown_path is not None:
        print(f"Fingerprint markdown: {result.fingerprint_markdown_path}")
