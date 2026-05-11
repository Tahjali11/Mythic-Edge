from pathlib import Path
from mythic_edge_parser import MtgaEventStream
import asyncio

async def main():
    stream, subscriber = await MtgaEventStream.start(
        Path(r"C:\Users\Tahj Blow\AppData\LocalLow\Wizards Of The Coast\MTGA\Player.log")
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
