"""Analysis tools — activity comparison, similarity search, period analysis."""

from garmin_mcp.client import get_client
from garmin_mcp.server import mcp


@mcp.tool()
async def compare_activities(activity_ids: list[str]) -> dict:
    """Compare 2 to 5 activities side by side with key metrics.

    Use this when the user wants to compare specific activities, see how two
    runs or rides differ, or analyze performance differences between workouts.

    Args:
        activity_ids: List of 2-5 activity IDs to compare
    """
    client = await get_client()
    return await client.compare_activities(activity_ids)


@mcp.tool()
async def find_similar_activities(activity_id: str, limit: int = 5) -> list:
    """Find activities similar to a reference activity based on type and distance.

    Use this when the user asks to find similar workouts, comparable runs,
    or wants to see past activities that match a given one.

    Args:
        activity_id: Reference activity ID to find similar activities for
        limit: Maximum number of similar activities to return (default 5)
    """
    client = await get_client()
    return await client.find_similar_activities(activity_id, limit)


@mcp.tool()
async def analyze_training_period(start_date: str, end_date: str) -> dict:
    """Analyze training over a time period with aggregated stats and insights.

    Use this when the user asks for a training summary, overview of a training
    block, season review, or wants to understand their training volume and
    patterns over a specific date range.

    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
    """
    client = await get_client()
    return await client.analyze_training_period(start_date, end_date)
