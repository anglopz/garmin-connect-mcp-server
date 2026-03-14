"""Tests for Garmin MCP resources."""

import json
from unittest.mock import AsyncMock, patch

import pytest

from garmin_mcp.client import GarminClient


@pytest.mark.asyncio
async def test_athlete_profile(garmin_client: GarminClient, mock_garmin):
    from garmin_mcp.resources.athlete import athlete_profile

    mock_get = AsyncMock(return_value=garmin_client)
    with patch("garmin_mcp.resources.athlete.get_client", new=mock_get):
        result = await athlete_profile()

    data = json.loads(result)
    assert "profile" in data
    assert data["profile"]["displayName"] == "TestUser"


@pytest.mark.asyncio
async def test_training_readiness_success(garmin_client: GarminClient, mock_garmin):
    from garmin_mcp.resources.readiness import training_readiness

    mock_garmin.get_training_readiness.return_value = {"trainingReadinessScore": 72}
    mock_garmin.get_body_battery.return_value = [{"charged": 80}]

    mock_get = AsyncMock(return_value=garmin_client)
    with patch("garmin_mcp.resources.readiness.get_client", new=mock_get):
        result = await training_readiness()

    data = json.loads(result)
    assert "date" in data
    assert "training_readiness" in data
    assert "body_battery" in data


@pytest.mark.asyncio
async def test_training_readiness_fallback_on_error(garmin_client: GarminClient, mock_garmin):
    from garmin_mcp.resources.readiness import training_readiness

    mock_garmin.get_training_readiness.side_effect = NotImplementedError("not implemented")
    mock_garmin.get_body_battery.side_effect = NotImplementedError("not implemented")

    mock_get = AsyncMock(return_value=garmin_client)
    with patch("garmin_mcp.resources.readiness.get_client", new=mock_get):
        result = await training_readiness()

    data = json.loads(result)
    assert "error" in data["training_readiness"]
    assert "error" in data["body_battery"]


@pytest.mark.asyncio
async def test_daily_health_success(garmin_client: GarminClient, mock_garmin):
    from garmin_mcp.resources.daily import daily_health

    mock_garmin.get_user_summary.return_value = {"totalSteps": 8500}
    mock_garmin.get_sleep_data.return_value = {"sleepScore": 82}
    mock_garmin.get_all_day_stress.return_value = {"overallStressLevel": 32}

    with patch("garmin_mcp.resources.daily.get_client", new=AsyncMock(return_value=garmin_client)):
        result = await daily_health()

    data = json.loads(result)
    assert "date" in data
    assert "daily_summary" in data
    assert "sleep" in data
    assert "stress" in data


@pytest.mark.asyncio
async def test_daily_health_fallback_on_error(garmin_client: GarminClient, mock_garmin):
    from garmin_mcp.resources.daily import daily_health

    mock_garmin.get_user_summary.side_effect = NotImplementedError("not implemented")
    mock_garmin.get_sleep_data.side_effect = NotImplementedError("not implemented")
    mock_garmin.get_all_day_stress.side_effect = NotImplementedError("not implemented")

    with patch("garmin_mcp.resources.daily.get_client", new=AsyncMock(return_value=garmin_client)):
        result = await daily_health()

    data = json.loads(result)
    assert "error" in data["daily_summary"]
    assert "error" in data["sleep"]
    assert "error" in data["stress"]
