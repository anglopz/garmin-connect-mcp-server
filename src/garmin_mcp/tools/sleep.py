"""Sleep tools for Garmin Connect MCP server."""

from garmin_mcp.client import get_client
from garmin_mcp.server import mcp


@mcp.tool()
async def get_sleep_data(date: str) -> dict:
    """Get structured sleep data for a specific date including sleep score, stages, and times.

    Use this when the user asks about their sleep quality, sleep score, how long they slept,
    sleep stages (deep, light, REM), or when they went to bed and woke up.

    Returns sleep score, bed time, wake time, total duration, and time in each sleep stage
    (deep, light, REM, awake).

    Args:
        date: Date in YYYY-MM-DD format (the morning after the sleep night)
    """
    try:
        client = await get_client()
        return await client.get_sleep_data(date)
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def get_sleep_data_raw(date: str) -> dict:
    """Get the full raw sleep payload for a specific date including heart rate and SpO2 data.

    Use this when the user wants detailed sleep tracking data, heart rate during sleep,
    blood oxygen levels during sleep, or the complete sleep session data.

    Args:
        date: Date in YYYY-MM-DD format (the morning after the sleep night)
    """
    try:
        client = await get_client()
        return await client.get_sleep_data_raw(date)
    except Exception as e:
        return {"error": str(e)}
