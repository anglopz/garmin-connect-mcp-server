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
    mock_garmin.get_user_summary.return_value = {
        "totalSteps": 10234,
        "dailyStepGoal": 10000,
    }
    client = GarminClient(mock_garmin)
    result = await client.get_steps("2026-03-14")
    assert result["date"] == "2026-03-14"
    assert result["total_steps"] == 10234
    assert result["step_goal"] == 10000
    mock_garmin.get_user_summary.assert_called_with("2026-03-14")


@pytest.mark.asyncio
async def test_get_steps_chart(mock_garmin):
    mock_garmin.get_steps_data.return_value = [
        {"startGMT": "2026-03-14 08:00:00", "steps": 500},
    ]
    client = GarminClient(mock_garmin)
    result = await client.get_steps_chart("2026-03-14")
    assert result["date"] == "2026-03-14"
    assert len(result["time_series"]) == 1
    assert result["time_series"][0]["steps"] == 500


@pytest.mark.asyncio
async def test_get_heart_rate(mock_garmin):
    mock_garmin.get_heart_rates.return_value = {
        "restingHeartRate": 47,
        "minHeartRate": 43,
        "maxHeartRate": 187,
        "lastSevenDaysAvgRestingHeartRate": 47,
        "heartRateValues": [[1773442800000, 62]],
    }
    client = GarminClient(mock_garmin)
    result = await client.get_heart_rate("2026-03-14")
    assert result["date"] == "2026-03-14"
    assert result["resting_heart_rate"] == 47
    assert result["min_heart_rate"] == 43
    assert result["max_heart_rate"] == 187
    assert result["last_seven_days_avg_resting_heart_rate"] == 47
    assert len(result["time_series"]) == 1
    assert "heart_rate_zones" not in result
    mock_garmin.get_heart_rates.assert_called_once_with("2026-03-14")


@pytest.mark.asyncio
async def test_get_resting_heart_rate(mock_garmin):
    mock_garmin.get_rhr_day.return_value = {
        "allMetrics": {"metricsMap": {"WELLNESS_RESTING_HEART_RATE": [{"value": 47.0}]}}
    }
    client = GarminClient(mock_garmin)
    result = await client.get_resting_heart_rate("2026-03-14")
    assert result["date"] == "2026-03-14"
    assert result["resting_heart_rate"] == 47.0
    assert result["value"] == 47.0
    mock_garmin.get_rhr_day.assert_called_once_with("2026-03-14")


@pytest.mark.asyncio
async def test_get_resting_heart_rate_missing_metrics(mock_garmin):
    mock_garmin.get_rhr_day.return_value = {}
    client = GarminClient(mock_garmin)
    result = await client.get_resting_heart_rate("2026-03-14")
    assert result["date"] == "2026-03-14"
    assert result["resting_heart_rate"] is None


@pytest.mark.asyncio
async def test_get_stress(mock_garmin):
    mock_garmin.get_all_day_stress.return_value = {
        "avgStressLevel": 22,
        "maxStressLevel": 97,
        "restStressDuration": 45600,
        "lowStressDuration": 13320,
        "mediumStressDuration": 3180,
        "highStressDuration": 1800,
        "stressQualifier": "BALANCED",
        "stressValuesArray": [[1773442800000, 25]],
    }
    client = GarminClient(mock_garmin)
    result = await client.get_stress("2026-03-14")
    assert result["date"] == "2026-03-14"
    assert result["avg_stress_level"] == 22
    assert result["max_stress_level"] == 97
    assert result["rest_stress_duration"] == 45600
    assert result["stress_qualifier"] == "BALANCED"
    assert len(result["stress_values"]) == 1
    assert "overall_stress_level" not in result
    mock_garmin.get_all_day_stress.assert_called_once_with("2026-03-14")


@pytest.mark.asyncio
async def test_get_body_battery(mock_garmin):
    mock_garmin.get_body_battery.return_value = [
        {"date": "2026-03-14", "charged": 57, "drained": 76},
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
        {
            "event": {
                "eventType": "SLEEP",
                "eventStartTimeGmt": "2026-03-14T00:08:29.0",
                "bodyBatteryImpact": 49,
            },
        },
    ]
    client = GarminClient(mock_garmin)
    result = await client.get_body_battery_events("2026-03-14")
    assert result["date"] == "2026-03-14"
    assert len(result["events"]) == 1
    mock_garmin.get_body_battery_events.assert_called_once_with("2026-03-14")


@pytest.mark.asyncio
async def test_get_respiration(mock_garmin):
    mock_garmin.get_respiration_data.return_value = {
        "avgWakingRespirationValue": 14.0,
        "highestRespirationValue": 21.0,
        "lowestRespirationValue": 7.0,
        "avgSleepRespirationValue": 14.0,
        "respirationValuesArray": [[1773442920000, 13.0]],
    }
    client = GarminClient(mock_garmin)
    result = await client.get_respiration("2026-03-14")
    assert result["date"] == "2026-03-14"
    assert result["avg_waking_respiration_value"] == 14.0
    assert result["highest_respiration_value"] == 21.0
    assert result["lowest_respiration_value"] == 7.0
    assert len(result["respiration_values"]) == 1
    mock_garmin.get_respiration_data.assert_called_once_with("2026-03-14")


@pytest.mark.asyncio
async def test_get_spo2(mock_garmin):
    mock_garmin.get_spo2_data.return_value = {
        "averageSpO2": None,
        "lowestSpO2": 88,
        "latestSpO2": 88,
        "spO2SingleValues": [[1773524760000, 88, True]],
        "continuousReadingDTOList": None,
    }
    client = GarminClient(mock_garmin)
    result = await client.get_spo2("2026-03-14")
    assert result["date"] == "2026-03-14"
    assert result["avg_spo2"] is None
    assert result["lowest_spo2"] == 88
    assert result["latest_spo2"] == 88
    assert len(result["spo2_single_values"]) == 1
    assert result["continuous_reading_list"] == []
    assert "on_demand_reading_list" not in result
    mock_garmin.get_spo2_data.assert_called_once_with("2026-03-14")


@pytest.mark.asyncio
async def test_get_intensity_minutes(mock_garmin):
    mock_garmin.get_intensity_minutes_data.return_value = {
        "moderateMinutes": 53,
        "vigorousMinutes": 29,
        "weeklyModerate": 128,
        "weeklyVigorous": 41,
        "weeklyTotal": 210,
        "weekGoal": 150,
    }
    client = GarminClient(mock_garmin)
    result = await client.get_intensity_minutes("2026-03-14")
    assert result["date"] == "2026-03-14"
    assert result["moderate_minutes"] == 53
    assert result["vigorous_minutes"] == 29
    assert result["weekly_moderate"] == 128
    assert result["weekly_vigorous"] == 41
    assert result["weekly_total"] == 210
    assert result["week_goal"] == 150
    mock_garmin.get_intensity_minutes_data.assert_called_once_with("2026-03-14")


@pytest.mark.asyncio
async def test_get_floors(mock_garmin):
    mock_garmin.get_floors.return_value = {
        "floorValuesArray": [
            ["2026-03-14T08:00:00.0", "2026-03-14T08:15:00.0", 2, 0],
        ],
    }
    client = GarminClient(mock_garmin)
    result = await client.get_floors("2026-03-14")
    assert result["date"] == "2026-03-14"
    assert len(result["floor_values_array"]) == 1
    assert "floors_ascended" not in result
    assert "floors_descended" not in result
    mock_garmin.get_floors.assert_called_once_with("2026-03-14")


@pytest.mark.asyncio
async def test_get_hydration(mock_garmin):
    mock_garmin.get_hydration_data.return_value = {
        "valueInML": 0.0,
        "goalInML": 3917.056,
        "dailyAverageinML": None,
        "sweatLossInML": 1078.0,
    }
    client = GarminClient(mock_garmin)
    result = await client.get_hydration("2026-03-14")
    assert result["date"] == "2026-03-14"
    assert result["value_in_ml"] == 0.0
    assert result["goal_in_ml"] == 3917.056
    assert result["daily_average_in_ml"] is None
    assert result["sweat_loss_in_ml"] == 1078.0
    mock_garmin.get_hydration_data.assert_called_once_with("2026-03-14")


@pytest.mark.asyncio
async def test_get_daily_events(mock_garmin):
    mock_garmin.get_all_day_events.return_value = [
        {
            "calendarDate": "2026-03-14",
            "activityType": "running",
            "duration": 19,
            "moderateIntensityMinutes": 6,
            "vigorousIntensityMinutes": 12,
        },
    ]
    client = GarminClient(mock_garmin)
    result = await client.get_daily_events("2026-03-14")
    assert result["date"] == "2026-03-14"
    assert len(result["events"]) == 1
    mock_garmin.get_all_day_events.assert_called_once_with("2026-03-14")
