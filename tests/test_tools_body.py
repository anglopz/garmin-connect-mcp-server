"""Tests for body composition client methods."""

import pytest

from garmin_mcp.client import GarminClient


@pytest.mark.asyncio
async def test_get_body_composition(mock_garmin):
    mock_garmin.get_body_composition.return_value = {
        "dateWeightList": [
            {"calendarDate": "2026-03-14", "weight": 75.0, "bmi": 23.1, "bodyFat": 18.5}
        ]
    }
    client = GarminClient(mock_garmin)
    result = await client.get_body_composition("2026-03-01", "2026-03-14")
    assert "dateWeightList" in result
    mock_garmin.get_body_composition.assert_called_once_with("2026-03-01", "2026-03-14")


@pytest.mark.asyncio
async def test_get_latest_weight_with_entries(mock_garmin):
    mock_garmin.get_body_composition.return_value = {
        "dateWeightList": [
            {
                "calendarDate": "2026-03-10",
                "weight": 76.0,
                "bmi": 23.4,
                "bodyFat": 19.0,
                "muscleMass": 60.0,
            },
            {
                "calendarDate": "2026-03-14",
                "weight": 75.5,
                "bmi": 23.2,
                "bodyFat": 18.8,
                "muscleMass": 60.2,
            },
        ]
    }
    client = GarminClient(mock_garmin)
    result = await client.get_latest_weight()
    assert result["date"] == "2026-03-14"
    assert result["weight_kg"] == 75.5
    assert result["bmi"] == 23.2
    assert result["body_fat_percent"] == 18.8
    assert result["muscle_mass_kg"] == 60.2


@pytest.mark.asyncio
async def test_get_latest_weight_no_entries(mock_garmin):
    mock_garmin.get_body_composition.return_value = {"dateWeightList": []}
    client = GarminClient(mock_garmin)
    result = await client.get_latest_weight()
    assert "error" in result


@pytest.mark.asyncio
async def test_get_daily_weigh_ins(mock_garmin):
    mock_garmin.get_daily_weigh_ins.return_value = {
        "calendarDate": "2026-03-14",
        "allWeightMetrics": [{"weight": 75.5, "bmi": 23.2}],
    }
    client = GarminClient(mock_garmin)
    result = await client.get_daily_weigh_ins("2026-03-14")
    assert result["calendarDate"] == "2026-03-14"
    mock_garmin.get_daily_weigh_ins.assert_called_once_with("2026-03-14")


@pytest.mark.asyncio
async def test_get_weigh_ins(mock_garmin):
    mock_garmin.get_weigh_ins.return_value = {
        "dateWeightList": [
            {"calendarDate": "2026-03-14", "weight": 75.5},
        ]
    }
    client = GarminClient(mock_garmin)
    result = await client.get_weigh_ins("2026-03-01", "2026-03-14")
    assert "dateWeightList" in result
    mock_garmin.get_weigh_ins.assert_called_once_with("2026-03-01", "2026-03-14")


@pytest.mark.asyncio
async def test_get_blood_pressure(mock_garmin):
    mock_garmin.get_blood_pressure.return_value = {
        "measurementSummaries": [{"systolic": 118, "diastolic": 76, "calendarDate": "2026-03-14"}]
    }
    client = GarminClient(mock_garmin)
    result = await client.get_blood_pressure("2026-03-01", "2026-03-14")
    assert "measurementSummaries" in result
    mock_garmin.get_blood_pressure.assert_called_once_with("2026-03-01", "2026-03-14")
