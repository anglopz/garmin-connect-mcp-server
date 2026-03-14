"""Tests for Fenix 8 AMOLED tools — running dynamics, training effect, power, etc."""

import pytest

from garmin_mcp.client import GarminClient


@pytest.mark.asyncio
async def test_get_running_dynamics(mock_garmin):
    mock_garmin.get_activity.return_value = {
        "activityId": 12345,
        "averageRunningCadenceInStepsPerMinute": 170.0,
        "maxRunningCadenceInStepsPerMinute": 185.0,
        "avgGroundContactTime": 245.5,
        "avgStrideLength": 1.12,
        "avgVerticalOscillation": 8.3,
        "avgGroundContactBalance": 49.8,
    }
    client = GarminClient(mock_garmin)
    result = await client.get_running_dynamics("12345")
    assert result["activity_id"] == "12345"
    assert result["avg_cadence"] == 170.0
    assert result["max_cadence"] == 185.0
    assert result["avg_ground_contact_time_ms"] == 245.5
    assert result["avg_stride_length_m"] == 1.12
    assert result["avg_vertical_oscillation_cm"] == 8.3
    assert result["avg_ground_contact_balance"] == 49.8
    mock_garmin.get_activity.assert_called_once_with("12345")


@pytest.mark.asyncio
async def test_get_training_effect(mock_garmin):
    mock_garmin.get_activity.return_value = {
        "activityId": 12345,
        "aerobicTrainingEffect": 3.2,
        "anaerobicTrainingEffect": 1.8,
        "aerobicTrainingEffectMessage": "Improving",
        "anaerobicTrainingEffectMessage": "Minor",
    }
    client = GarminClient(mock_garmin)
    result = await client.get_training_effect("12345")
    assert result["activity_id"] == "12345"
    assert result["aerobic_training_effect"] == 3.2
    assert result["anaerobic_training_effect"] == 1.8
    assert result["aerobic_effect_message"] == "Improving"
    assert result["anaerobic_effect_message"] == "Minor"
    mock_garmin.get_activity.assert_called_once_with("12345")


@pytest.mark.asyncio
async def test_get_activity_power_zones(mock_garmin):
    mock_garmin.get_activity_power_in_timezones.return_value = [
        {"zone": 1, "secsInZone": 120},
        {"zone": 2, "secsInZone": 300},
    ]
    client = GarminClient(mock_garmin)
    result = await client.get_activity_power_zones("12345")
    assert result["activity_id"] == "12345"
    assert len(result["power_zones"]) == 2
    assert result["power_zones"][0]["zone"] == 1
    mock_garmin.get_activity_power_in_timezones.assert_called_once_with("12345")


@pytest.mark.asyncio
async def test_get_activity_power_zones_non_list(mock_garmin):
    mock_garmin.get_activity_power_in_timezones.return_value = {}
    client = GarminClient(mock_garmin)
    result = await client.get_activity_power_zones("12345")
    assert result["power_zones"] == []


@pytest.mark.asyncio
async def test_get_running_power(mock_garmin):
    mock_garmin.get_activity.return_value = {
        "activityId": 12345,
        "avgPower": 245.0,
        "maxPower": 380.0,
        "normPower": 260.0,
        "minPower": 120.0,
    }
    client = GarminClient(mock_garmin)
    result = await client.get_running_power("12345")
    assert result["activity_id"] == "12345"
    assert result["avg_power_watts"] == 245.0
    assert result["max_power_watts"] == 380.0
    assert result["normalized_power_watts"] == 260.0
    assert result["min_power_watts"] == 120.0
    mock_garmin.get_activity.assert_called_once_with("12345")


@pytest.mark.asyncio
async def test_get_climbpro_data(mock_garmin):
    mock_garmin.get_activity_split_summaries.return_value = {
        "splitSummaries": [
            {"splitType": "CLIMB", "distance": 1200, "elevationGain": 150},
        ]
    }
    client = GarminClient(mock_garmin)
    result = await client.get_climbpro_data("12345")
    assert result["activity_id"] == "12345"
    assert len(result["split_summaries"]) == 1
    assert result["split_summaries"][0]["splitType"] == "CLIMB"
    mock_garmin.get_activity_split_summaries.assert_called_once_with("12345")


@pytest.mark.asyncio
async def test_get_climbpro_data_non_dict(mock_garmin):
    mock_garmin.get_activity_split_summaries.return_value = []
    client = GarminClient(mock_garmin)
    result = await client.get_climbpro_data("12345")
    assert result["split_summaries"] == []


@pytest.mark.asyncio
async def test_get_activity_typed_splits(mock_garmin):
    mock_garmin.get_activity_typed_splits.return_value = {
        "typedSplits": [
            {"splitType": "RUN", "distance": 5000, "duration": 1500},
        ]
    }
    client = GarminClient(mock_garmin)
    result = await client.get_activity_typed_splits("12345")
    assert result["activity_id"] == "12345"
    assert len(result["typed_splits"]) == 1
    assert result["typed_splits"][0]["splitType"] == "RUN"
    mock_garmin.get_activity_typed_splits.assert_called_once_with("12345")


@pytest.mark.asyncio
async def test_get_activity_typed_splits_non_dict(mock_garmin):
    mock_garmin.get_activity_typed_splits.return_value = []
    client = GarminClient(mock_garmin)
    result = await client.get_activity_typed_splits("12345")
    assert result["typed_splits"] == []


@pytest.mark.asyncio
async def test_get_morning_readiness(mock_garmin):
    mock_garmin.get_morning_training_readiness.return_value = {
        "morningReadinessScore": 68,
        "morningReadinessLevel": "MODERATE",
        "sleepScore": 75,
        "hrvStatus": "BALANCED",
    }
    client = GarminClient(mock_garmin)
    result = await client.get_morning_readiness("2026-03-14")
    assert result["date"] == "2026-03-14"
    assert result["score"] == 68
    assert result["level"] == "MODERATE"
    assert result["sleep_score"] == 75
    assert result["hrv_status"] == "BALANCED"
    mock_garmin.get_morning_training_readiness.assert_called_once_with("2026-03-14")
