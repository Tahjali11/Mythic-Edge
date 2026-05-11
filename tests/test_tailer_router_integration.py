import asyncio
from pathlib import Path

import pytest

from mythic_edge_parser.log.tailer import FileTailer
from mythic_edge_parser.router import Router

FIXTURE = Path(__file__).resolve().parent / "fixtures" / "router_smoke_slice.log"


@pytest.mark.integration
@pytest.mark.smoke
def test_tailer_entry_router_smoke_fixture_produces_expected_event_kinds(tmp_path: Path) -> None:
    log_path = tmp_path / "Player.log"
    fixture_lines = [
        line
        for line in FIXTURE.read_text(encoding="utf-8").splitlines()
        if not line.startswith("#")
    ]
    log_path.write_text("\n".join(fixture_lines) + "\n", encoding="utf-8")

    async def run() -> None:
        tailer = await FileTailer.open_from_start(log_path, poll_interval_seconds=0)
        batch = await tailer.poll_once()
        router = Router()
        kinds: list[str] = []

        for entry in batch.entries:
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

    asyncio.run(run())
