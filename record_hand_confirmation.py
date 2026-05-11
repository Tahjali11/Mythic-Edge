from __future__ import annotations

import argparse
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))


from mythic_edge_parser.app.hand_confirmations import HAND_WINDOW_LABELS, main_record


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Record a manual opening-hand or mulligan-hand card confirmation for later grpId matching."
    )
    parser.add_argument("card_name", help="Exact card name you saw in hand.")
    parser.add_argument(
        "--hand-window",
        default="opening_hand",
        choices=sorted(HAND_WINDOW_LABELS),
        help="Which hand window this card was seen in.",
    )
    parser.add_argument("--match-id", default="", help="Optional MTGA match ID hint.")
    parser.add_argument("--game", type=int, default=None, help="Game number, if known.")
    parser.add_argument("--date", default="", help="Match date hint in YYYY-MM-DD format.")
    parser.add_argument("--time", default="", help="Match time hint in HH:MM or HH:MM:SS format.")
    parser.add_argument("--opponent", default="", help="Optional opponent archetype hint.")
    parser.add_argument("--note", default="", help="Optional free-text note.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)

    entry, json_path, markdown_path = main_record(
        card_name=args.card_name,
        hand_window=args.hand_window,
        match_id_hint=args.match_id,
        game_number=args.game,
        match_date_hint=args.date,
        match_time_hint=args.time,
        opponent_archetype=args.opponent,
        note=args.note,
    )

    print(f"Recorded confirmation: {entry['card_name']}")
    print(f"Hand window: {entry['hand_window']}")
    print(f"Confirmation ID: {entry['confirmation_id']}")
    print(f"Section hint: {entry['section_hint']}")
    print(f"Hand confirmation file: {json_path}")
    print(f"Readable tracker: {markdown_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
