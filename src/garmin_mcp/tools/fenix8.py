"""Fenix 8 AMOLED tools — running dynamics, training effect, power, ClimbPro."""

from garmin_mcp.client import get_client
from garmin_mcp.server import mcp


@mcp.tool()
async def get_running_dynamics(activity_id: str) -> dict:
    """Get running dynamics metrics like cadence, ground contact time, and stride length.

    Use this when the user asks about their running form, cadence, ground contact
    time, vertical oscillation, stride length, or ground contact balance for a run.

    Args:
        activity_id: The Garmin activity ID
    """
    client = await get_client()
    return await client.get_running_dynamics(activity_id)


@mcp.tool()
async def get_training_effect(activity_id: str) -> dict:
    """Get aerobic and anaerobic training effect scores for an activity.

    Use this when the user asks about the training effect, aerobic benefit,
    anaerobic benefit, or impact of a specific workout on their fitness.

    Args:
        activity_id: The Garmin activity ID
    """
    client = await get_client()
    return await client.get_training_effect(activity_id)


@mcp.tool()
async def get_activity_power_zones(activity_id: str) -> dict:
    """Get time spent in each power zone during an activity.

    Use this when the user asks about power zone distribution, time in zones,
    or power-based training intensity for a cycling or running activity.

    Args:
        activity_id: The Garmin activity ID
    """
    client = await get_client()
    return await client.get_activity_power_zones(activity_id)


@mcp.tool()
async def get_running_power(activity_id: str) -> dict:
    """Get running power metrics including average, max, and normalized power.

    Use this when the user asks about running power, wattage during a run,
    normalized power, or power-based running metrics.

    Args:
        activity_id: The Garmin activity ID
    """
    client = await get_client()
    return await client.get_running_power(activity_id)


@mcp.tool()
async def get_climbpro_data(activity_id: str) -> dict:
    """Get ClimbPro split summaries with climb segments for an activity.

    Use this when the user asks about climbs in an activity, elevation segments,
    ClimbPro data, or split summaries for a hilly workout.

    Args:
        activity_id: The Garmin activity ID
    """
    client = await get_client()
    return await client.get_climbpro_data(activity_id)


@mcp.tool()
async def get_activity_typed_splits(activity_id: str) -> dict:
    """Get typed split data (run, walk, rest segments) for an activity.

    Use this when the user asks about activity splits by type, run/walk intervals,
    or segment breakdowns within an activity.

    Args:
        activity_id: The Garmin activity ID
    """
    client = await get_client()
    return await client.get_activity_typed_splits(activity_id)


@mcp.tool()
async def get_morning_readiness(date: str) -> dict:
    """Get morning training readiness assessment with sleep and HRV context.

    Use this when the user asks about their morning readiness, how ready they
    are to train based on morning metrics, or morning recovery assessment.

    Args:
        date: Date in YYYY-MM-DD format
    """
    client = await get_client()
    return await client.get_morning_readiness(date)
