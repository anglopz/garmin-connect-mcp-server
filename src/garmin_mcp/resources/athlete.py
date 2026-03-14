"""Athlete profile resource — garmin://athlete/profile."""

import json

from garmin_mcp.client import get_client
from garmin_mcp.server import mcp


@mcp.resource("garmin://athlete/profile")
async def athlete_profile() -> str:
    """Athlete profile with account info and preferences.

    Returns the user's Garmin Connect profile including display name,
    username, and account settings.
    """
    client = await get_client()
    profile = await client.get_user_profile()
    return json.dumps({"profile": profile}, indent=2, default=str)
