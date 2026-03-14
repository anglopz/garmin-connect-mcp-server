"""Device resource — garmin://device/fenix8."""

import json

from garmin_mcp.client import get_client
from garmin_mcp.server import mcp


@mcp.resource("garmin://device/fenix8")
async def fenix8_device_info() -> str:
    """Fenix 8 AMOLED device information and status.

    Returns registered device details including device name, software version,
    and current battery level.
    """
    client = await get_client()
    raw_devices = await client.get_devices()
    devices = [
        {
            "deviceId": d.get("deviceId"),
            "deviceName": d.get("deviceName"),
            "productDisplayName": d.get("productDisplayName"),
            "softwareVersion": d.get("softwareVersionString"),
            "batteryLevel": d.get("batteryLevel"),
        }
        for d in (raw_devices if isinstance(raw_devices, list) else [])
    ]
    return json.dumps({"devices": devices}, indent=2, default=str)
