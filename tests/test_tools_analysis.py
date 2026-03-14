"""Tests for analysis tools — compare, find similar, period analysis."""

import pytest

from garmin_mcp.client import GarminClient


@pytest.mark.asyncio
async def test_compare_activities(mock_garmin):
    mock_garmin.get_activity.side_effect = [
        {
            "activityName": "Morning Run",
            "distance": 5000.0,
            "duration": 1500,
            "averageHR": 155,
            "averageSpeed": 3.33,
        },
        {
            "activityName": "Evening Run",
            "distance": 10000.0,
            "duration": 3200,
            "averageHR": 162,
            "averageSpeed": 3.12,
        },
    ]
    client = GarminClient(mock_garmin)
    result = await client.compare_activities(["111", "222"])
    assert result["count"] == 2
    assert len(result["activities"]) == 2
    assert result["activities"][0]["id"] == "111"
    assert result["activities"][0]["distance"] == 5000.0
    assert result["activities"][1]["id"] == "222"
    assert result["activities"][1]["average_hr"] == 162


@pytest.mark.asyncio
async def test_compare_activities_empty(mock_garmin):
    client = GarminClient(mock_garmin)
    result = await client.compare_activities([])
    assert result["count"] == 0
    assert result["activities"] == []


@pytest.mark.asyncio
async def test_find_similar_activities(mock_garmin):
    ref_activity = {
        "activityId": 100,
        "activityType": {"typeKey": "running"},
        "distance": 5000.0,
    }
    mock_garmin.get_activity.return_value = ref_activity
    mock_garmin.get_activities.return_value = [
        {
            "activityId": 200,
            "activityType": {"typeKey": "running"},
            "distance": 5100.0,
        },
        {
            "activityId": 300,
            "activityType": {"typeKey": "cycling"},
            "distance": 20000.0,
        },
        {
            "activityId": 400,
            "activityType": {"typeKey": "running"},
            "distance": 10000.0,
        },
        {
            "activityId": 100,  # same as ref, should be excluded
            "activityType": {"typeKey": "running"},
            "distance": 5000.0,
        },
    ]
    client = GarminClient(mock_garmin)
    result = await client.find_similar_activities("100", limit=5)
    # Should return only running activities (not cycling, not the ref itself)
    assert isinstance(result, list)
    ids = [str(a["activityId"]) for a in result]
    assert "100" not in ids  # ref excluded
    assert all(
        a["activityType"]["typeKey"] == "running" for a in result
    )  # only same type
    # Closest distance first: 200 (5100) then 400 (10000)
    assert result[0]["activityId"] == 200


@pytest.mark.asyncio
async def test_find_similar_activities_limit(mock_garmin):
    ref_activity = {
        "activityId": 1,
        "activityType": {"typeKey": "running"},
        "distance": 5000.0,
    }
    mock_garmin.get_activity.return_value = ref_activity
    mock_garmin.get_activities.return_value = [
        {"activityId": i, "activityType": {"typeKey": "running"}, "distance": 5000.0 + i * 100}
        for i in range(2, 12)  # 10 candidates
    ]
    client = GarminClient(mock_garmin)
    result = await client.find_similar_activities("1", limit=3)
    assert len(result) <= 3


@pytest.mark.asyncio
async def test_analyze_training_period(mock_garmin):
    mock_garmin.get_activities_by_date.return_value = [
        {
            "activityType": {"typeKey": "running"},
            "distance": 5000.0,
            "averageHR": 155,
        },
        {
            "activityType": {"typeKey": "running"},
            "distance": 10000.0,
            "averageHR": 160,
        },
        {
            "activityType": {"typeKey": "cycling"},
            "distance": 30000.0,
            "averageHR": None,
        },
    ]
    client = GarminClient(mock_garmin)
    result = await client.analyze_training_period("2026-03-01", "2026-03-14")
    assert result["start_date"] == "2026-03-01"
    assert result["end_date"] == "2026-03-14"
    assert result["activity_count"] == 3
    assert result["total_distance_meters"] == 45000.0
    assert result["average_heart_rate"] == 157.5  # avg of 155 and 160
    assert result["activity_types"]["running"] == 2
    assert result["activity_types"]["cycling"] == 1
    mock_garmin.get_activities_by_date.assert_called_once_with("2026-03-01", "2026-03-14")


@pytest.mark.asyncio
async def test_analyze_training_period_empty(mock_garmin):
    mock_garmin.get_activities_by_date.return_value = []
    client = GarminClient(mock_garmin)
    result = await client.analyze_training_period("2026-03-01", "2026-03-07")
    assert result["activity_count"] == 0
    assert result["total_distance_meters"] == 0
    assert result["average_heart_rate"] is None
    assert result["activity_types"] == {}
