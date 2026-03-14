"""Tests for training tools — client methods for VO2 Max, readiness, HRV, etc."""

import pytest

from garmin_mcp.client import GarminClient


@pytest.mark.asyncio
async def test_get_vo2max(mock_garmin):
    mock_garmin.get_max_metrics.return_value = [
        {
            "generic": {"vo2MaxPreciseValue": 45.3, "fitnessAge": None},
            "cycling": None,
        }
    ]
    client = GarminClient(mock_garmin)
    result = await client.get_vo2max("2026-03-14")
    assert result["date"] == "2026-03-14"
    assert result["vo2max_running"] == 45.3
    assert result["vo2max_cycling"] is None
    mock_garmin.get_max_metrics.assert_called_once_with("2026-03-14")


@pytest.mark.asyncio
async def test_get_vo2max_empty_list(mock_garmin):
    mock_garmin.get_max_metrics.return_value = []
    client = GarminClient(mock_garmin)
    result = await client.get_vo2max("2026-03-14")
    assert result["vo2max_running"] is None
    assert result["vo2max_cycling"] is None


@pytest.mark.asyncio
async def test_get_training_readiness(mock_garmin):
    mock_garmin.get_training_readiness.return_value = [
        {
            "score": 60,
            "level": "MODERATE",
            "sleepScore": 60,
            "recoveryTime": 1,
            "hrvWeeklyAverage": 66,
            "feedbackShort": "GOOD_SLEEP_HISTORY",
        },
    ]
    client = GarminClient(mock_garmin)
    result = await client.get_training_readiness("2026-03-14")
    assert result["date"] == "2026-03-14"
    assert result["score"] == 60
    assert result["level"] == "MODERATE"
    assert result["sleep_score"] == 60
    assert result["feedback"] == "GOOD_SLEEP_HISTORY"


@pytest.mark.asyncio
async def test_get_training_readiness_empty(mock_garmin):
    mock_garmin.get_training_readiness.return_value = []
    client = GarminClient(mock_garmin)
    result = await client.get_training_readiness("2026-03-14")
    assert result["score"] is None
    assert result["level"] is None


@pytest.mark.asyncio
async def test_get_training_status(mock_garmin):
    mock_garmin.get_training_status.return_value = {
        "mostRecentTrainingStatus": {
            "latestTrainingStatusData": {
                "3509549590": {
                    "trainingStatus": 7,
                    "trainingStatusFeedbackPhrase": "PRODUCTIVE_6",
                    "fitnessTrend": 2,
                    "acuteTrainingLoadDTO": {
                        "dailyTrainingLoadAcute": 358,
                        "dailyTrainingLoadChronic": 197,
                        "dailyAcuteChronicWorkloadRatio": 1.8,
                    },
                    "primaryTrainingDevice": True,
                }
            }
        },
        "mostRecentVO2Max": {
            "generic": {"vo2MaxPreciseValue": 45.3},
        },
    }
    client = GarminClient(mock_garmin)
    result = await client.get_training_status("2026-03-14")
    assert result["date"] == "2026-03-14"
    assert result["training_status"] == 7
    assert result["training_status_feedback"] == "PRODUCTIVE_6"
    assert result["acute_load"] == 358
    assert result["chronic_load"] == 197
    assert result["acwr_ratio"] == 1.8
    assert result["vo2max"] == 45.3


@pytest.mark.asyncio
async def test_get_hrv(mock_garmin):
    mock_garmin.get_hrv_data.return_value = {
        "hrvSummary": {
            "lastNightAvg": 68,
            "lastNight5MinHigh": 99,
            "status": "BALANCED",
            "weeklyAvg": 66,
            "baseline": {"lowUpper": 62, "balancedLow": 65, "balancedUpper": 80},
            "feedbackPhrase": "HRV_BALANCED_7",
        },
        "hrvReadings": [{"hrvValue": 61}],
    }
    client = GarminClient(mock_garmin)
    result = await client.get_hrv("2026-03-14")
    assert result["date"] == "2026-03-14"
    assert result["last_night_avg"] == 68
    assert result["last_night_5min_high"] == 99
    assert result["status"] == "BALANCED"
    assert result["weekly_avg"] == 66
    assert result["feedback"] == "HRV_BALANCED_7"


@pytest.mark.asyncio
async def test_get_endurance_score(mock_garmin):
    mock_garmin.get_endurance_score.return_value = {
        "avg": 4933,
        "max": 5033,
        "enduranceScoreDTO": {
            "overallScore": 5033,
            "classification": 1,
        },
    }
    client = GarminClient(mock_garmin)
    result = await client.get_endurance_score("2026-03-01", "2026-03-14")
    assert result["start_date"] == "2026-03-01"
    assert result["end_date"] == "2026-03-14"
    assert result["overall_score"] == 5033
    assert result["classification"] == 1
    assert result["period_avg"] == 4933
    assert result["period_max"] == 5033


@pytest.mark.asyncio
async def test_get_hill_score(mock_garmin):
    mock_garmin.get_hill_score.return_value = {
        "maxScore": 15,
        "hillScoreDTOList": [
            {
                "overallScore": 15,
                "strengthScore": 8,
                "enduranceScore": 1,
            }
        ],
    }
    client = GarminClient(mock_garmin)
    result = await client.get_hill_score("2026-03-01", "2026-03-14")
    assert result["start_date"] == "2026-03-01"
    assert result["end_date"] == "2026-03-14"
    assert result["overall_score"] == 15
    assert result["strength_score"] == 8
    assert result["endurance_score"] == 1
    assert result["max_score"] == 15


@pytest.mark.asyncio
async def test_get_hill_score_empty(mock_garmin):
    mock_garmin.get_hill_score.return_value = {
        "maxScore": None,
        "hillScoreDTOList": [],
    }
    client = GarminClient(mock_garmin)
    result = await client.get_hill_score("2026-03-01", "2026-03-14")
    assert result["overall_score"] is None


@pytest.mark.asyncio
async def test_get_race_predictions(mock_garmin):
    mock_garmin.get_race_predictions.return_value = {
        "time5K": 1634,
        "time10K": 3579,
        "timeHalfMarathon": 8304,
        "timeMarathon": 19024,
    }
    client = GarminClient(mock_garmin)
    result = await client.get_race_predictions()
    assert result["5k_seconds"] == 1634
    assert result["10k_seconds"] == 3579
    assert result["half_marathon_seconds"] == 8304
    assert result["marathon_seconds"] == 19024


@pytest.mark.asyncio
async def test_get_fitness_age(mock_garmin):
    mock_garmin.get_fitnessage_data.return_value = {
        "fitnessAge": 21.95,
        "chronologicalAge": 26,
    }
    client = GarminClient(mock_garmin)
    result = await client.get_fitness_age("2026-03-14")
    assert result["date"] == "2026-03-14"
    assert result["fitness_age"] == 21.95
    assert result["chronological_age"] == 26


@pytest.mark.asyncio
async def test_get_personal_records(mock_garmin):
    mock_garmin.get_personal_record.return_value = [
        {"typeId": 1, "activityType": "running", "value": 307.087},
    ]
    client = GarminClient(mock_garmin)
    result = await client.get_personal_records()
    assert "records" in result
    assert len(result["records"]) == 1


@pytest.mark.asyncio
async def test_get_personal_records_non_list(mock_garmin):
    mock_garmin.get_personal_record.return_value = {}
    client = GarminClient(mock_garmin)
    result = await client.get_personal_records()
    assert result["records"] == []


@pytest.mark.asyncio
async def test_get_lactate_threshold(mock_garmin):
    mock_garmin.get_lactate_threshold.return_value = {
        "speed_and_heart_rate": {
            "heartRate": 175,
            "speed": 0.30277693,
        },
        "power": {
            "functionalThresholdPower": 326,
            "sport": "RUNNING",
        },
    }
    client = GarminClient(mock_garmin)
    result = await client.get_lactate_threshold()
    assert result["heart_rate"] == 175
    assert result["speed"] == 0.30277693
    assert result["running_ftp"] == 326
    assert result["sport"] == "RUNNING"


@pytest.mark.asyncio
async def test_get_cycling_ftp(mock_garmin):
    mock_garmin.get_cycling_ftp.return_value = {
        "functionalThresholdPower": 208,
        "sport": "CYCLING",
        "isStale": False,
    }
    client = GarminClient(mock_garmin)
    result = await client.get_cycling_ftp()
    assert result["ftp"] == 208
    assert result["sport"] == "CYCLING"
    assert result["is_stale"] is False
