"""Trends tools — weekly and range-based step, stress, intensity aggregates."""

from garmin_mcp.client import get_client
from garmin_mcp.server import mcp


@mcp.tool()
async def get_daily_steps_range(start_date: str, end_date: str) -> list:
    """Get daily step counts over a date range.

    Use this when the user asks about step trends, daily steps over time,
    or wants to see how their step count has changed over a period.

    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
    """
    client = await get_client()
    return await client.get_daily_steps_range(start_date, end_date)


@mcp.tool()
async def get_weekly_steps(date: str) -> dict:
    """Get weekly step aggregate summary for the week containing the given date.

    Use this when the user asks about their weekly step total, steps this week,
    or wants a weekly step summary.

    Args:
        date: Any date within the target week in YYYY-MM-DD format
    """
    client = await get_client()
    return await client.get_weekly_steps(date)


@mcp.tool()
async def get_weekly_stress(date: str) -> dict:
    """Get weekly stress aggregate summary for the week containing the given date.

    Use this when the user asks about their weekly stress levels, average stress
    this week, or stress trends over the week.

    Args:
        date: Any date within the target week in YYYY-MM-DD format
    """
    client = await get_client()
    return await client.get_weekly_stress(date)


@mcp.tool()
async def get_weekly_intensity_minutes(start_date: str, end_date: str) -> dict:
    """Get weekly intensity minutes (moderate and vigorous) over a date range.

    Use this when the user asks about intensity minutes, activity minutes goal,
    whether they met their weekly fitness goals, or moderate/vigorous exercise time.

    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
    """
    client = await get_client()
    return await client.get_weekly_intensity_minutes(start_date, end_date)
