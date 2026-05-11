from __future__ import annotations

import sys

from ..sanitize import scrub_raw_log


def main() -> int:
    raw = sys.stdin.read()
    sys.stdout.write(scrub_raw_log(raw))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
