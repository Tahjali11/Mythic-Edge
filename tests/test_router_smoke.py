from pathlib import Path

from mythic_edge_parser.log.entry import LineBuffer
from mythic_edge_parser.router import Router

FIXTURE = Path(__file__).resolve().parent / "fixtures" / "router_smoke_slice.log"


def test_router_smoke_fixture_covers_connection_and_deck_events() -> None:
    buffer = LineBuffer()
    router = Router()
    kinds: list[str] = []

    for line in FIXTURE.read_text(encoding="utf-8").splitlines():
        if line.startswith("#"):
            continue
        for entry in buffer.feed(f"{line}\n"):
            for event in router.route(entry):
                kinds.append(event.kind)
    for entry in buffer.flush():
        for event in router.route(entry):
            kinds.append(event.kind)

    assert kinds == [
        "DetailedLoggingStatus",
        "MatchConnectionState",
        "TcpConnectionClose",
        "ConnectionError",
        "ConnectionError",
        "Collection",
        "DeckCollection",
    ]
