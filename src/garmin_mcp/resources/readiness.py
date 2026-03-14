"""Training readiness resource — garmin://training/readiness."""

import json
from datetime import date

from garmin_mcp.client import get_client
from garmin_mcp.server import mcp


@mcp.resource("garmin://training/readiness")
async def training_readiness() -> str:
    """Training readiness and body battery for today.

    Returns the current training readiness score and body battery levels
    to help determine how ready the athlete is to train.
    """
    client = await get_client()
    today = date.today().isoformat()
    data: dict = {}

    try:
        data["training_readiness"] = await client.get_training_readiness(today)
    except Exception as e:
        data["training_readiness"] = {"error": str(e)}

    try:
        data["body_battery"] = await client.get_body_battery(today, today)
    except Exception as e:
        data["body_battery"] = {"error": str(e)}

    data["date"] = today
    return json.dumps(data, indent=2, default=str)
