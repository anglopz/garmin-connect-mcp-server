"""Tests for health tool client methods."""

import pytest

from garmin_mcp.client import GarminClient


@pytest.mark.asyncio
async def test_get_daily_summary(mock_garmin):
    mock_garmin.get_user_summary.return_value = {
        "totalSteps": 8500,
        "totalDistanceMeters": 6200.0,
        "activeKilocalories": 450,
        "bmrKilocalories": 1800,
        "floorsAscended": 5,
        "restingHeartRate": 52,
    }
    client = GarminClient(mock_garmin)
    result = await client.get_daily_summary("2026-03-14")
    assert result["date"] == "2026-03-14"
    assert result["total_steps"] == 8500
    assert result["total_distance_meters"] == 6200.0
    assert result["active_kilocalories"] == 450
    assert result["floors_ascended"] == 5
    assert result["resting_heart_rate"] == 52
    mock_garmin.get_user_summary.assert_called_once_with("2026-03-14")


@pytest.mark.asyncio
async def test_get_steps(mock_garmin):
    mock_garmin.get_steps_data.return_value = {
        "totalSteps": 10234,
        "dailyStepGoal": 10000,
    }
    client = GarminClient(mock_garmin)
    result = await client.get_steps("2026-03-14")
    assert result["date"] == "2026-03-14"
    assert result["total_steps"] == 10234
    assert result["step_goal"] == 10000
    mock_garmin.get_steps_data.assert_called_once_with("2026-03-14")


@pytest.mark.asyncio
async def test_get_steps_chart(mock_garmin):
    mock_garmin.get_steps_data.return_value = {
        "totalSteps": 10234,
        "stepList": [{"startGMT": "2026-03-14 08:00:00", "steps": 500}],
    }
    client = GarminClient(mock_garmin)
    result = await client.get_steps_chart("2026-03-14")
    assert result["date"] == "2026-03-14"
    assert len(result["time_series"]) == 1
    assert result["time_series"][0]["steps"] == 500


@pytest.mark.asyncio
async def test_get_heart_rate(mock_garmin):
    mock_garmin.get_heart_rates.return_value = {
        "restingHeartRate": 52,
        "maxHeartRate": 165,
        "heartRateZones": [{"zoneName": "Zone 1"}],
        "heartRateValues": [[1710391200000, 58]],
    }
    client = GarminClient(mock_garmin)
    result = await client.get_heart_rate("2026-03-14")
    assert result["date"] == "2026-03-14"
    assert result["resting_heart_rate"] == 52
    assert result["max_heart_rate"] == 165
    assert len(result["heart_rate_zones"]) == 1
    assert len(result["time_series"]) == 1
    mock_garmin.get_heart_rates.assert_called_once_with("2026-03-14")


@pytest.mark.asyncio
async def test_get_resting_heart_rate(mock_garmin):
    mock_garmin.get_resting_heart_rate.return_value = {
        "allMetrics": {"metricsMap": {"WELLNESS_RESTING_HEART_RATE": [{"value": 52.0}]}}
    }
    client = GarminClient(mock_garmin)
    result = await client.get_resting_heart_rate("2026-03-14")
    assert result["date"] == "2026-03-14"
    assert result["resting_heart_rate"] == 52.0
    assert result["value"] == 52.0
    mock_garmin.get_resting_heart_rate.assert_called_once_with("2026-03-14")


@pytest.mark.asyncio
async def test_get_resting_heart_rate_missing_metrics(mock_garmin):
    mock_garmin.get_resting_heart_rate.return_value = {}
    client = GarminClient(mock_garmin)
    result = await client.get_resting_heart_rate("2026-03-14")
    assert result["date"] == "2026-03-14"
    assert result["resting_heart_rate"] is None


@pytest.mark.asyncio
async def test_get_stress(mock_garmin):
    mock_garmin.get_all_day_stress.return_value = {
        "overallStressLevel": 32,
        "restStressDuration": 14400,
        "lowStressDuration": 7200,
        "mediumStressDuration": 3600,
        "highStressDuration": 1800,
        "stressValuesArray": [[1710391200000, 25]],
    }
    client = GarminClient(mock_garmin)
    result = await client.get_stress("2026-03-14")
    assert result["date"] == "2026-03-14"
    assert result["overall_stress_level"] == 32
    assert result["rest_stress_duration"] == 14400
    assert len(result["stress_values"]) == 1
    mock_garmin.get_all_day_stress.assert_called_once_with("2026-03-14")


@pytest.mark.asyncio
async def test_get_body_battery(mock_garmin):
    mock_garmin.get_body_battery.return_value = [
        {"date": "2026-03-14", "charged": 80, "drained": 45},
    ]
    client = GarminClient(mock_garmin)
    result = await client.get_body_battery("2026-03-14", "2026-03-14")
    assert result["start_date"] == "2026-03-14"
    assert result["end_date"] == "2026-03-14"
    assert len(result["data"]) == 1
    mock_garmin.get_body_battery.assert_called_once_with("2026-03-14", "2026-03-14")


@pytest.mark.asyncio
async def test_get_body_battery_events(mock_garmin):
    mock_garmin.get_body_battery_events.return_value = [
        {"type": "ACTIVITY", "startTimestampGMT": "2026-03-14 07:00:00"},
    ]
    client = GarminClient(mock_garmin)
    result = await client.get_body_battery_events("2026-03-14")
    assert result["date"] == "2026-03-14"
    assert len(result["events"]) == 1
    mock_garmin.get_body_battery_events.assert_called_once_with("2026-03-14")


@pytest.mark.asyncio
async def test_get_respiration(mock_garmin):
    mock_garmin.get_respiration_data.return_value = {
        "avgWakingRespirationValue": 16.5,
        "highestRespirationValue": 22.0,
        "lowestRespirationValue": 12.0,
        "avgSleepRespirationValue": 14.0,
        "respirationValues": [[1710391200000, 16]],
    }
    client = GarminClient(mock_garmin)
    result = await client.get_respiration("2026-03-14")
    assert result["date"] == "2026-03-14"
    assert result["avg_waking_respiration_value"] == 16.5
    assert result["highest_respiration_value"] == 22.0
    assert result["lowest_respiration_value"] == 12.0
    assert len(result["respiration_values"]) == 1
    mock_garmin.get_respiration_data.assert_called_once_with("2026-03-14")


@pytest.mark.asyncio
async def test_get_spo2(mock_garmin):
    mock_garmin.get_spo2_data.return_value = {
        "averageSpO2": 97.5,
        "lowestSpO2": 94.0,
        "onDemandReadingList": [{"startTimestampGMT": "2026-03-14 08:00:00", "reading": 98}],
        "spO2HourlyAverages": [],
    }
    client = GarminClient(mock_garmin)
    result = await client.get_spo2("2026-03-14")
    assert result["date"] == "2026-03-14"
    assert result["avg_spo2"] == 97.5
    assert result["lowest_spo2"] == 94.0
    assert len(result["on_demand_reading_list"]) == 1
    mock_garmin.get_spo2_data.assert_called_once_with("2026-03-14")


@pytest.mark.asyncio
async def test_get_intensity_minutes(mock_garmin):
    mock_garmin.get_intensity_minutes_data.return_value = {
        "weeklyIntensityMinutes": {
            "moderateIntensityMinutes": 45,
            "vigorousIntensityMinutes": 20,
        },
        "weeklyGoal": 150,
        "intensityMinutesGoal": 150,
    }
    client = GarminClient(mock_garmin)
    result = await client.get_intensity_minutes("2026-03-14")
    assert result["date"] == "2026-03-14"
    assert result["moderate_intensity_minutes"] == 45
    assert result["vigorous_intensity_minutes"] == 20
    assert result["weekly_goal"] == 150
    mock_garmin.get_intensity_minutes_data.assert_called_once_with("2026-03-14")


@pytest.mark.asyncio
async def test_get_floors(mock_garmin):
    mock_garmin.get_floors.return_value = {
        "floorsAscended": 8,
        "floorsDescended": 6,
        "floorValuesArray": [[1710391200000, 2]],
    }
    client = GarminClient(mock_garmin)
    result = await client.get_floors("2026-03-14")
    assert result["date"] == "2026-03-14"
    assert result["floors_ascended"] == 8
    assert result["floors_descended"] == 6
    assert len(result["floor_values_array"]) == 1
    mock_garmin.get_floors.assert_called_once_with("2026-03-14")


@pytest.mark.asyncio
async def test_get_hydration(mock_garmin):
    mock_garmin.get_hydration_data.return_value = {
        "valueInML": 1800.0,
        "goalInML": 2500.0,
        "dailyAverageMl": 1750.0,
    }
    client = GarminClient(mock_garmin)
    result = await client.get_hydration("2026-03-14")
    assert result["date"] == "2026-03-14"
    assert result["value_in_ml"] == 1800.0
    assert result["goal_in_ml"] == 2500.0
    mock_garmin.get_hydration_data.assert_called_once_with("2026-03-14")


@pytest.mark.asyncio
async def test_get_daily_events(mock_garmin):
    mock_garmin.get_all_day_events.return_value = [
        {"eventType": "SLEEP", "startTimestampGMT": "2026-03-13 22:30:00"},
        {"eventType": "ACTIVITY", "startTimestampGMT": "2026-03-14 07:00:00"},
    ]
    client = GarminClient(mock_garmin)
    result = await client.get_daily_events("2026-03-14")
    assert result["date"] == "2026-03-14"
    assert len(result["events"]) == 2
    mock_garmin.get_all_day_events.assert_called_once_with("2026-03-14")
