from __future__ import annotations

import argparse
from pathlib import Path

from mythic_edge_parser.app.grp_id_candidates import (
    build_grp_id_candidate_report,
    confirm_candidate_suggestion,
    defer_candidate_suggestion,
    load_grp_id_candidate_report,
    promote_auto_suggestions_with_details,
)


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Rank likely card-name candidates for unresolved MTGA grpIds using the current decklist."
    )
    parser.add_argument(
        "--decklist",
        default="",
        help="Optional path to a saved current-deck JSON file. Defaults to the project current deck.",
    )
    parser.add_argument("--format", default="arena", help="Card lookup format to use. Default: arena.")
    parser.add_argument(
        "--promote-singletons",
        action="store_true",
        help="Write singleton high-confidence auto-suggestions into the grpId override file.",
    )
    parser.add_argument(
        "--confirm-grp-id",
        type=int,
        default=0,
        help="Manually confirm the current suggested candidate for one grpId from the latest scored report.",
    )
    parser.add_argument(
        "--defer-grp-id",
        type=int,
        default=0,
        help="Defer the current suggested candidate for one grpId from the latest scored report.",
    )
    parser.add_argument(
        "--hand-confirmations",
        default="",
        help="Optional path to a hand-confirmations JSON file. Defaults to the project hand tracker.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)

    needs_fresh_scoring = bool(args.promote_singletons or not (args.confirm_grp_id or args.defer_grp_id))
    if needs_fresh_scoring:
        report = build_grp_id_candidate_report(
            decklist_path=Path(args.decklist) if args.decklist.strip() else None,
            hand_confirmation_path=Path(args.hand_confirmations) if args.hand_confirmations.strip() else None,
            format_key=args.format.strip().lower() or "arena",
        )
    else:
        report = load_grp_id_candidate_report()
    if args.confirm_grp_id:
        promoted = confirm_candidate_suggestion(report, grp_id=int(args.confirm_grp_id))
        print(
            f"Confirmed: grpId {promoted.grp_id} -> {promoted.name} "
            f"[{promoted.section}] evidence={promoted.evidence_match_percent}% score={promoted.score}"
        )
    if args.defer_grp_id:
        deferred = defer_candidate_suggestion(report, grp_id=int(args.defer_grp_id))
        print(
            f"Deferred: grpId {deferred.grp_id} -> {deferred.name} "
            f"[{deferred.section}] evidence={deferred.evidence_match_percent}%"
        )
    if args.promote_singletons:
        promoted = promote_auto_suggestions_with_details(report)
        print(f"Promoted overrides: {len(promoted)}")
        if promoted:
            for row in promoted:
                print(
                    f"Promoted: grpId {row.grp_id} -> {row.name} "
                    f"[{row.section}] evidence={row.evidence_match_percent}% score={row.score}"
                )
        else:
            print("Promoted: none")
    print(report.summary_line())
    if report.report_path is not None:
        print(f"Report: {report.report_path}")
    if report.markdown_report_path is not None:
        print(f"Readable report: {report.markdown_report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
