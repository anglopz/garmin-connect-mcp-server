"""FastMCP server for Garmin Connect data.

This is the main entry point. It creates the MCP server instance and imports
all tool, resource, and prompt modules to register them.
"""

import logging
import sys

from mcp.server.fastmcp import FastMCP

# Configure logging to stderr (stdout is reserved for MCP stdio transport)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stderr,
)

logger = logging.getLogger("garmin_mcp")

mcp = FastMCP("Garmin Connect")

# Tool modules — importing registers them with the server
from garmin_mcp.prompts import (  # noqa: E402
    health_summary,  # noqa: F401
    readiness_check,  # noqa: F401
    sleep_report,  # noqa: F401
    training_analysis,  # noqa: F401
)
from garmin_mcp.resources import (  # noqa: E402
    athlete,  # noqa: F401
    daily,  # noqa: F401
    readiness,  # noqa: F401
)
from garmin_mcp.tools import (  # noqa: E402
    activities,  # noqa: F401
    analysis,  # noqa: F401
    body,  # noqa: F401
    health,  # noqa: F401
    profile,  # noqa: F401
    sleep,  # noqa: F401
    training,  # noqa: F401
    trends,  # noqa: F401
)


def main():
    """Run the Garmin Connect MCP server via stdio transport."""
    logger.info("Starting Garmin Connect MCP server")
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
