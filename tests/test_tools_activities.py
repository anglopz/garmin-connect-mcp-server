"""Tests for activity tools — client methods (GarminClient adapter layer)."""

from __future__ import annotations

import pytest

from garmin_mcp.client import GarminClient


@pytest.mark.asyncio
async def test_get_activities(mock_garmin):
    mock_garmin.get_activities.return_value = [{"activityId": 123, "activityName": "Morning Run"}]
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
    mock_garmin.get_activities_by_date.assert_called_once_with("2026-03-01", "2026-03-14", None)
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
    mock_garmin.count_activities.return_value = 20
    client = GarminClient(mock_garmin)
    result = await client.count_activities()
    assert result["total_activities"] == 20
    mock_garmin.count_activities.assert_called_once()


@pytest.mark.asyncio
async def test_get_activity(mock_garmin):
    mock_garmin.get_activity.return_value = {
        "activityId": 789,
        "activityName": "Trail Run",
        "summaryDTO": {"distance": 10500.0, "duration": 3600.0},
    }
    client = GarminClient(mock_garmin)
    result = await client.get_activity("789")
    assert result["activityId"] == 789
    mock_garmin.get_activity.assert_called_once_with("789")


@pytest.mark.asyncio
async def test_get_activity_details(mock_garmin):
    mock_garmin.get_activity_details.return_value = {
        "activityId": 789,
        "metricDescriptors": [],
        "activityDetailMetrics": [],
        "heartRateDTOs": [],
    }
    client = GarminClient(mock_garmin)
    result = await client.get_activity_details("789")
    assert result["activityId"] == 789
    mock_garmin.get_activity_details.assert_called_once_with("789")


@pytest.mark.asyncio
async def test_get_activity_splits(mock_garmin):
    mock_garmin.get_activity_splits.return_value = {
        "activityId": 789,
        "lapDTOs": [{"distance": 1609.34, "duration": 659.562, "averageHR": 159.0}],
    }
    client = GarminClient(mock_garmin)
    result = await client.get_activity_splits("789")
    assert "lapDTOs" in result
    assert result["lapDTOs"][0]["distance"] == 1609.34
    mock_garmin.get_activity_splits.assert_called_once_with("789")


@pytest.mark.asyncio
async def test_get_activity_weather(mock_garmin):
    mock_garmin.get_activity_weather.return_value = {
        "temp": 15,
        "relativeHumidity": 60,
        "windSpeed": 10,
        "windDirection": 180,
    }
    client = GarminClient(mock_garmin)
    result = await client.get_activity_weather("789")
    assert result["temp"] == 15
    assert result["relativeHumidity"] == 60
    mock_garmin.get_activity_weather.assert_called_once_with("789")


@pytest.mark.asyncio
async def test_get_activity_hr_zones(mock_garmin):
    mock_garmin.get_activity_hr_in_timezones.return_value = [
        {"zoneNumber": 1, "secsInZone": 89.007, "zoneLowBoundary": 98},
        {"zoneNumber": 2, "secsInZone": 484.98, "zoneLowBoundary": 117},
    ]
    client = GarminClient(mock_garmin)
    result = await client.get_activity_hr_zones("789")
    assert result["activity_id"] == "789"
    assert len(result["hr_zones"]) == 2
    assert result["hr_zones"][0]["zoneNumber"] == 1
    assert result["hr_zones"][0]["secsInZone"] == 89.007
    mock_garmin.get_activity_hr_in_timezones.assert_called_once_with("789")


@pytest.mark.asyncio
async def test_get_activity_exercise_sets(mock_garmin):
    mock_garmin.get_activity_exercise_sets.return_value = {
        "activityId": 789,
        "exerciseSets": [
            {
                "exercises": [{"category": "BENCH_PRESS", "probability": 43.75}],
                "duration": 77.285,
                "repetitionCount": 8,
                "weight": 40812.0,
                "setType": "ACTIVE",
            }
        ],
    }
    client = GarminClient(mock_garmin)
    result = await client.get_activity_exercise_sets("789")
    assert "exerciseSets" in result
    assert result["exerciseSets"][0]["repetitionCount"] == 8
    assert result["exerciseSets"][0]["setType"] == "ACTIVE"
    mock_garmin.get_activity_exercise_sets.assert_called_once_with("789")


@pytest.mark.asyncio
async def test_get_activity_types(mock_garmin):
    mock_garmin.get_activity_types.return_value = [
        {"typeId": 1, "typeKey": "running", "parentTypeId": 17},
        {"typeId": 2, "typeKey": "cycling", "parentTypeId": 17},
    ]
    client = GarminClient(mock_garmin)
    result = await client.get_activity_types()
    assert len(result) == 2
    assert result[0]["typeKey"] == "running"
    mock_garmin.get_activity_types.assert_called_once()


@pytest.mark.asyncio
async def test_get_progress_summary(mock_garmin):
    mock_garmin.get_progress_summary_between_dates.return_value = [
        {
            "date": "2026-03-14",
            "countOfActivities": 1,
            "stats": {
                "running": {
                    "distance": {"count": 3, "sum": 913690.99},
                }
            },
        }
    ]
    client = GarminClient(mock_garmin)
    result = await client.get_progress_summary("2026-03-01", "2026-03-14")
    assert result["start_date"] == "2026-03-01"
    assert result["end_date"] == "2026-03-14"
    assert len(result["summaries"]) == 1
    assert result["summaries"][0]["countOfActivities"] == 1
    mock_garmin.get_progress_summary_between_dates.assert_called_once_with(
        "2026-03-01", "2026-03-14"
    )
