"""Health tools for Garmin Connect MCP server.

Exposes 14 health and wellness tools covering daily summary, steps, heart rate,
stress, body battery, respiration, SpO2, intensity minutes, floors, hydration,
and daily events.
"""

from garmin_mcp.client import get_client
from garmin_mcp.server import mcp


@mcp.tool()
async def get_daily_summary(date: str) -> dict:
    """Get a full daily wellness summary including steps, calories, distance, HR, stress, and body battery.

    Use this when the user asks for an overview of their day, daily stats, or a health summary
    for a particular date.

    Args:
        date: Date in YYYY-MM-DD format
    """
    client = await get_client()
    return await client.get_daily_summary(date)


@mcp.tool()
async def get_steps(date: str) -> dict:
    """Get total step count and daily step goal for a specific date.

    Use this when the user asks how many steps they took, whether they hit their step goal,
    or about their step count on a particular day.

    Args:
        date: Date in YYYY-MM-DD format
    """
    client = await get_client()
    return await client.get_steps(date)


@mcp.tool()
async def get_steps_chart(date: str) -> dict:
    """Get intraday step data showing step counts throughout the day.

    Use this when the user asks about their step pattern, when they were most active,
    or wants a time-series breakdown of steps during the day.

    Args:
        date: Date in YYYY-MM-DD format
    """
    client = await get_client()
    return await client.get_steps_chart(date)


@mcp.tool()
async def get_heart_rate(date: str) -> dict:
    """Get heart rate data including resting HR, max HR, heart rate zones, and time series.

    Use this when the user asks about their heart rate, pulse, cardiovascular data,
    or HR zones for a particular day.

    Args:
        date: Date in YYYY-MM-DD format
    """
    client = await get_client()
    return await client.get_heart_rate(date)


@mcp.tool()
async def get_resting_heart_rate(date: str) -> dict:
    """Get resting heart rate for a specific date.

    Use this when the user asks specifically about their resting heart rate or RHR
    for a particular day.

    Args:
        date: Date in YYYY-MM-DD format
    """
    client = await get_client()
    return await client.get_resting_heart_rate(date)


@mcp.tool()
async def get_stress(date: str) -> dict:
    """Get stress levels throughout the day including overall stress score and time series.

    Use this when the user asks about their stress, how stressed they were, or wants
    to understand their stress patterns for a particular day.

    Args:
        date: Date in YYYY-MM-DD format
    """
    client = await get_client()
    return await client.get_stress(date)


@mcp.tool()
async def get_body_battery(start_date: str, end_date: str) -> dict:
    """Get Body Battery energy levels over a date range.

    Use this when the user asks about their energy levels, body battery, how recovered
    they were, or wants to see battery trends over a period.

    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
    """
    client = await get_client()
    return await client.get_body_battery(start_date, end_date)


@mcp.tool()
async def get_body_battery_events(date: str) -> dict:
    """Get Body Battery charge and drain events for a specific day.

    Use this when the user asks what charged or drained their body battery,
    or wants to understand energy changes during a particular day.

    Args:
        date: Date in YYYY-MM-DD format
    """
    client = await get_client()
    return await client.get_body_battery_events(date)


@mcp.tool()
async def get_respiration(date: str) -> dict:
    """Get breathing rate data including average, highest, and lowest respiration values.

    Use this when the user asks about their breathing rate, respiration, or respiratory
    health for a particular day.

    Args:
        date: Date in YYYY-MM-DD format
    """
    client = await get_client()
    return await client.get_respiration(date)


@mcp.tool()
async def get_spo2(date: str) -> dict:
    """Get blood oxygen saturation (SpO2) data including average and lowest values.

    Use this when the user asks about their blood oxygen levels, SpO2, oxygen saturation,
    or pulse oximetry data for a particular day.

    Args:
        date: Date in YYYY-MM-DD format
    """
    client = await get_client()
    return await client.get_spo2(date)


@mcp.tool()
async def get_intensity_minutes(date: str) -> dict:
    """Get moderate and vigorous intensity minutes for a specific date.

    Use this when the user asks about their intensity minutes, active minutes,
    weekly activity goal progress, or how much time they spent exercising at moderate/vigorous levels.

    Args:
        date: Date in YYYY-MM-DD format
    """
    client = await get_client()
    return await client.get_intensity_minutes(date)


@mcp.tool()
async def get_floors(date: str) -> dict:
    """Get floors climbed and descended data for a specific date.

    Use this when the user asks about floors climbed, floors descended, elevation,
    or stair climbing activity for a particular day.

    Args:
        date: Date in YYYY-MM-DD format
    """
    client = await get_client()
    return await client.get_floors(date)


@mcp.tool()
async def get_hydration(date: str) -> dict:
    """Get daily hydration and water intake data.

    Use this when the user asks about their water intake, hydration level,
    or fluid consumption for a particular day.

    Args:
        date: Date in YYYY-MM-DD format
    """
    client = await get_client()
    return await client.get_hydration(date)


@mcp.tool()
async def get_daily_events(date: str) -> dict:
    """Get all daily wellness events including sleep, activities, and naps.

    Use this when the user asks what events were recorded during a day,
    wants a timeline of their wellness events, or asks about naps and activity events.

    Args:
        date: Date in YYYY-MM-DD format
    """
    client = await get_client()
    return await client.get_daily_events(date)
