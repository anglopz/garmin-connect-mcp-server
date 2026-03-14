"""Tests for activity tools — client methods (GarminClient adapter layer)."""

from __future__ import annotations

import pytest

from garmin_mcp.client import GarminClient


@pytest.mark.asyncio
async def test_get_activities(mock_garmin):
    mock_garmin.get_activities.return_value = [
        {"activityId": 123, "activityName": "Morning Run"}
    ]
    client = GarminClient(mock_garmin)
    result = await client.get_activities(0, 10)
    assert len(result) == 1
    assert result[0]["activityId"] == 123
    mock_garmin.get_activities.assert_called_once_with(0, 10)


@pytest.mark.asyncio
async def test_get_activities_by_date(mock_garmin):
    mock_garmin.get_activities_by_date.return_value = [
        {"activityId": 456, "activityName": "Evening Ride"}
    ]
    client = GarminClient(mock_garmin)
    result = await client.get_activities_by_date("2026-03-01", "2026-03-14", "cycling")
    assert len(result) == 1
    assert result[0]["activityId"] == 456
    mock_garmin.get_activities_by_date.assert_called_once_with(
        "2026-03-01", "2026-03-14", "cycling"
    )


@pytest.mark.asyncio
async def test_get_activities_by_date_no_type(mock_garmin):
    mock_garmin.get_activities_by_date.return_value = []
    client = GarminClient(mock_garmin)
    result = await client.get_activities_by_date("2026-03-01", "2026-03-14")
    mock_garmin.get_activities_by_date.assert_called_once_with(
        "2026-03-01", "2026-03-14", None
    )
    assert result == []


@pytest.mark.asyncio
async def test_get_last_activity(mock_garmin):
    mock_garmin.get_last_activity.return_value = {
        "activityId": 123,
        "activityName": "Morning Run",
    }
    client = GarminClient(mock_garmin)
    result = await client.get_last_activity()
    assert result["activityId"] == 123
    assert result["activityName"] == "Morning Run"
    mock_garmin.get_last_activity.assert_called_once()


@pytest.mark.asyncio
async def test_count_activities(mock_garmin):
    mock_garmin.count_activities.return_value = {"total": 342}
    client = GarminClient(mock_garmin)
    result = await client.count_activities()
    assert result["total"] == 342
    mock_garmin.count_activities.assert_called_once()


@pytest.mark.asyncio
async def test_get_activity(mock_garmin):
    mock_garmin.get_activity.return_value = {
        "activityId": 789,
        "activityName": "Trail Run",
        "distance": 10500.0,
    }
    client = GarminClient(mock_garmin)
    result = await client.get_activity("789")
    assert result["activityId"] == 789
    mock_garmin.get_activity.assert_called_once_with("789")


@pytest.mark.asyncio
async def test_get_activity_details(mock_garmin):
    mock_garmin.get_activity_details.return_value = {
        "activityId": 789,
        "heartRateData": [],
        "elevationData": [],
    }
    client = GarminClient(mock_garmin)
    result = await client.get_activity_details("789")
    assert result["activityId"] == 789
    mock_garmin.get_activity_details.assert_called_once_with("789")


@pytest.mark.asyncio
async def test_get_activity_splits(mock_garmin):
    mock_garmin.get_activity_splits.return_value = {
        "lapDTOs": [{"distance": 1000, "duration": 360}]
    }
    client = GarminClient(mock_garmin)
    result = await client.get_activity_splits("789")
    assert "lapDTOs" in result
    mock_garmin.get_activity_splits.assert_called_once_with("789")


@pytest.mark.asyncio
async def test_get_activity_weather(mock_garmin):
    mock_garmin.get_activity_weather.return_value = {
        "temperature": 15,
        "humidity": 60,
        "windSpeed": 10,
    }
    client = GarminClient(mock_garmin)
    result = await client.get_activity_weather("789")
    assert result["temperature"] == 15
    mock_garmin.get_activity_weather.assert_called_once_with("789")


@pytest.mark.asyncio
async def test_get_activity_hr_zones(mock_garmin):
    mock_garmin.get_activity_hr_in_timezones.return_value = {
        "zones": [{"zone": 1, "seconds": 600}, {"zone": 2, "seconds": 1200}]
    }
    client = GarminClient(mock_garmin)
    result = await client.get_activity_hr_zones("789")
    assert "zones" in result
    mock_garmin.get_activity_hr_in_timezones.assert_called_once_with("789")


@pytest.mark.asyncio
async def test_get_activity_exercise_sets(mock_garmin):
    mock_garmin.get_activity_exercise_sets.return_value = {
        "exerciseSets": [{"setType": "ACTIVE", "reps": 10, "weight": 60.0}]
    }
    client = GarminClient(mock_garmin)
    result = await client.get_activity_exercise_sets("789")
    assert "exerciseSets" in result
    mock_garmin.get_activity_exercise_sets.assert_called_once_with("789")


@pytest.mark.asyncio
async def test_get_activity_types(mock_garmin):
    mock_garmin.get_activity_types.return_value = [
        {"typeId": 1, "typeKey": "running"},
        {"typeId": 2, "typeKey": "cycling"},
    ]
    client = GarminClient(mock_garmin)
    result = await client.get_activity_types()
    assert len(result) == 2
    assert result[0]["typeKey"] == "running"
    mock_garmin.get_activity_types.assert_called_once()


@pytest.mark.asyncio
async def test_get_progress_summary(mock_garmin):
    mock_garmin.get_progress_summary_between_dates.return_value = {
        "totalDistance": 85000.0,
        "totalDuration": 36000,
        "activityCount": 12,
    }
    client = GarminClient(mock_garmin)
    result = await client.get_progress_summary("2026-03-01", "2026-03-14")
    assert result["activityCount"] == 12
    mock_garmin.get_progress_summary_between_dates.assert_called_once_with(
        "2026-03-01", "2026-03-14"
    )
