#!/usr/bin/env bash
set -euo pipefail

# Launch the MCP Inspector for interactive debugging of the Garmin Connect MCP server.
exec uv run mcp dev src/garmin_mcp/server.py
