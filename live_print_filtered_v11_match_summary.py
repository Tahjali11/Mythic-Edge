"""Legacy entrypoint that forwards to the current parser implementation."""

import asyncio

from main import run_parser


if __name__ == "__main__":
    asyncio.run(run_parser())
