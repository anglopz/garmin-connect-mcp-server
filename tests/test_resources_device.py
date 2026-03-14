"""Tests for device resource — garmin://device/fenix8."""

import json
from unittest.mock import AsyncMock, patch

import pytest

from garmin_mcp.client import GarminClient


@pytest.mark.asyncio
async def test_fenix8_device_info(garmin_client: GarminClient, mock_garmin):
    from garmin_mcp.resources.device import fenix8_device_info

    mock_garmin.get_devices.return_value = [
        {
            "deviceId": "abc123",
            "deviceName": "Fenix 8 AMOLED",
            "productDisplayName": "fenix 8 47mm AMOLED",
            "softwareVersionString": "21.00",
            "batteryLevel": 85,
        }
    ]

    mock_get = AsyncMock(return_value=garmin_client)
    with patch("garmin_mcp.resources.device.get_client", new=mock_get):
        result = await fenix8_device_info()

    data = json.loads(result)
    assert len(data["devices"]) == 1
    device = data["devices"][0]
    assert device["deviceId"] == "abc123"
    assert device["deviceName"] == "Fenix 8 AMOLED"
    assert device["productDisplayName"] == "fenix 8 47mm AMOLED"
    assert device["softwareVersion"] == "21.00"
    assert device["batteryLevel"] == 85
