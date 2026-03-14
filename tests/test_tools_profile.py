"""Tests for GarminClient profile methods."""

import pytest

from garmin_mcp.client import GarminClient


@pytest.mark.asyncio
async def test_get_user_profile(garmin_client: GarminClient, mock_garmin):
    result = await garmin_client.get_user_profile()
    assert result["displayName"] == "TestUser"
    mock_garmin.get_user_profile.assert_called_once()


@pytest.mark.asyncio
async def test_get_user_settings(garmin_client: GarminClient, mock_garmin):
    mock_garmin.get_userprofile_settings.return_value = {"measurementSystem": "METRIC"}
    result = await garmin_client.get_user_settings()
    assert result["measurementSystem"] == "METRIC"
    mock_garmin.get_userprofile_settings.assert_called_once()


@pytest.mark.asyncio
async def test_get_devices(garmin_client: GarminClient, mock_garmin):
    result = await garmin_client.get_devices()
    assert len(result) == 1
    assert result[0]["deviceName"] == "Fenix 8 AMOLED"
    mock_garmin.get_devices.assert_called_once()


@pytest.mark.asyncio
async def test_get_device_settings(garmin_client: GarminClient, mock_garmin):
    mock_garmin.get_device_settings.return_value = {"deviceId": "abc123", "gpsMode": "GPS"}
    result = await garmin_client.get_device_settings("abc123")
    assert result["deviceId"] == "abc123"
    mock_garmin.get_device_settings.assert_called_once_with("abc123")


@pytest.mark.asyncio
async def test_get_device_last_used(garmin_client: GarminClient, mock_garmin):
    mock_garmin.get_device_last_used.return_value = {
        "deviceId": "abc123",
        "userProfileNumber": 42,
    }
    result = await garmin_client.get_device_last_used()
    assert result["userProfileNumber"] == 42
    mock_garmin.get_device_last_used.assert_called_once()


@pytest.mark.asyncio
async def test_get_primary_training_device(garmin_client: GarminClient, mock_garmin):
    mock_garmin.get_primary_training_device.return_value = {"deviceId": "abc123"}
    result = await garmin_client.get_primary_training_device()
    assert result["deviceId"] == "abc123"
    mock_garmin.get_primary_training_device.assert_called_once()


@pytest.mark.asyncio
async def test_get_gear(garmin_client: GarminClient, mock_garmin):
    mock_garmin.get_device_last_used.return_value = {"userProfileNumber": 42}
    mock_garmin.get_gear.return_value = [{"gearUuid": "shoe-uuid", "displayName": "Trail Shoes"}]
    result = await garmin_client.get_gear()
    assert len(result) == 1
    assert result[0]["displayName"] == "Trail Shoes"
    mock_garmin.get_gear.assert_called_once_with(42)


@pytest.mark.asyncio
async def test_get_gear_stats(garmin_client: GarminClient, mock_garmin):
    mock_garmin.get_gear_stats.return_value = {"totalDistance": 250000, "gearUuid": "shoe-uuid"}
    result = await garmin_client.get_gear_stats("shoe-uuid")
    assert result["totalDistance"] == 250000
    mock_garmin.get_gear_stats.assert_called_once_with("shoe-uuid")


@pytest.mark.asyncio
async def test_get_goals(garmin_client: GarminClient, mock_garmin):
    mock_garmin.get_active_goals.return_value = [{"goalType": "STEPS", "goalValue": 10000}]
    result = await garmin_client.get_goals()
    assert len(result) == 1
    assert result[0]["goalType"] == "STEPS"
    mock_garmin.get_active_goals.assert_called_once()


@pytest.mark.asyncio
async def test_get_earned_badges(garmin_client: GarminClient, mock_garmin):
    mock_garmin.get_earned_badges.return_value = [{"badgeName": "5K Finisher"}]
    result = await garmin_client.get_earned_badges()
    assert len(result) == 1
    assert result[0]["badgeName"] == "5K Finisher"
    mock_garmin.get_earned_badges.assert_called_once()


@pytest.mark.asyncio
async def test_get_workouts(garmin_client: GarminClient, mock_garmin):
    mock_garmin.get_workouts.return_value = [{"workoutId": 1, "workoutName": "Easy Run"}]
    result = await garmin_client.get_workouts()
    assert len(result) == 1
    assert result[0]["workoutName"] == "Easy Run"
    mock_garmin.get_workouts.assert_called_once()


@pytest.mark.asyncio
async def test_get_workout(garmin_client: GarminClient, mock_garmin):
    mock_garmin.get_workout_by_id.return_value = {"workoutId": 1, "workoutName": "Easy Run"}
    result = await garmin_client.get_workout("1")
    assert result["workoutName"] == "Easy Run"
    mock_garmin.get_workout_by_id.assert_called_once_with("1")


@pytest.mark.asyncio
async def test_get_activity_gear(garmin_client: GarminClient, mock_garmin):
    mock_garmin.get_activity_gear.return_value = {
        "gearUuid": "shoe-uuid",
        "displayName": "Trail Shoes",
    }
    result = await garmin_client.get_activity_gear("123")
    assert result["displayName"] == "Trail Shoes"
    mock_garmin.get_activity_gear.assert_called_once_with("123")
