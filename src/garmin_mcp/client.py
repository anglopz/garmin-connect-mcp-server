"""GarminClient — single adapter for all Garmin Connect API interactions.

All data transformation and API logic lives here. Tool functions are thin
wrappers that delegate to this client. The client wraps the garminconnect
library's Garmin class.
"""

from __future__ import annotations

import logging
from typing import Any

from garminconnect import Garmin

from garmin_mcp.auth import authenticate

logger = logging.getLogger("garmin_mcp.client")

_client_instance: GarminClient | None = None


class GarminClient:
    """Adapter around garminconnect.Garmin with structured return types."""

    def __init__(self, garmin: Garmin) -> None:
        self._garmin = garmin

    # --- Activities methods (activities agent) ---

    async def get_activities(self, start: int = 0, limit: int = 10) -> list[dict[str, Any]]:
        """List recent activities with pagination."""
        raise NotImplementedError

    async def get_activities_by_date(
        self, start_date: str, end_date: str, activity_type: str | None = None
    ) -> list[dict[str, Any]]:
        """Search activities within a date range."""
        raise NotImplementedError

    async def get_last_activity(self) -> dict[str, Any]:
        """Get the most recent activity."""
        raise NotImplementedError

    async def count_activities(self) -> dict[str, Any]:
        """Get total number of activities."""
        raise NotImplementedError

    async def get_activity(self, activity_id: str) -> dict[str, Any]:
        """Summary data for a specific activity."""
        raise NotImplementedError

    async def get_activity_details(self, activity_id: str) -> dict[str, Any]:
        """Detailed metrics: HR, pace, elevation time series."""
        raise NotImplementedError

    async def get_activity_splits(self, activity_id: str) -> dict[str, Any]:
        """Per-km or per-mile split data."""
        raise NotImplementedError

    async def get_activity_weather(self, activity_id: str) -> dict[str, Any]:
        """Weather conditions during activity."""
        raise NotImplementedError

    async def get_activity_hr_zones(self, activity_id: str) -> dict[str, Any]:
        """Time in each heart rate zone."""
        raise NotImplementedError

    async def get_activity_exercise_sets(self, activity_id: str) -> dict[str, Any]:
        """Strength training sets (reps, weight)."""
        raise NotImplementedError

    async def get_activity_types(self) -> list[dict[str, Any]]:
        """All available activity types."""
        raise NotImplementedError

    async def get_progress_summary(self, start_date: str, end_date: str) -> dict[str, Any]:
        """Fitness stats over a date range by activity type."""
        raise NotImplementedError

    # --- Health methods (health agent) ---

    async def get_daily_summary(self, date: str) -> dict[str, Any]:
        """Full daily summary (steps, calories, distance, etc.)."""
        raise NotImplementedError

    async def get_steps(self, date: str) -> dict[str, Any]:
        """Step count for a date."""
        raise NotImplementedError

    async def get_steps_chart(self, date: str) -> dict[str, Any]:
        """Intraday step data throughout the day."""
        raise NotImplementedError

    async def get_heart_rate(self, date: str) -> dict[str, Any]:
        """Heart rate data (resting, max, zones, time series)."""
        raise NotImplementedError

    async def get_resting_heart_rate(self, date: str) -> dict[str, Any]:
        """Resting heart rate for a date."""
        raise NotImplementedError

    async def get_stress(self, date: str) -> dict[str, Any]:
        """Stress levels and time series."""
        raise NotImplementedError

    async def get_body_battery(self, start_date: str, end_date: str) -> dict[str, Any]:
        """Body Battery energy levels (date range)."""
        raise NotImplementedError

    async def get_body_battery_events(self, date: str) -> dict[str, Any]:
        """Battery charge/drain events for a day."""
        raise NotImplementedError

    async def get_respiration(self, date: str) -> dict[str, Any]:
        """Breathing rate data."""
        raise NotImplementedError

    async def get_spo2(self, date: str) -> dict[str, Any]:
        """Blood oxygen saturation."""
        raise NotImplementedError

    async def get_intensity_minutes(self, date: str) -> dict[str, Any]:
        """Moderate/vigorous intensity minutes."""
        raise NotImplementedError

    async def get_floors(self, date: str) -> dict[str, Any]:
        """Floors climbed chart data."""
        raise NotImplementedError

    async def get_hydration(self, date: str) -> dict[str, Any]:
        """Daily hydration/water intake."""
        raise NotImplementedError

    async def get_daily_events(self, date: str) -> dict[str, Any]:
        """Daily wellness events (sleep, activities, naps)."""
        raise NotImplementedError

    # --- Training methods (training agent) ---

    async def get_vo2max(self, date: str) -> dict[str, Any]:
        """VO2 Max estimate (running/cycling)."""
        raise NotImplementedError

    async def get_training_readiness(self, date: str) -> dict[str, Any]:
        """Training Readiness score."""
        raise NotImplementedError

    async def get_training_status(self, date: str) -> dict[str, Any]:
        """Training status and load."""
        raise NotImplementedError

    async def get_hrv(self, date: str) -> dict[str, Any]:
        """Heart Rate Variability."""
        raise NotImplementedError

    async def get_endurance_score(self, start_date: str, end_date: str) -> dict[str, Any]:
        """Endurance fitness score."""
        raise NotImplementedError

    async def get_hill_score(self, start_date: str, end_date: str) -> dict[str, Any]:
        """Climbing performance score."""
        raise NotImplementedError

    async def get_race_predictions(self) -> dict[str, Any]:
        """5K/10K/half/full marathon predictions."""
        raise NotImplementedError

    async def get_fitness_age(self, date: str) -> dict[str, Any]:
        """Estimated fitness age."""
        raise NotImplementedError

    async def get_personal_records(self) -> dict[str, Any]:
        """All personal records."""
        raise NotImplementedError

    async def get_lactate_threshold(self) -> dict[str, Any]:
        """Lactate threshold HR and pace."""
        raise NotImplementedError

    async def get_cycling_ftp(self) -> dict[str, Any]:
        """Functional Threshold Power (cycling)."""
        raise NotImplementedError

    # --- Trends methods (training agent) ---

    async def get_daily_steps_range(self, start_date: str, end_date: str) -> list[dict[str, Any]]:
        """Daily step counts over a date range."""
        raise NotImplementedError

    async def get_weekly_steps(self, date: str) -> dict[str, Any]:
        """Weekly step aggregates."""
        raise NotImplementedError

    async def get_weekly_stress(self, date: str) -> dict[str, Any]:
        """Weekly stress aggregates."""
        raise NotImplementedError

    async def get_weekly_intensity_minutes(
        self, start_date: str, end_date: str
    ) -> dict[str, Any]:
        """Weekly intensity minutes."""
        raise NotImplementedError

    # --- Analysis methods (training agent) ---

    async def compare_activities(self, activity_ids: list[str]) -> dict[str, Any]:
        """Side-by-side comparison of 2-5 activities."""
        raise NotImplementedError

    async def find_similar_activities(
        self, activity_id: str, limit: int = 5
    ) -> list[dict[str, Any]]:
        """Find activities similar to a reference."""
        raise NotImplementedError

    async def analyze_training_period(
        self, start_date: str, end_date: str
    ) -> dict[str, Any]:
        """Analyze training over a time period with insights."""
        raise NotImplementedError

    # --- Body methods (body/sleep agent) ---

    async def get_body_composition(
        self, start_date: str, end_date: str
    ) -> dict[str, Any]:
        """Weight, BMI, body fat %, muscle mass (date range)."""
        raise NotImplementedError

    async def get_latest_weight(self) -> dict[str, Any]:
        """Most recent weight entry."""
        raise NotImplementedError

    async def get_daily_weigh_ins(self, date: str) -> dict[str, Any]:
        """All weigh-ins for a date."""
        raise NotImplementedError

    async def get_weigh_ins(self, start_date: str, end_date: str) -> dict[str, Any]:
        """Weigh-in records over a date range."""
        raise NotImplementedError

    async def get_blood_pressure(self, start_date: str, end_date: str) -> dict[str, Any]:
        """Blood pressure readings (date range)."""
        raise NotImplementedError

    # --- Sleep methods (body/sleep agent) ---

    async def get_sleep_data(self, date: str) -> dict[str, Any]:
        """Sleep stages, score, bed/wake times."""
        raise NotImplementedError

    async def get_sleep_data_raw(self, date: str) -> dict[str, Any]:
        """Raw sleep data with HR and SpO2."""
        raise NotImplementedError

    # --- Profile methods (profile agent) ---

    async def get_user_profile(self) -> dict[str, Any]:
        """User social profile and preferences."""
        raise NotImplementedError

    async def get_user_settings(self) -> dict[str, Any]:
        """User settings, measurement system, sleep schedule."""
        raise NotImplementedError

    async def get_devices(self) -> list[dict[str, Any]]:
        """Registered Garmin devices."""
        raise NotImplementedError

    async def get_device_settings(self, device_id: str) -> dict[str, Any]:
        """Settings for a specific device."""
        raise NotImplementedError

    async def get_device_last_used(self) -> dict[str, Any]:
        """Last used device info."""
        raise NotImplementedError

    async def get_primary_training_device(self) -> dict[str, Any]:
        """Primary training device."""
        raise NotImplementedError

    async def get_gear(self) -> list[dict[str, Any]]:
        """All tracked gear/equipment."""
        raise NotImplementedError

    async def get_gear_stats(self, gear_uuid: str) -> dict[str, Any]:
        """Usage stats for a gear item."""
        raise NotImplementedError

    async def get_goals(self) -> list[dict[str, Any]]:
        """Active goals and progress."""
        raise NotImplementedError

    async def get_earned_badges(self) -> list[dict[str, Any]]:
        """Earned badges and achievements."""
        raise NotImplementedError

    async def get_workouts(self) -> list[dict[str, Any]]:
        """Saved workouts."""
        raise NotImplementedError

    async def get_workout(self, workout_id: str) -> dict[str, Any]:
        """Specific workout by ID."""
        raise NotImplementedError

    async def get_activity_gear(self, activity_id: str) -> dict[str, Any]:
        """Gear used for a specific activity."""
        raise NotImplementedError


async def get_client() -> GarminClient:
    """Get or create the singleton GarminClient instance.

    Uses lazy authentication — first call triggers Garmin Connect login.
    """
    global _client_instance

    if _client_instance is None:
        garmin = authenticate()
        _client_instance = GarminClient(garmin)
        logger.info("GarminClient initialized")

    return _client_instance


def reset_client() -> None:
    """Reset the singleton client (useful for testing)."""
    global _client_instance
    _client_instance = None
