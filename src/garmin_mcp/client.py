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
        return self._garmin.get_activities(start, limit)

    async def get_activities_by_date(
        self, start_date: str, end_date: str, activity_type: str | None = None
    ) -> list[dict[str, Any]]:
        """Search activities within a date range."""
        return self._garmin.get_activities_by_date(start_date, end_date, activity_type)

    async def get_last_activity(self) -> dict[str, Any]:
        """Get the most recent activity."""
        return self._garmin.get_last_activity()

    async def count_activities(self) -> dict[str, Any]:
        """Get total number of activities."""
        count = self._garmin.count_activities()
        return {"total_activities": count}

    async def get_activity(self, activity_id: str) -> dict[str, Any]:
        """Summary data for a specific activity."""
        return self._garmin.get_activity(activity_id)

    async def get_activity_details(self, activity_id: str) -> dict[str, Any]:
        """Detailed metrics: HR, pace, elevation time series."""
        return self._garmin.get_activity_details(activity_id)

    async def get_activity_splits(self, activity_id: str) -> dict[str, Any]:
        """Per-km or per-mile split data."""
        return self._garmin.get_activity_splits(activity_id)

    async def get_activity_weather(self, activity_id: str) -> dict[str, Any]:
        """Weather conditions during activity."""
        return self._garmin.get_activity_weather(activity_id)

    async def get_activity_hr_zones(self, activity_id: str) -> dict[str, Any]:
        """Time in each heart rate zone."""
        data = self._garmin.get_activity_hr_in_timezones(activity_id)
        return {
            "activity_id": activity_id,
            "hr_zones": data if isinstance(data, list) else [],
        }

    async def get_activity_exercise_sets(self, activity_id: str) -> dict[str, Any]:
        """Strength training sets (reps, weight)."""
        return self._garmin.get_activity_exercise_sets(activity_id)

    async def get_activity_types(self) -> list[dict[str, Any]]:
        """All available activity types."""
        return self._garmin.get_activity_types()

    async def get_progress_summary(self, start_date: str, end_date: str) -> dict[str, Any]:
        """Fitness stats over a date range by activity type."""
        data = self._garmin.get_progress_summary_between_dates(start_date, end_date)
        return {
            "start_date": start_date,
            "end_date": end_date,
            "summaries": data if isinstance(data, list) else [],
        }

    # --- Health methods (health agent) ---

    async def get_daily_summary(self, date: str) -> dict[str, Any]:
        """Full daily summary (steps, calories, distance, etc.)."""
        data = self._garmin.get_user_summary(date)
        return {
            "date": date,
            "total_steps": data.get("totalSteps"),
            "total_distance_meters": data.get("totalDistanceMeters"),
            "active_kilocalories": data.get("activeKilocalories"),
            "bmr_kilocalories": data.get("bmrKilocalories"),
            "total_kilocalories": data.get("totalKilocalories"),
            "floors_ascended": data.get("floorsAscended"),
            "floors_descended": data.get("floorsDescended"),
            "moderate_intensity_minutes": data.get("moderateIntensityMinutes"),
            "vigorous_intensity_minutes": data.get("vigorousIntensityMinutes"),
            "resting_heart_rate": data.get("restingHeartRate"),
            "average_stress_level": data.get("averageStressLevel"),
            "body_battery_charged_value": data.get("bodyBatteryChargedValue"),
            "body_battery_drained_value": data.get("bodyBatteryDrainedValue"),
            "body_battery_highest_value": data.get("bodyBatteryHighestValue"),
            "body_battery_lowest_value": data.get("bodyBatteryLowestValue"),
        }

    async def get_steps(self, date: str) -> dict[str, Any]:
        """Step count for a date."""
        data = self._garmin.get_user_summary(date)
        return {
            "date": date,
            "total_steps": data.get("totalSteps"),
            "step_goal": data.get("dailyStepGoal"),
        }

    async def get_steps_chart(self, date: str) -> dict[str, Any]:
        """Intraday step data throughout the day."""
        data = self._garmin.get_steps_data(date)
        return {
            "date": date,
            "time_series": data if isinstance(data, list) else [],
        }

    async def get_heart_rate(self, date: str) -> dict[str, Any]:
        """Heart rate data (resting, min, max, time series)."""
        data = self._garmin.get_heart_rates(date)
        return {
            "date": date,
            "resting_heart_rate": data.get("restingHeartRate"),
            "min_heart_rate": data.get("minHeartRate"),
            "max_heart_rate": data.get("maxHeartRate"),
            "last_seven_days_avg_resting_heart_rate": data.get("lastSevenDaysAvgRestingHeartRate"),
            "time_series": data.get("heartRateValues", []),
        }

    async def get_resting_heart_rate(self, date: str) -> dict[str, Any]:
        """Resting heart rate for a date."""
        data = self._garmin.get_rhr_day(date)
        value = (
            data.get("allMetrics", {})
            .get("metricsMap", {})
            .get("WELLNESS_RESTING_HEART_RATE", [{}])
        )
        rhr = value[0].get("value") if value else None
        return {
            "date": date,
            "resting_heart_rate": rhr,
            "value": rhr,
        }

    async def get_stress(self, date: str) -> dict[str, Any]:
        """Stress levels and time series."""
        data = self._garmin.get_all_day_stress(date)
        return {
            "date": date,
            "avg_stress_level": data.get("avgStressLevel"),
            "max_stress_level": data.get("maxStressLevel"),
            "rest_stress_duration": data.get("restStressDuration"),
            "low_stress_duration": data.get("lowStressDuration"),
            "medium_stress_duration": data.get("mediumStressDuration"),
            "high_stress_duration": data.get("highStressDuration"),
            "stress_qualifier": data.get("stressQualifier"),
            "stress_values": data.get("stressValuesArray", []),
        }

    async def get_body_battery(self, start_date: str, end_date: str) -> dict[str, Any]:
        """Body Battery energy levels (date range)."""
        data = self._garmin.get_body_battery(start_date, end_date)
        return {
            "start_date": start_date,
            "end_date": end_date,
            "data": data if isinstance(data, list) else [],
        }

    async def get_body_battery_events(self, date: str) -> dict[str, Any]:
        """Battery charge/drain events for a day."""
        data = self._garmin.get_body_battery_events(date)
        return {
            "date": date,
            "events": data if isinstance(data, list) else [],
        }

    async def get_respiration(self, date: str) -> dict[str, Any]:
        """Breathing rate data."""
        data = self._garmin.get_respiration_data(date)
        return {
            "date": date,
            "avg_waking_respiration_value": data.get("avgWakingRespirationValue"),
            "highest_respiration_value": data.get("highestRespirationValue"),
            "lowest_respiration_value": data.get("lowestRespirationValue"),
            "avg_sleep_respiration_value": data.get("avgSleepRespirationValue"),
            "respiration_values": data.get("respirationValuesArray", []),
        }

    async def get_spo2(self, date: str) -> dict[str, Any]:
        """Blood oxygen saturation."""
        data = self._garmin.get_spo2_data(date)
        return {
            "date": date,
            "avg_spo2": data.get("averageSpO2"),
            "lowest_spo2": data.get("lowestSpO2"),
            "latest_spo2": data.get("latestSpO2"),
            "spo2_single_values": data.get("spO2SingleValues", []),
            "continuous_reading_list": data.get("continuousReadingDTOList") or [],
        }

    async def get_intensity_minutes(self, date: str) -> dict[str, Any]:
        """Moderate/vigorous intensity minutes."""
        data = self._garmin.get_intensity_minutes_data(date)
        return {
            "date": date,
            "moderate_minutes": data.get("moderateMinutes"),
            "vigorous_minutes": data.get("vigorousMinutes"),
            "weekly_moderate": data.get("weeklyModerate"),
            "weekly_vigorous": data.get("weeklyVigorous"),
            "weekly_total": data.get("weeklyTotal"),
            "week_goal": data.get("weekGoal"),
        }

    async def get_floors(self, date: str) -> dict[str, Any]:
        """Floors climbed chart data."""
        data = self._garmin.get_floors(date)
        return {
            "date": date,
            "floor_values_array": data.get("floorValuesArray", []),
        }

    async def get_hydration(self, date: str) -> dict[str, Any]:
        """Daily hydration/water intake."""
        data = self._garmin.get_hydration_data(date)
        return {
            "date": date,
            "value_in_ml": data.get("valueInML"),
            "goal_in_ml": data.get("goalInML"),
            "daily_average_in_ml": data.get("dailyAverageinML"),
            "sweat_loss_in_ml": data.get("sweatLossInML"),
        }

    async def get_daily_events(self, date: str) -> dict[str, Any]:
        """Daily wellness events (sleep, activities, naps)."""
        data = self._garmin.get_all_day_events(date)
        return {
            "date": date,
            "events": data if isinstance(data, list) else [],
        }

    # --- Training methods (training agent) ---

    async def get_vo2max(self, date: str) -> dict[str, Any]:
        """VO2 Max estimate (running/cycling)."""
        data = self._garmin.get_max_metrics(date)
        # API returns a list; extract first entry if present
        entry = data[0] if isinstance(data, list) and data else {}
        generic = entry.get("generic") or {}
        cycling = entry.get("cycling") or {}
        return {
            "date": date,
            "vo2max_running": generic.get("vo2MaxPreciseValue"),
            "vo2max_cycling": cycling.get("vo2MaxPreciseValue"),
            "fitness_age": generic.get("fitnessAge"),
        }

    async def get_training_readiness(self, date: str) -> dict[str, Any]:
        """Training Readiness score."""
        data = self._garmin.get_training_readiness(date)
        # API returns a list of readiness entries; take the most recent
        entry = data[0] if isinstance(data, list) and data else {}
        return {
            "date": date,
            "score": entry.get("score"),
            "level": entry.get("level"),
            "sleep_score": entry.get("sleepScore"),
            "recovery_time": entry.get("recoveryTime"),
            "hrv_weekly_average": entry.get("hrvWeeklyAverage"),
            "feedback": entry.get("feedbackShort"),
        }

    async def get_training_status(self, date: str) -> dict[str, Any]:
        """Training status and load."""
        data = self._garmin.get_training_status(date)
        # Navigate nested structure to find primary device status
        latest = data.get("mostRecentTrainingStatus", {}).get("latestTrainingStatusData", {})
        # Find the primary device entry (or first available)
        status_entry = {}
        for device_data in latest.values():
            if isinstance(device_data, dict):
                if device_data.get("primaryTrainingDevice", False):
                    status_entry = device_data
                    break
                if not status_entry:
                    status_entry = device_data
        acute = status_entry.get("acuteTrainingLoadDTO", {})
        # VO2max from training status response
        vo2max_data = data.get("mostRecentVO2Max", {})
        generic_vo2 = vo2max_data.get("generic") or {}
        return {
            "date": date,
            "training_status": status_entry.get("trainingStatus"),
            "training_status_feedback": status_entry.get("trainingStatusFeedbackPhrase"),
            "fitness_trend": status_entry.get("fitnessTrend"),
            "acute_load": acute.get("dailyTrainingLoadAcute"),
            "chronic_load": acute.get("dailyTrainingLoadChronic"),
            "acwr_ratio": acute.get("dailyAcuteChronicWorkloadRatio"),
            "vo2max": generic_vo2.get("vo2MaxPreciseValue"),
        }

    async def get_hrv(self, date: str) -> dict[str, Any]:
        """Heart Rate Variability."""
        data = self._garmin.get_hrv_data(date)
        summary = data.get("hrvSummary", {}) or {}
        return {
            "date": date,
            "last_night_avg": summary.get("lastNightAvg"),
            "last_night_5min_high": summary.get("lastNight5MinHigh"),
            "status": summary.get("status"),
            "weekly_avg": summary.get("weeklyAvg"),
            "baseline": summary.get("baseline"),
            "feedback": summary.get("feedbackPhrase"),
        }

    async def get_endurance_score(self, start_date: str, end_date: str) -> dict[str, Any]:
        """Endurance fitness score."""
        data = self._garmin.get_endurance_score(start_date, end_date)
        score_dto = data.get("enduranceScoreDTO", {}) or {}
        return {
            "start_date": start_date,
            "end_date": end_date,
            "overall_score": score_dto.get("overallScore"),
            "classification": score_dto.get("classification"),
            "period_avg": data.get("avg"),
            "period_max": data.get("max"),
        }

    async def get_hill_score(self, start_date: str, end_date: str) -> dict[str, Any]:
        """Climbing performance score."""
        data = self._garmin.get_hill_score(start_date, end_date)
        scores = data.get("hillScoreDTOList", [])
        latest = scores[0] if scores else {}
        return {
            "start_date": start_date,
            "end_date": end_date,
            "overall_score": latest.get("overallScore"),
            "strength_score": latest.get("strengthScore"),
            "endurance_score": latest.get("enduranceScore"),
            "max_score": data.get("maxScore"),
        }

    async def get_race_predictions(self) -> dict[str, Any]:
        """5K/10K/half/full marathon predictions."""
        data = self._garmin.get_race_predictions()
        return {
            "5k_seconds": data.get("time5K"),
            "10k_seconds": data.get("time10K"),
            "half_marathon_seconds": data.get("timeHalfMarathon"),
            "marathon_seconds": data.get("timeMarathon"),
        }

    async def get_fitness_age(self, date: str) -> dict[str, Any]:
        """Estimated fitness age."""
        data = self._garmin.get_fitnessage_data(date)
        return {
            "date": date,
            "fitness_age": data.get("fitnessAge"),
            "chronological_age": data.get("chronologicalAge"),
        }

    async def get_personal_records(self) -> dict[str, Any]:
        """All personal records."""
        data = self._garmin.get_personal_record()
        return {"records": data if isinstance(data, list) else []}

    async def get_lactate_threshold(self) -> dict[str, Any]:
        """Lactate threshold HR and pace."""
        data = self._garmin.get_lactate_threshold()
        shr = data.get("speed_and_heart_rate", {}) or {}
        power = data.get("power", {}) or {}
        return {
            "heart_rate": shr.get("heartRate"),
            "speed": shr.get("speed"),
            "running_ftp": power.get("functionalThresholdPower"),
            "sport": power.get("sport"),
        }

    async def get_cycling_ftp(self) -> dict[str, Any]:
        """Functional Threshold Power (cycling)."""
        data = self._garmin.get_cycling_ftp()
        return {
            "ftp": data.get("functionalThresholdPower"),
            "sport": data.get("sport"),
            "is_stale": data.get("isStale"),
        }

    # --- Trends methods (training agent) ---

    async def get_daily_steps_range(self, start_date: str, end_date: str) -> list[dict[str, Any]]:
        """Daily step counts over a date range."""
        data = self._garmin.get_daily_steps(start_date, end_date)
        return data if isinstance(data, list) else []

    async def get_weekly_steps(self, date: str) -> dict[str, Any]:
        """Weekly step aggregates."""
        data = self._garmin.get_weekly_steps(date)
        return {"date": date, "weekly_steps": data}

    async def get_weekly_stress(self, date: str) -> dict[str, Any]:
        """Weekly stress aggregates."""
        data = self._garmin.get_weekly_stress(date)
        return {"date": date, "weekly_stress": data}

    async def get_weekly_intensity_minutes(self, start_date: str, end_date: str) -> dict[str, Any]:
        """Weekly intensity minutes."""
        data = self._garmin.get_weekly_intensity_minutes(start_date, end_date)
        return {"start_date": start_date, "end_date": end_date, "weekly_intensity": data}

    # --- Analysis methods (training agent) ---

    async def compare_activities(self, activity_ids: list[str]) -> dict[str, Any]:
        """Side-by-side comparison of 2-5 activities."""
        activities = []
        for aid in activity_ids:
            activity = self._garmin.get_activity(aid)
            # Detail endpoint nests metrics under summaryDTO
            summary = activity.get("summaryDTO", {})
            activities.append(
                {
                    "id": aid,
                    "name": activity.get("activityName"),
                    "distance": summary.get("distance"),
                    "duration": summary.get("duration"),
                    "average_hr": summary.get("averageHR"),
                    "average_speed": summary.get("averageSpeed"),
                }
            )
        return {"count": len(activities), "activities": activities}

    async def find_similar_activities(
        self, activity_id: str, limit: int = 5
    ) -> list[dict[str, Any]]:
        """Find activities similar to a reference."""
        ref = self._garmin.get_activity(activity_id)
        # Detail endpoint uses activityTypeDTO, summaryDTO
        ref_type = ref.get("activityTypeDTO", {}).get("typeKey")
        ref_distance = ref.get("summaryDTO", {}).get("distance") or 0
        # List endpoint uses flat activityType, distance
        candidates = self._garmin.get_activities(0, 50)
        same_type = [
            a
            for a in candidates
            if a.get("activityType", {}).get("typeKey") == ref_type
            and str(a.get("activityId")) != str(activity_id)
        ]
        same_type.sort(key=lambda a: abs((a.get("distance") or 0) - ref_distance))
        return same_type[:limit]

    async def analyze_training_period(self, start_date: str, end_date: str) -> dict[str, Any]:
        """Analyze training over a time period with insights."""
        activities = self._garmin.get_activities_by_date(start_date, end_date)
        count = len(activities)
        total_distance = sum(a.get("distance") or 0 for a in activities)
        hr_values = [a.get("averageHR") for a in activities if a.get("averageHR")]
        avg_hr = sum(hr_values) / len(hr_values) if hr_values else None
        type_counts: dict[str, int] = {}
        for a in activities:
            t = a.get("activityType", {}).get("typeKey", "unknown")
            type_counts[t] = type_counts.get(t, 0) + 1
        return {
            "start_date": start_date,
            "end_date": end_date,
            "activity_count": count,
            "total_distance_meters": total_distance,
            "average_heart_rate": avg_hr,
            "activity_types": type_counts,
        }

    # --- Body methods (body/sleep agent) ---

    async def get_body_composition(self, start_date: str, end_date: str) -> dict[str, Any]:
        """Weight, BMI, body fat %, muscle mass (date range)."""
        return self._garmin.get_body_composition(start_date, end_date)

    async def get_latest_weight(self) -> dict[str, Any]:
        """Most recent weight entry."""
        from datetime import date, timedelta

        end = date.today().isoformat()
        start = (date.today() - timedelta(days=30)).isoformat()
        data = self._garmin.get_body_composition(start, end)
        entries = data.get("dateWeightList", []) if isinstance(data, dict) else []
        if entries:
            latest = entries[-1]
            return {
                "date": latest.get("calendarDate"),
                "weight_kg": latest.get("weight"),
                "bmi": latest.get("bmi"),
                "body_fat_percent": latest.get("bodyFat"),
                "muscle_mass_kg": latest.get("muscleMass"),
            }
        return {"error": "No weight entries found in last 30 days"}

    async def get_daily_weigh_ins(self, date: str) -> dict[str, Any]:
        """All weigh-ins for a date."""
        return self._garmin.get_daily_weigh_ins(date)

    async def get_weigh_ins(self, start_date: str, end_date: str) -> dict[str, Any]:
        """Weigh-in records over a date range."""
        return self._garmin.get_weigh_ins(start_date, end_date)

    async def get_blood_pressure(self, start_date: str, end_date: str) -> dict[str, Any]:
        """Blood pressure readings (date range)."""
        return self._garmin.get_blood_pressure(start_date, end_date)

    # --- Sleep methods (body/sleep agent) ---

    async def get_sleep_data(self, date: str) -> dict[str, Any]:
        """Sleep stages, score, bed/wake times."""
        data = self._garmin.get_sleep_data(date)
        dto = data.get("dailySleepDTO", {})
        return {
            "date": date,
            "sleep_score": dto.get("sleepScores", {}).get("overall", {}).get("value"),
            "sleep_start": dto.get("sleepStartTimestampGMT"),
            "sleep_end": dto.get("sleepEndTimestampGMT"),
            "duration_seconds": dto.get("sleepTimeSeconds"),
            "deep_sleep_seconds": dto.get("deepSleepSeconds"),
            "light_sleep_seconds": dto.get("lightSleepSeconds"),
            "rem_sleep_seconds": dto.get("remSleepSeconds"),
            "awake_seconds": dto.get("awakeSleepSeconds"),
        }

    async def get_sleep_data_raw(self, date: str) -> dict[str, Any]:
        """Raw sleep data with HR and SpO2."""
        return self._garmin.get_sleep_data(date)

    # --- Profile methods (profile agent) ---

    async def get_user_profile(self) -> dict[str, Any]:
        """User social profile and preferences."""
        return self._garmin.get_user_profile()

    async def get_user_settings(self) -> dict[str, Any]:
        """User settings, measurement system, sleep schedule."""
        return self._garmin.get_userprofile_settings()

    async def get_devices(self) -> list[dict[str, Any]]:
        """Registered Garmin devices."""
        return self._garmin.get_devices()

    async def get_device_settings(self, device_id: str) -> dict[str, Any]:
        """Settings for a specific device."""
        return self._garmin.get_device_settings(device_id)

    async def get_device_last_used(self) -> dict[str, Any]:
        """Last used device info."""
        return self._garmin.get_device_last_used()

    async def get_primary_training_device(self) -> dict[str, Any]:
        """Primary training device."""
        return self._garmin.get_primary_training_device()

    async def get_gear(self) -> list[dict[str, Any]]:
        """All tracked gear/equipment."""
        last_used = self._garmin.get_device_last_used()
        profile_number = last_used["userProfileNumber"]
        return self._garmin.get_gear(profile_number)

    async def get_gear_stats(self, gear_uuid: str) -> dict[str, Any]:
        """Usage stats for a gear item."""
        return self._garmin.get_gear_stats(gear_uuid)

    async def get_goals(self) -> list[dict[str, Any]]:
        """Active goals and progress."""
        return self._garmin.get_goals()

    async def get_earned_badges(self) -> list[dict[str, Any]]:
        """Earned badges and achievements."""
        return self._garmin.get_earned_badges()

    async def get_workouts(self) -> list[dict[str, Any]]:
        """Saved workouts."""
        return self._garmin.get_workouts()

    async def get_workout(self, workout_id: str) -> dict[str, Any]:
        """Specific workout by ID."""
        return self._garmin.get_workout_by_id(workout_id)

    async def get_activity_gear(self, activity_id: str) -> list[dict[str, Any]]:
        """Gear used for a specific activity."""
        return self._garmin.get_activity_gear(activity_id)

    # --- Fenix 8 AMOLED methods ---

    async def get_running_dynamics(self, activity_id: str) -> dict[str, Any]:
        """Running dynamics metrics from an activity."""
        data = self._garmin.get_activity(activity_id)
        summary = data.get("summaryDTO", {})
        return {
            "activity_id": activity_id,
            "avg_cadence": summary.get("averageRunCadence"),
            "max_cadence": summary.get("maxRunCadence"),
            "avg_ground_contact_time_ms": summary.get("groundContactTime"),
            "avg_stride_length_m": summary.get("strideLength"),
            "avg_vertical_oscillation_cm": summary.get("verticalOscillation"),
            "avg_vertical_ratio": summary.get("verticalRatio"),
        }

    async def get_training_effect(self, activity_id: str) -> dict[str, Any]:
        """Training effect breakdown for an activity."""
        data = self._garmin.get_activity(activity_id)
        summary = data.get("summaryDTO", {})
        return {
            "activity_id": activity_id,
            "aerobic_training_effect": summary.get("trainingEffect"),
            "anaerobic_training_effect": summary.get("anaerobicTrainingEffect"),
            "aerobic_effect_message": summary.get("aerobicTrainingEffectMessage"),
            "anaerobic_effect_message": summary.get("anaerobicTrainingEffectMessage"),
            "training_effect_label": summary.get("trainingEffectLabel"),
        }

    async def get_activity_power_zones(self, activity_id: str) -> dict[str, Any]:
        """Power zone time distribution for an activity."""
        data = self._garmin.get_activity_power_in_timezones(activity_id)
        return {
            "activity_id": activity_id,
            "power_zones": data if isinstance(data, list) else [],
        }

    async def get_running_power(self, activity_id: str) -> dict[str, Any]:
        """Running power metrics from an activity."""
        data = self._garmin.get_activity(activity_id)
        summary = data.get("summaryDTO", {})
        return {
            "activity_id": activity_id,
            "avg_power_watts": summary.get("averagePower"),
            "max_power_watts": summary.get("maxPower"),
            "normalized_power_watts": summary.get("normalizedPower"),
            "min_power_watts": summary.get("minPower"),
        }

    async def get_climbpro_data(self, activity_id: str) -> dict[str, Any]:
        """ClimbPro split summaries for an activity."""
        data = self._garmin.get_activity_split_summaries(activity_id)
        return {
            "activity_id": activity_id,
            "split_summaries": data.get("splitSummaries", []) if isinstance(data, dict) else [],
        }

    async def get_activity_typed_splits(self, activity_id: str) -> dict[str, Any]:
        """Typed split data for an activity."""
        data = self._garmin.get_activity_typed_splits(activity_id)
        return {
            "activity_id": activity_id,
            "typed_splits": data.get("typedSplits", []) if isinstance(data, dict) else [],
        }

    async def get_morning_readiness(self, date: str) -> dict[str, Any]:
        """Morning training readiness assessment."""
        data = self._garmin.get_morning_training_readiness(date)
        return {
            "date": date,
            "score": data.get("score"),
            "level": data.get("level"),
            "sleep_score": data.get("sleepScore"),
            "hrv_factor_feedback": data.get("hrvFactorFeedback"),
            "hrv_weekly_average": data.get("hrvWeeklyAverage"),
            "recovery_time": data.get("recoveryTime"),
            "feedback_short": data.get("feedbackShort"),
        }


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
