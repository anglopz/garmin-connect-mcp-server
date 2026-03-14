# Garmin Connect API Reference

Maps each MCP tool to its `garminconnect` library method.

## Activities (12 tools)

| MCP Tool | `garminconnect` Method |
|----------|----------------------|
| `get_activities` | `get_activities(start, limit)` |
| `get_activities_by_date` | `get_activities_by_date(start, end, activitytype)` |
| `get_last_activity` | `get_last_activity()` |
| `count_activities` | `count_activities()` |
| `get_activity` | `get_activity(activity_id)` |
| `get_activity_details` | `get_activity_details(activity_id)` |
| `get_activity_splits` | `get_activity_splits(activity_id)` |
| `get_activity_weather` | `get_activity_weather(activity_id)` |
| `get_activity_hr_zones` | `get_activity_hr_in_timezones(activity_id)` |
| `get_activity_exercise_sets` | `get_activity_exercise_sets(activity_id)` |
| `get_activity_types` | `get_activity_types()` |
| `get_progress_summary` | `get_progress_summary_between_dates(start, end)` |

## Daily Health (14 tools)

| MCP Tool | `garminconnect` Method |
|----------|----------------------|
| `get_daily_summary` | `get_user_summary(date)` |
| `get_steps` | `get_steps_data(date)` |
| `get_steps_chart` | `get_steps_data(date)` (chart detail) |
| `get_heart_rate` | `get_heart_rates(date)` |
| `get_resting_heart_rate` | `get_resting_heart_rate(date)` |
| `get_stress` | `get_all_day_stress(date)` |
| `get_body_battery` | `get_body_battery(start, end)` |
| `get_body_battery_events` | `get_body_battery_events(date)` |
| `get_respiration` | `get_respiration_data(date)` |
| `get_spo2` | `get_spo2_data(date)` |
| `get_intensity_minutes` | `get_intensity_minutes_data(date)` |
| `get_floors` | `get_floors(date)` |
| `get_hydration` | `get_hydration_data(date)` |
| `get_daily_events` | `get_all_day_events(date)` |

## Trends (4 tools)

| MCP Tool | `garminconnect` Method |
|----------|----------------------|
| `get_daily_steps_range` | `get_daily_steps(start, end)` |
| `get_weekly_steps` | `get_weekly_steps(date)` |
| `get_weekly_stress` | `get_weekly_stress(date)` |
| `get_weekly_intensity_minutes` | `get_weekly_intensity_minutes(start, end)` |

## Sleep (2 tools)

| MCP Tool | `garminconnect` Method |
|----------|----------------------|
| `get_sleep_data` | `get_sleep_data(date)` |
| `get_sleep_data_raw` | `get_sleep_data(date)` (full payload) |

## Body Composition (5 tools)

| MCP Tool | `garminconnect` Method |
|----------|----------------------|
| `get_body_composition` | `get_body_composition(start, end)` |
| `get_latest_weight` | `get_weigh_ins(date_range)` (latest) |
| `get_daily_weigh_ins` | `get_daily_weigh_ins(date)` |
| `get_weigh_ins` | `get_weigh_ins(start, end)` |
| `get_blood_pressure` | `get_blood_pressure(start, end)` |

## Performance & Training (11 tools)

| MCP Tool | `garminconnect` Method |
|----------|----------------------|
| `get_vo2max` | `get_max_metrics(date)` |
| `get_training_readiness` | `get_training_readiness(date)` |
| `get_training_status` | `get_training_status(date)` |
| `get_hrv` | `get_hrv_data(date)` |
| `get_endurance_score` | `get_endurance_score(start, end)` |
| `get_hill_score` | `get_hill_score(start, end)` |
| `get_race_predictions` | `get_race_predictions()` |
| `get_fitness_age` | `get_fitnessage_data(date)` |
| `get_personal_records` | `get_personal_records()` |
| `get_lactate_threshold` | `get_lactate_threshold(latest, ...)` |
| `get_cycling_ftp` | `get_cycling_ftp()` |

## Profile & Devices (13 tools)

| MCP Tool | `garminconnect` Method |
|----------|----------------------|
| `get_user_profile` | `get_user_profile()` |
| `get_user_settings` | `get_userprofile_settings()` |
| `get_devices` | `get_devices()` |
| `get_device_settings` | `get_device_settings(device_id)` |
| `get_device_last_used` | `get_device_last_used()` |
| `get_primary_training_device` | `get_primary_training_device()` |
| `get_gear` | `get_gear(profile_number)` |
| `get_gear_stats` | `get_gear_stats(gear_uuid)` |
| `get_goals` | `get_active_goals()` |
| `get_earned_badges` | `get_earned_badges()` |
| `get_workouts` | `get_workouts()` |
| `get_workout` | `get_workout_by_id(workout_id)` |
| `get_activity_gear` | `get_activity_gear(activity_id)` |

## Analysis (3 custom tools)

| MCP Tool | Implementation |
|----------|---------------|
| `compare_activities` | Fetches details for each, returns comparison dict |
| `find_similar_activities` | Fetches recent, filters by type/distance/pace |
| `analyze_training_period` | Aggregates activities + health data for period |

## Resources (3)

| URI | Source |
|-----|--------|
| `garmin://athlete/profile` | `get_user_profile()` + `get_personal_records()` |
| `garmin://training/readiness` | `get_training_readiness()` + `get_body_battery()` |
| `garmin://health/today` | `get_user_summary()` + `get_sleep_data()` + `get_stress()` |

## Prompts (4)

| Name | Context Tools |
|------|--------------|
| `analyze-recent-training` | Activities + training status + VO2max |
| `sleep-quality-report` | Sleep data + body battery + stress |
| `training-readiness-check` | Training readiness + HRV + sleep + body battery |
| `health-summary` | Daily summary + HR + stress + sleep + steps |
