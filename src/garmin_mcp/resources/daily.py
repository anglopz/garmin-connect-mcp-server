"""Daily health resource — garmin://health/today."""

import json
from datetime import date

from garmin_mcp.client import get_client
from garmin_mcp.server import mcp


@mcp.resource("garmin://health/today")
async def daily_health() -> str:
    """Daily health summary including steps, sleep, and stress for today.

    Returns a combined snapshot of today's health data: daily summary,
    sleep data from last night, and stress levels throughout the day.
    """
    client = await get_client()
    today = date.today().isoformat()
    data: dict = {"date": today}

    try:
        data["daily_summary"] = await client.get_daily_summary(today)
    except Exception as e:
        data["daily_summary"] = {"error": str(e)}

    try:
        data["sleep"] = await client.get_sleep_data(today)
    except Exception as e:
        data["sleep"] = {"error": str(e)}

    try:
        data["stress"] = await client.get_stress(today)
    except Exception as e:
        data["stress"] = {"error": str(e)}

    return json.dumps(data, indent=2, default=str)
