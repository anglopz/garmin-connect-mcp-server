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

# Phase 1: Tool modules will be imported here to register with the server
# from garmin_mcp.tools import activities  # noqa: F401
# from garmin_mcp.tools import health  # noqa: F401
# from garmin_mcp.tools import training  # noqa: F401
# from garmin_mcp.tools import trends  # noqa: F401
# from garmin_mcp.tools import analysis  # noqa: F401
# from garmin_mcp.tools import body  # noqa: F401
# from garmin_mcp.tools import sleep  # noqa: F401
# from garmin_mcp.tools import profile  # noqa: F401

# Phase 1: Resource modules
# from garmin_mcp.resources import athlete  # noqa: F401
# from garmin_mcp.resources import readiness  # noqa: F401
# from garmin_mcp.resources import daily  # noqa: F401

# Phase 1: Prompt modules
# from garmin_mcp.prompts import training_analysis  # noqa: F401
# from garmin_mcp.prompts import sleep_report  # noqa: F401
# from garmin_mcp.prompts import readiness_check  # noqa: F401
# from garmin_mcp.prompts import health_summary  # noqa: F401


def main():
    """Run the Garmin Connect MCP server via stdio transport."""
    logger.info("Starting Garmin Connect MCP server")
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
