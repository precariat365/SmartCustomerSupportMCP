import asyncio

from . import mcp_server


def main():
    """Main entry point for the package."""
    print("start ……")
    asyncio.run(mcp_server.main())


__all__ = ["main", "mcp_server"]
