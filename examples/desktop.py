"""
FastMCP Desktop Example

A simple example that exposes the desktop directory as a resource.
"""

import asyncio
from pathlib import Path

from fastmcp.server import FastMCP

# Create server
app = FastMCP("desktop")

# Add desktop as a directory resource
desktop = Path.home() / "Desktop"
app.add_dir_resource(
    str(desktop),
    recursive=True,
    name="Desktop",
    description="Files on the desktop",
)


def main123():
    # Run the server
    asyncio.run(FastMCP.run_stdio(app))


if __name__ == "__main__":
    main123()
