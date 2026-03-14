"""Tests for sleep client methods."""

import pytest

from garmin_mcp.client import GarminClient


@pytest.mark.asyncio
async def test_get_sleep_data_structured(mock_garmin):
    mock_garmin.get_sleep_data.return_value = {
        "dailySleepDTO": {
            "sleepScores": {"overall": {"value": 82, "qualifierKey": "GOOD"}},
            "sleepStartTimestampGMT": 1710370800000,
            "sleepEndTimestampGMT": 1710399600000,
            "sleepTimeSeconds": 28800,
            "deepSleepSeconds": 5400,
            "lightSleepSeconds": 14400,
            "remSleepSeconds": 7200,
            "awakeSleepSeconds": 1800,
        }
    }
    client = GarminClient(mock_garmin)
    result = await client.get_sleep_data("2026-03-14")
    assert result["date"] == "2026-03-14"
    assert result["sleep_score"] == 82
    assert result["sleep_start"] == 1710370800000
    assert result["sleep_end"] == 1710399600000
    assert result["duration_seconds"] == 28800
    assert result["deep_sleep_seconds"] == 5400
    assert result["light_sleep_seconds"] == 14400
    assert result["rem_sleep_seconds"] == 7200
    assert result["awake_seconds"] == 1800
    mock_garmin.get_sleep_data.assert_called_once_with("2026-03-14")


@pytest.mark.asyncio
async def test_get_sleep_data_missing_fields(mock_garmin):
    mock_garmin.get_sleep_data.return_value = {
        "dailySleepDTO": {
            "sleepScores": {"overall": {"value": 75}},
        }
    }
    client = GarminClient(mock_garmin)
    result = await client.get_sleep_data("2026-03-14")
    assert result["sleep_score"] == 75
    assert result["duration_seconds"] is None
    assert result["deep_sleep_seconds"] is None


@pytest.mark.asyncio
async def test_get_sleep_data_no_dto(mock_garmin):
    mock_garmin.get_sleep_data.return_value = {}
    client = GarminClient(mock_garmin)
    result = await client.get_sleep_data("2026-03-14")
    assert result["sleep_score"] is None
    assert result["duration_seconds"] is None


@pytest.mark.asyncio
async def test_get_sleep_data_raw(mock_garmin):
    raw_payload = {
        "dailySleepDTO": {"sleepTimeSeconds": 28800},
        "hrvData": [{"value": 45}],
        "sleepHeartRate": {"averageHR": 52},
    }
    mock_garmin.get_sleep_data.return_value = raw_payload
    client = GarminClient(mock_garmin)
    result = await client.get_sleep_data_raw("2026-03-14")
    assert result == raw_payload
    assert "hrvData" in result
    assert "dailySleepDTO" in result
    mock_garmin.get_sleep_data.assert_called_once_with("2026-03-14")
