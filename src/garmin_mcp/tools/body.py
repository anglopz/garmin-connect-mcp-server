"""Body composition tools for Garmin Connect MCP server."""

from garmin_mcp.client import get_client
from garmin_mcp.server import mcp


@mcp.tool()
async def get_body_composition(start_date: str, end_date: str) -> dict:
    """Get body composition data over a date range including weight, BMI, body fat, and muscle mass.

    Use this when the user asks about their body composition, weight trends, BMI, body fat
    percentage, or muscle mass over a period of time.

    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
    """
    try:
        client = await get_client()
        return await client.get_body_composition(start_date, end_date)
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def get_latest_weight() -> dict:
    """Get the most recent weight entry from the last 30 days.

    Use this when the user asks about their current weight, latest weigh-in,
    or most recent body composition measurement.
    """
    try:
        client = await get_client()
        return await client.get_latest_weight()
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def get_daily_weigh_ins(date: str) -> dict:
    """Get all weigh-in records for a specific date.

    Use this when the user asks how many times they weighed themselves on a given day
    or wants all weigh-in entries for a specific date.

    Args:
        date: Date in YYYY-MM-DD format
    """
    try:
        client = await get_client()
        return await client.get_daily_weigh_ins(date)
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def get_weigh_ins(start_date: str, end_date: str) -> dict:
    """Get weigh-in records over a date range.

    Use this when the user asks about their weigh-in history, weight log,
    or wants to see weight entries over a period of time.

    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
    """
    try:
        client = await get_client()
        return await client.get_weigh_ins(start_date, end_date)
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def get_blood_pressure(start_date: str, end_date: str) -> dict:
    """Get blood pressure readings over a date range.

    Use this when the user asks about their blood pressure, systolic/diastolic readings,
    or cardiovascular health measurements over a period of time.

    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
    """
    try:
        client = await get_client()
        return await client.get_blood_pressure(start_date, end_date)
    except Exception as e:
        return {"error": str(e)}
