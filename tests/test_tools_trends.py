"""Tests for trends tools — daily/weekly step, stress, intensity aggregates."""

import pytest

from garmin_mcp.client import GarminClient


@pytest.mark.asyncio
async def test_get_daily_steps_range(mock_garmin):
    mock_garmin.get_daily_steps.return_value = [
        {"calendarDate": "2026-03-01", "totalSteps": 8000},
        {"calendarDate": "2026-03-02", "totalSteps": 10500},
    ]
    client = GarminClient(mock_garmin)
    result = await client.get_daily_steps_range("2026-03-01", "2026-03-07")
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["totalSteps"] == 8000
    mock_garmin.get_daily_steps.assert_called_once_with("2026-03-01", "2026-03-07")


@pytest.mark.asyncio
async def test_get_daily_steps_range_non_list(mock_garmin):
    mock_garmin.get_daily_steps.return_value = {}
    client = GarminClient(mock_garmin)
    result = await client.get_daily_steps_range("2026-03-01", "2026-03-07")
    assert result == []


@pytest.mark.asyncio
async def test_get_weekly_steps(mock_garmin):
    mock_garmin.get_weekly_steps.return_value = {"weeklySteps": 56000}
    client = GarminClient(mock_garmin)
    result = await client.get_weekly_steps("2026-03-14")
    assert result["date"] == "2026-03-14"
    assert "weekly_steps" in result
    mock_garmin.get_weekly_steps.assert_called_once_with("2026-03-14")


@pytest.mark.asyncio
async def test_get_weekly_stress(mock_garmin):
    mock_garmin.get_weekly_stress.return_value = {"avgStressLevel": 28}
    client = GarminClient(mock_garmin)
    result = await client.get_weekly_stress("2026-03-14")
    assert result["date"] == "2026-03-14"
    assert "weekly_stress" in result
    mock_garmin.get_weekly_stress.assert_called_once_with("2026-03-14")


@pytest.mark.asyncio
async def test_get_weekly_intensity_minutes(mock_garmin):
    mock_garmin.get_weekly_intensity_minutes.return_value = {
        "moderateIntensityMinutes": 120,
        "vigorousIntensityMinutes": 45,
    }
    client = GarminClient(mock_garmin)
    result = await client.get_weekly_intensity_minutes("2026-03-01", "2026-03-14")
    assert result["start_date"] == "2026-03-01"
    assert result["end_date"] == "2026-03-14"
    assert "weekly_intensity" in result
    mock_garmin.get_weekly_intensity_minutes.assert_called_once_with("2026-03-01", "2026-03-14")
