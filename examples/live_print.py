import asyncio
import os
from pathlib import Path

from mythic_edge_parser import MtgaEventStream
from mythic_edge_parser.app.config import DEFAULT_MTGA_PLAYER_LOG


async def main():
    stream, subscriber = await MtgaEventStream.start(
        Path(os.environ.get("MTGA_PLAYER_LOG", str(DEFAULT_MTGA_PLAYER_LOG)))
    )
    try:
        while True:
            event = await subscriber.recv()
            if event is None:
                break
            print(event.kind, event.payload)
    finally:
        await stream.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
