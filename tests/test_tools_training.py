"""Tests for training tools — client methods for VO2 Max, readiness, HRV, etc."""

import pytest

from garmin_mcp.client import GarminClient


@pytest.mark.asyncio
async def test_get_vo2max(mock_garmin):
    mock_garmin.get_max_metrics.return_value = {
        "vo2MaxPreciseValue": 48.5,
        "fitnessAge": 32,
    }
    client = GarminClient(mock_garmin)
    result = await client.get_vo2max("2026-03-14")
    assert result["date"] == "2026-03-14"
    assert result["vo2max"] == 48.5
    assert result["fitness_age"] == 32
    mock_garmin.get_max_metrics.assert_called_once_with("2026-03-14")


@pytest.mark.asyncio
async def test_get_training_readiness(mock_garmin):
    mock_garmin.get_training_readiness.return_value = {
        "trainingReadinessScore": 72,
        "trainingReadinessLabel": "GOOD",
    }
    client = GarminClient(mock_garmin)
    result = await client.get_training_readiness("2026-03-14")
    assert result["date"] == "2026-03-14"
    assert result["score"] == 72
    assert result["level"] == "GOOD"


@pytest.mark.asyncio
async def test_get_training_status(mock_garmin):
    mock_garmin.get_training_status.return_value = {
        "trainingStatusPhaseType": "MAINTAINING",
        "trainingLoad": 450,
    }
    client = GarminClient(mock_garmin)
    result = await client.get_training_status("2026-03-14")
    assert result["date"] == "2026-03-14"
    assert result["status"] == "MAINTAINING"
    assert result["load"] == 450


@pytest.mark.asyncio
async def test_get_hrv(mock_garmin):
    mock_garmin.get_hrv_data.return_value = {
        "hrvValue": 45,
        "status": "BALANCED",
        "weeklyAvg": 42,
    }
    client = GarminClient(mock_garmin)
    result = await client.get_hrv("2026-03-14")
    assert result["date"] == "2026-03-14"
    assert result["hrv_value"] == 45
    assert result["status"] == "BALANCED"
    assert result["weekly_avg"] == 42


@pytest.mark.asyncio
async def test_get_endurance_score(mock_garmin):
    mock_garmin.get_endurance_score.return_value = {
        "overallScore": 65,
        "trend": "IMPROVING",
    }
    client = GarminClient(mock_garmin)
    result = await client.get_endurance_score("2026-03-01", "2026-03-14")
    assert result["start_date"] == "2026-03-01"
    assert result["end_date"] == "2026-03-14"
    assert result["score"] == 65
    assert result["trend"] == "IMPROVING"


@pytest.mark.asyncio
async def test_get_hill_score(mock_garmin):
    mock_garmin.get_hill_score.return_value = {"hillScore": 42}
    client = GarminClient(mock_garmin)
    result = await client.get_hill_score("2026-03-01", "2026-03-14")
    assert result["start_date"] == "2026-03-01"
    assert result["end_date"] == "2026-03-14"
    assert result["score"] == 42


@pytest.mark.asyncio
async def test_get_race_predictions(mock_garmin):
    mock_garmin.get_race_predictions.return_value = {
        "racePredictions": {
            "5K": 1320,
            "10K": 2760,
            "HALF_MARATHON": 5940,
            "MARATHON": 12600,
        }
    }
    client = GarminClient(mock_garmin)
    result = await client.get_race_predictions()
    assert result["5k"] == 1320
    assert result["10k"] == 2760
    assert result["half_marathon"] == 5940
    assert result["marathon"] == 12600


@pytest.mark.asyncio
async def test_get_fitness_age(mock_garmin):
    mock_garmin.get_fitnessage_data.return_value = {
        "fitnessAge": 32,
        "chronologicalAge": 38,
    }
    client = GarminClient(mock_garmin)
    result = await client.get_fitness_age("2026-03-14")
    assert result["date"] == "2026-03-14"
    assert result["fitness_age"] == 32
    assert result["chronological_age"] == 38


@pytest.mark.asyncio
async def test_get_personal_records(mock_garmin):
    mock_garmin.get_personal_records.return_value = [
        {"activityType": "running", "value": 5000, "unit": "m"},
    ]
    client = GarminClient(mock_garmin)
    result = await client.get_personal_records()
    assert "records" in result
    assert len(result["records"]) == 1


@pytest.mark.asyncio
async def test_get_personal_records_non_list(mock_garmin):
    mock_garmin.get_personal_records.return_value = {}
    client = GarminClient(mock_garmin)
    result = await client.get_personal_records()
    assert result["records"] == []


@pytest.mark.asyncio
async def test_get_lactate_threshold(mock_garmin):
    mock_garmin.get_lactate_threshold.return_value = {
        "ltHeartRate": 162,
        "ltPaceSeconds": 285,
        "ltLevel": "THRESHOLD",
    }
    client = GarminClient(mock_garmin)
    result = await client.get_lactate_threshold()
    assert result["heart_rate"] == 162
    assert result["pace"] == 285
    assert result["level"] == "THRESHOLD"


@pytest.mark.asyncio
async def test_get_cycling_ftp(mock_garmin):
    mock_garmin.get_cycling_ftp.return_value = {
        "ftpValue": 240,
        "autoFtpValue": 235,
    }
    client = GarminClient(mock_garmin)
    result = await client.get_cycling_ftp()
    assert result["ftp"] == 240
    assert result["ftp_auto_detected"] == 235
