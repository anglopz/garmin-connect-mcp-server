"""Activity tools for the Garmin Connect MCP server.

Exposes 12 tools for querying Garmin Connect activity data.
"""

from __future__ import annotations

from garmin_mcp.client import get_client
from garmin_mcp.server import mcp


@mcp.tool()
async def get_activities(start: int = 0, limit: int = 10) -> list[dict]:
    """List recent activities with pagination.

    Use this when the user asks to see their recent workouts, runs, rides,
    swims, or other exercises. Returns a list of activity summaries.

    Args:
        start: Starting index for pagination (default 0)
        limit: Number of activities to return (default 10)
    """
    client = await get_client()
    return await client.get_activities(start, limit)


@mcp.tool()
async def get_activities_by_date(
    start_date: str, end_date: str, activity_type: str | None = None
) -> list[dict]:
    """Search activities within a date range, optionally filtered by type.

    Use this when the user asks about activities in a specific time period,
    e.g. "show my runs last week" or "all activities in March".

    Args:
        start_date: Start of date range in YYYY-MM-DD format
        end_date: End of date range in YYYY-MM-DD format
        activity_type: Optional activity type filter (e.g. "running", "cycling")
    """
    client = await get_client()
    return await client.get_activities_by_date(start_date, end_date, activity_type)


@mcp.tool()
async def get_last_activity() -> dict:
    """Get the most recent activity recorded.

    Use this when the user asks about their latest or most recent workout,
    run, or exercise session.
    """
    client = await get_client()
    return await client.get_last_activity()


@mcp.tool()
async def count_activities() -> dict:
    """Get the total number of activities recorded on Garmin Connect.

    Use this when the user asks how many workouts or activities they have
    logged in total.
    """
    client = await get_client()
    return await client.count_activities()


@mcp.tool()
async def get_activity(activity_id: str) -> dict:
    """Get summary data for a specific activity by its ID.

    Use this when the user asks for details about a particular activity
    and you have the activity ID. Returns high-level summary metrics.

    Args:
        activity_id: The Garmin Connect activity ID
    """
    client = await get_client()
    return await client.get_activity(activity_id)


@mcp.tool()
async def get_activity_details(activity_id: str) -> dict:
    """Get detailed metrics for a specific activity including HR, pace, and elevation time series.

    Use this when the user wants in-depth data about a workout such as
    heart rate graphs, pace over time, or elevation profile.

    Args:
        activity_id: The Garmin Connect activity ID
    """
    client = await get_client()
    return await client.get_activity_details(activity_id)


@mcp.tool()
async def get_activity_splits(activity_id: str) -> dict:
    """Get per-km or per-mile split data for an activity.

    Use this when the user asks how fast each mile or kilometer was in a
    run or how their pace varied throughout a workout.

    Args:
        activity_id: The Garmin Connect activity ID
    """
    client = await get_client()
    return await client.get_activity_splits(activity_id)


@mcp.tool()
async def get_activity_weather(activity_id: str) -> dict:
    """Get weather conditions recorded during an activity.

    Use this when the user asks what the weather was like during a workout,
    including temperature, humidity, and wind conditions.

    Args:
        activity_id: The Garmin Connect activity ID
    """
    client = await get_client()
    return await client.get_activity_weather(activity_id)


@mcp.tool()
async def get_activity_hr_zones(activity_id: str) -> dict:
    """Get time spent in each heart rate zone during an activity.

    Use this when the user asks about heart rate zone distribution,
    training intensity breakdown, or how much time they spent in zone 2, 3, etc.

    Args:
        activity_id: The Garmin Connect activity ID
    """
    client = await get_client()
    return await client.get_activity_hr_zones(activity_id)


@mcp.tool()
async def get_activity_exercise_sets(activity_id: str) -> dict:
    """Get strength training sets including reps and weight for an activity.

    Use this when the user asks about their gym workout details, how many
    sets/reps they did, or what weights they lifted.

    Args:
        activity_id: The Garmin Connect activity ID
    """
    client = await get_client()
    return await client.get_activity_exercise_sets(activity_id)


@mcp.tool()
async def get_activity_types() -> list[dict]:
    """Get all available activity types supported by Garmin Connect.

    Use this when the user wants to know what kinds of activities they can
    track, or when you need to find valid activity type names for filtering.
    """
    client = await get_client()
    return await client.get_activity_types()


@mcp.tool()
async def get_progress_summary(start_date: str, end_date: str) -> dict:
    """Get a fitness progress summary over a date range broken down by activity type.

    Use this when the user asks for an overview of their training progress,
    total distances, times, or workout counts over a period.

    Args:
        start_date: Start of date range in YYYY-MM-DD format
        end_date: End of date range in YYYY-MM-DD format
    """
    client = await get_client()
    return await client.get_progress_summary(start_date, end_date)
