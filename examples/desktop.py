"""
FastMCP Desktop Example

A simple example that exposes the desktop directory as a resource.
"""

import asyncio
from pathlib import Path

from fastmcp.server import FastMCP

# Create server
mcp = FastMCP("desktop")


@mcp.resource("desktop")
def desktop() -> list[str]:
    """List the files in the desktop directory"""
    desktop = Path.home() / "Desktop"
    return [str(f) for f in desktop.iterdir()]


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


if __name__ == "__main__":
    asyncio.run(FastMCP.run_stdio(mcp))
