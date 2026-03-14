"""Profile tools — user profile, devices, gear, goals, and workouts."""

from garmin_mcp.client import get_client
from garmin_mcp.server import mcp


@mcp.tool()
async def get_user_profile() -> dict:
    """Get the user's Garmin Connect social profile and preferences.

    Use this when the user asks about their Garmin account, display name,
    username, or personal profile information.
    """
    try:
        client = await get_client()
        return await client.get_user_profile()
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def get_user_settings() -> dict:
    """Get the user's Garmin Connect account settings.

    Use this when the user asks about their measurement units, language,
    sleep schedule settings, or account preferences.
    """
    try:
        client = await get_client()
        return await client.get_user_settings()
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def get_devices() -> list:
    """Get all Garmin devices registered to the user's account.

    Use this when the user asks what Garmin devices they have, wants a
    list of their watches or GPS devices.
    """
    try:
        client = await get_client()
        return await client.get_devices()
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def get_device_settings(device_id: str) -> dict:
    """Get settings for a specific Garmin device.

    Use this when the user asks about settings for a particular device.

    Args:
        device_id: The unique device identifier
    """
    try:
        client = await get_client()
        return await client.get_device_settings(device_id)
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def get_device_last_used() -> dict:
    """Get information about the most recently used Garmin device.

    Use this when the user asks which device they last used or wants
    info about their most recently active device.
    """
    try:
        client = await get_client()
        return await client.get_device_last_used()
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def get_primary_training_device() -> dict:
    """Get the user's primary training device.

    Use this when the user asks which device is set as their main training
    device or primary watch.
    """
    try:
        client = await get_client()
        return await client.get_primary_training_device()
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def get_gear() -> list:
    """Get all tracked gear and equipment for the user.

    Use this when the user asks about their running shoes, bikes, or other
    gear they're tracking in Garmin Connect.
    """
    try:
        client = await get_client()
        return await client.get_gear()
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def get_gear_stats(gear_uuid: str) -> dict:
    """Get usage statistics for a specific piece of gear.

    Use this when the user asks how many miles or kilometers are on a specific
    pair of shoes or piece of equipment.

    Args:
        gear_uuid: The unique identifier (UUID) for the gear item
    """
    try:
        client = await get_client()
        return await client.get_gear_stats(gear_uuid)
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def get_goals() -> list:
    """Get the user's active fitness goals and progress.

    Use this when the user asks about their goals, targets, or what they're
    working toward in Garmin Connect.
    """
    try:
        client = await get_client()
        return await client.get_goals()
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def get_earned_badges() -> list:
    """Get all badges and achievements earned by the user.

    Use this when the user asks about their badges, awards, or achievements
    in Garmin Connect.
    """
    try:
        client = await get_client()
        return await client.get_earned_badges()
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def get_workouts() -> list:
    """Get all saved workouts from the user's Garmin Connect library.

    Use this when the user asks about their saved or planned workouts,
    structured training sessions, or workout library.
    """
    try:
        client = await get_client()
        return await client.get_workouts()
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def get_workout(workout_id: str) -> dict:
    """Get a specific saved workout by its ID.

    Use this when the user wants details about a particular saved workout,
    including its structure, steps, and target metrics.

    Args:
        workout_id: The unique identifier for the workout
    """
    try:
        client = await get_client()
        return await client.get_workout(workout_id)
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def get_activity_gear(activity_id: str) -> dict:
    """Get the gear used during a specific activity.

    Use this when the user asks which shoes or equipment they used for
    a particular run, ride, or other activity.

    Args:
        activity_id: The unique identifier for the activity
    """
    try:
        client = await get_client()
        return await client.get_activity_gear(activity_id)
    except Exception as e:
        return {"error": str(e)}
