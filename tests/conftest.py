"""Shared test fixtures for Garmin Connect MCP server tests.

Provides mock Garmin instances and GarminClient instances that return
predictable test data without making network calls.
"""

from unittest.mock import MagicMock

import pytest

from garmin_mcp.client import GarminClient


@pytest.fixture
def mock_garmin() -> MagicMock:
    """Create a mock garminconnect.Garmin instance with common return values.

    Each test module should configure specific return values as needed.
    This provides a base mock with sensible defaults.
    """
    garmin = MagicMock()

    # Activities defaults
    garmin.get_activities.return_value = [
        {"activityId": 123, "activityName": "Morning Run", "startTimeLocal": "2026-03-14 07:00:00"}
    ]
    garmin.get_last_activity.return_value = {
        "activityId": 123,
        "activityName": "Morning Run",
    }

    # Health defaults
    garmin.get_user_summary.return_value = {
        "totalSteps": 8500,
        "totalDistanceMeters": 6200.0,
        "activeKilocalories": 450,
    }
    garmin.get_heart_rates.return_value = {
        "restingHeartRate": 52,
        "maxHeartRate": 165,
        "heartRateZones": [],
        "heartRateValues": [],
    }
    garmin.get_all_day_stress.return_value = {
        "overallStressLevel": 32,
        "stressValuesArray": [],
    }

    # Sleep defaults
    garmin.get_sleep_data.return_value = {
        "sleepScore": 82,
        "sleepStartTimestamp": 1710370800000,
        "sleepEndTimestamp": 1710399600000,
    }

    # Training defaults
    garmin.get_max_metrics.return_value = {
        "vo2MaxPreciseValue": 48.5,
    }
    garmin.get_training_readiness.return_value = {
        "trainingReadinessScore": 72,
    }
    garmin.get_hrv_data.return_value = {
        "hrvValue": 45,
        "status": "BALANCED",
    }

    # Profile defaults
    garmin.get_user_profile.return_value = {
        "displayName": "TestUser",
        "userName": "testuser",
    }
    garmin.get_devices.return_value = [
        {"deviceId": "abc123", "deviceName": "Fenix 8 AMOLED"},
    ]

    return garmin


@pytest.fixture
def garmin_client(mock_garmin: MagicMock) -> GarminClient:
    """Create a GarminClient backed by the mock Garmin instance."""
    return GarminClient(mock_garmin)
