# Garmin Connect MCP Server — Build Plan

## Project Overview

Build a Python MCP server that exposes Garmin Connect data (from a Garmin Fenix 8 AMOLED) as tools, resources, and prompts for Claude and other LLM clients. Uses `python-garminconnect` (cyberjunky) as the API layer and the official `mcp` Python SDK (`FastMCP`) for the server.

**Repo name:** `garmin-connect-mcp-server`
**Language:** Python 3.11+
**Package manager:** `uv`
**MCP SDK:** `mcp[cli]` (FastMCP)
**Garmin API:** `garminconnect` (forked from cyberjunky/python-garminconnect)
**Transport:** stdio (Claude Desktop / Claude Code compatible)
**Target device:** Garmin Fenix 8 AMOLED (no solar — AMOLED variant does not have solar charging)
**Tool count target:** 60+ tools across 7 categories, plus 3 resources and 4+ prompts

---

## Repository Structure

```
garmin-connect-mcp-server/
├── CLAUDE.md
├── pyproject.toml
├── uv.lock
├── .env.example
├── .gitignore
├── README.md
├── LICENSE                            # MIT
├── Dockerfile
├── .claude/
│   ├── settings.json
│   └── commands/
│       ├── build-all.md
│       └── test-mcp.md
├── docs/
│   ├── ARCHITECTURE.md
│   ├── DECISIONS.md
│   ├── initiatives/
│   │   ├── overview.md
│   │   ├── phase0-scaffolding/
│   │   │   ├── plan.md
│   │   │   ├── tasks.md
│   │   │   ├── progress.md
│   │   │   └── findings.md
│   │   ├── phase1-tools-parallel/
│   │   │   ├── plan.md
│   │   │   ├── tasks.md
│   │   │   ├── progress.md
│   │   │   └── findings.md
│   │   ├── phase2-integration/
│   │   │   ├── plan.md
│   │   │   ├── tasks.md
│   │   │   ├── progress.md
│   │   │   └── findings.md
│   │   ├── phase3-fenix8-polish/
│   │   │   ├── plan.md
│   │   │   ├── tasks.md
│   │   │   ├── progress.md
│   │   │   └── findings.md
│   │   └── tasks_lessons.md
│   └── garmin-api-reference.md
├── src/
│   └── garmin_mcp/
│       ├── __init__.py
│       ├── server.py
│       ├── auth.py
│       ├── client.py
│       ├── tools/
│       │   ├── __init__.py
│       │   ├── activities.py          # 12 tools
│       │   ├── health.py             # 14 tools
│       │   ├── trends.py             # 4 tools
│       │   ├── sleep.py              # 2 tools
│       │   ├── body.py               # 5 tools
│       │   ├── training.py           # 11 tools
│       │   ├── profile.py            # 13 tools
│       │   └── analysis.py           # 3 tools (custom, not direct API wrappers)
│       ├── resources/
│       │   ├── __init__.py
│       │   ├── athlete.py
│       │   ├── readiness.py
│       │   └── daily.py
│       └── prompts/
│           ├── __init__.py
│           ├── training_analysis.py
│           ├── sleep_report.py
│           ├── readiness_check.py
│           └── health_summary.py
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_client.py
│   ├── test_tools_activities.py
│   ├── test_tools_health.py
│   ├── test_tools_trends.py
│   ├── test_tools_sleep.py
│   ├── test_tools_body.py
│   ├── test_tools_training.py
│   ├── test_tools_profile.py
│   ├── test_tools_analysis.py
│   ├── test_resources.py
│   └── test_prompts.py
└── scripts/
    ├── setup_auth.py
    └── inspect.sh
```

---

## Complete Tool Inventory (64 tools + 3 resources + 4 prompts)

### Activities (12 tools) — `tools/activities.py`

| Tool | Description | `garminconnect` method |
|------|-------------|----------------------|
| `get_activities` | List recent activities with pagination | `get_activities(start, limit)` |
| `get_activities_by_date` | Search activities within a date range | `get_activities_by_date(start, end, activitytype)` |
| `get_last_activity` | Get the most recent activity | `get_last_activity()` |
| `count_activities` | Get total number of activities | `count_activities()` |
| `get_activity` | Summary data for a specific activity | `get_activity(activity_id)` |
| `get_activity_details` | Detailed metrics: HR, pace, elevation time series | `get_activity_details(activity_id)` |
| `get_activity_splits` | Per-km or per-mile split data | `get_activity_splits(activity_id)` |
| `get_activity_weather` | Weather conditions during activity | `get_activity_weather(activity_id)` |
| `get_activity_hr_zones` | Time in each heart rate zone | `get_activity_hr_in_timezones(activity_id)` |
| `get_activity_exercise_sets` | Strength training sets (reps, weight) | `get_activity_exercise_sets(activity_id)` |
| `get_activity_types` | All available activity types | `get_activity_types()` |
| `get_progress_summary` | Fitness stats over a date range by activity type | `get_progress_summary_between_dates(start, end)` |

### Daily Health (14 tools) — `tools/health.py`

| Tool | Description | `garminconnect` method |
|------|-------------|----------------------|
| `get_daily_summary` | Full daily summary (steps, calories, distance, etc.) | `get_user_summary(date)` |
| `get_steps` | Step count for a date | `get_steps_data(date)` |
| `get_steps_chart` | Intraday step data throughout the day | `get_steps_data(date)` (chart detail) |
| `get_heart_rate` | Heart rate data (resting, max, zones, time series) | `get_heart_rates(date)` |
| `get_resting_heart_rate` | Resting heart rate for a date | `get_resting_heart_rate(date)` |
| `get_stress` | Stress levels and time series | `get_all_day_stress(date)` |
| `get_body_battery` | Body Battery energy levels (date range) | `get_body_battery(start, end)` |
| `get_body_battery_events` | Battery charge/drain events for a day | `get_body_battery_events(date)` |
| `get_respiration` | Breathing rate data | `get_respiration_data(date)` |
| `get_spo2` | Blood oxygen saturation | `get_spo2_data(date)` |
| `get_intensity_minutes` | Moderate/vigorous intensity minutes | `get_intensity_minutes_data(date)` |
| `get_floors` | Floors climbed chart data | `get_floors(date)` |
| `get_hydration` | Daily hydration/water intake | `get_hydration_data(date)` |
| `get_daily_events` | Daily wellness events (sleep, activities, naps) | `get_all_day_events(date)` |

### Trends (4 tools) — `tools/trends.py`

| Tool | Description | `garminconnect` method |
|------|-------------|----------------------|
| `get_daily_steps_range` | Daily step counts over a date range | `get_daily_steps(start, end)` |
| `get_weekly_steps` | Weekly step aggregates | `get_weekly_steps(date)` |
| `get_weekly_stress` | Weekly stress aggregates | `get_weekly_stress(date)` |
| `get_weekly_intensity_minutes` | Weekly intensity minutes | `get_weekly_intensity_minutes(start, end)` |

### Sleep (2 tools) — `tools/sleep.py`

| Tool | Description | `garminconnect` method |
|------|-------------|----------------------|
| `get_sleep_data` | Sleep stages, score, bed/wake times | `get_sleep_data(date)` |
| `get_sleep_data_raw` | Raw sleep data with HR and SpO2 | `get_sleep_data(date)` (full payload) |

### Body Composition (5 tools) — `tools/body.py`

| Tool | Description | `garminconnect` method |
|------|-------------|----------------------|
| `get_body_composition` | Weight, BMI, body fat %, muscle mass (date range) | `get_body_composition(start, end)` |
| `get_latest_weight` | Most recent weight entry | `get_weigh_ins(date_range)` (latest) |
| `get_daily_weigh_ins` | All weigh-ins for a date | `get_daily_weigh_ins(date)` |
| `get_weigh_ins` | Weigh-in records over a date range | `get_weigh_ins(start, end)` |
| `get_blood_pressure` | Blood pressure readings (date range) | `get_blood_pressure(start, end)` |

### Performance & Training (11 tools) — `tools/training.py`

| Tool | Description | `garminconnect` method |
|------|-------------|----------------------|
| `get_vo2max` | VO2 Max estimate (running/cycling) | `get_max_metrics(date)` |
| `get_training_readiness` | Training Readiness score | `get_training_readiness(date)` |
| `get_training_status` | Training status and load | `get_training_status(date)` |
| `get_hrv` | Heart Rate Variability | `get_hrv_data(date)` |
| `get_endurance_score` | Endurance fitness score | `get_endurance_score(start, end)` |
| `get_hill_score` | Climbing performance score | `get_hill_score(start, end)` |
| `get_race_predictions` | 5K/10K/half/full marathon predictions | `get_race_predictions()` |
| `get_fitness_age` | Estimated fitness age | `get_fitnessage_data(date)` |
| `get_personal_records` | All personal records | `get_personal_records()` |
| `get_lactate_threshold` | Lactate threshold HR and pace | `get_lactate_threshold(latest, ...)` |
| `get_cycling_ftp` | Functional Threshold Power (cycling) | `get_cycling_ftp()` |

### Profile & Devices (13 tools) — `tools/profile.py`

| Tool | Description | `garminconnect` method |
|------|-------------|----------------------|
| `get_user_profile` | User social profile and preferences | `get_user_profile()` |
| `get_user_settings` | User settings, measurement system, sleep schedule | `get_userprofile_settings()` |
| `get_devices` | Registered Garmin devices | `get_devices()` |
| `get_device_settings` | Settings for a specific device | `get_device_settings(device_id)` |
| `get_device_last_used` | Last used device info | `get_device_last_used()` |
| `get_primary_training_device` | Primary training device | `get_primary_training_device()` |
| `get_gear` | All tracked gear/equipment | `get_gear(profile_number)` |
| `get_gear_stats` | Usage stats for a gear item | `get_gear_stats(gear_uuid)` |
| `get_goals` | Active goals and progress | `get_active_goals()` |
| `get_earned_badges` | Earned badges and achievements | `get_earned_badges()` |
| `get_workouts` | Saved workouts | `get_workouts()` |
| `get_workout` | Specific workout by ID | `get_workout_by_id(workout_id)` |
| `get_activity_gear` | Gear used for a specific activity | `get_activity_gear(activity_id)` |

### Analysis (3 tools) — `tools/analysis.py` (custom, built on top of API data)

| Tool | Description | Implementation |
|------|-------------|----------------|
| `compare_activities` | Side-by-side comparison of 2-5 activities | Fetches details for each, returns comparison dict |
| `find_similar_activities` | Find activities similar to a reference | Fetches recent, filters by type/distance/pace |
| `analyze_training_period` | Analyze training over a time period with insights | Aggregates activities + health data for period |

### Resources (3)

| URI | Description |
|-----|-------------|
| `garmin://athlete/profile` | Athlete profile with stats, zones, PRs |
| `garmin://training/readiness` | Current training readiness and body battery |
| `garmin://health/today` | Today's health snapshot (steps, sleep, stress, HR) |

### Prompts (4)

| Name | Description |
|------|-------------|
| `analyze-recent-training` | Analyze training over past N days |
| `sleep-quality-report` | Sleep analysis with recommendations |
| `training-readiness-check` | Am I ready to train today? |
| `health-summary` | Comprehensive health overview |

**Not included (intentionally):**
- `get_device_solar_data` — Fenix 8 AMOLED has no solar charging
- Write/delete operations (weigh-in writes, activity deletion, workout uploads) — read-only MCP server for safety in Phase 1. Can add in a future phase with confirmation prompts.

---

## Architecture & Design Principles

### Data Flow

```
Claude/LLM Client
    ↓ (MCP stdio transport)
FastMCP Server (server.py)
    ↓ (tool/resource/prompt dispatch)
Tool Functions (tools/*.py) ←→ Resources (resources/*.py)
    ↓                                ↓
GarminClient (client.py) — single adapter, all Garmin API logic
    ↓
Auth Module (auth.py) — lazy auth, token cache in ~/.garmin-mcp/
    ↓
garminconnect library (Garth OAuth)
    ↓
Garmin Connect API
```

### Core Principles

1. **Thin tools, fat client** — Each MCP tool is a thin async function calling `GarminClient`. All data transformation and API interaction lives in the client adapter.
2. **FastMCP decorators** — `@mcp.tool()`, `@mcp.resource()`, `@mcp.prompt()` with type hints and docstrings. FastMCP auto-generates JSON schemas.
3. **No stdout pollution** — All logging via `logging` module to stderr. `print()` forbidden in `src/`. Critical for stdio transport.
4. **Lazy auth** — Authenticate on first tool call, cache OAuth tokens in `~/.garmin-mcp/`. MFA prompt via stderr.
5. **Testable** — `GarminClient` is injectable. Tools tested with mock client. Zero network calls in unit tests.
6. **ISO dates everywhere** — All date params use `YYYY-MM-DD` string format.
7. **Read-only in Phase 1** — No write/delete operations. Safety first for MCP tool exposure.
8. **Fenix 8 AMOLED aware** — No solar tools. Phase 3 adds AMOLED-specific features.

---

## Docs Convention

Each phase in `docs/initiatives/<phase>/` has four files:

| File | Purpose | Who writes | When |
|------|---------|-----------|------|
| `plan.md` | Scope, objectives, acceptance criteria | Team lead | Before phase starts |
| `tasks.md` | Task breakdown with `[ ]`/`[x]` checkboxes | Lead creates; agents check off | Start of phase |
| `progress.md` | Running log: completions, blockers, decisions | Lead updates as agents report | Throughout |
| `findings.md` | Post-phase learnings, gotchas, patterns | Lead writes | After phase completes |

No `agent-notes/` — with agent teams the lead coordinates directly via mailbox and task list.

---

## Execution Strategy

### Prerequisites (WSL Ubuntu)

```bash
sudo apt install tmux

# ~/.claude/settings.json:
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}

gh repo fork cyberjunky/python-garminconnect --clone=false
gh repo create garmin-connect-mcp-server --public --clone
cd garmin-connect-mcp-server && git checkout -b main
```

---

## Phase 0 — Scaffolding

**Branch:** `main` | **Owner:** Team Lead (single session)
**Docs:** `docs/initiatives/phase0-scaffolding/`

### Tasks

1. `uv init` + `uv add "mcp[cli]" garminconnect python-dotenv`
2. `uv add --dev pytest pytest-asyncio ruff`
3. Create full directory structure with all `__init__.py` and empty modules
4. Write `CLAUDE.md` with project conventions and file ownership
5. Write `docs/ARCHITECTURE.md`, `docs/DECISIONS.md` (ADR-001: Python over TS)
6. Write `docs/initiatives/overview.md` + phase0 docs (plan/tasks/progress/findings)
7. Write `docs/garmin-api-reference.md` — map all 64 tools to `garminconnect` methods
8. Write `.env.example`
9. Write `src/garmin_mcp/server.py` — bare FastMCP server with module imports
10. Write `src/garmin_mcp/auth.py` — auth wrapper with token caching
11. Write `src/garmin_mcp/client.py` — `GarminClient` class with ALL 64+ method stubs, organized by section comments
12. Write `tests/conftest.py` — mock fixtures
13. Write `pyproject.toml` with `[project.scripts] garmin-mcp = "garmin_mcp.server:main"`
14. Commit + push

### Acceptance Criteria

```bash
uv run python -c "from garmin_mcp.server import mcp; print('Server OK')"
uv run pytest tests/ -v
```

---

## Phase 1 — Tools Implementation (Parallel Agent Teams)

**Branches:** 5 feature branches (one per teammate)
**Owner:** Team Lead orchestrates 5 teammates via agent teams
**Docs:** `docs/initiatives/phase1-tools-parallel/`

### Launch

```bash
tmux new-session -s garmin-mcp
cd ~/garmin-connect-mcp-server
claude
```

Instruct the lead:

```
Read CLAUDE.md and PLAN.md. We are starting Phase 1.
Create phase1 docs (plan.md, tasks.md with per-agent checkboxes, progress.md, findings.md).
Then spawn 5 teammates with worktree isolation using Sonnet.
Require plan approval before any teammate makes changes.
All teammates must read CLAUDE.md before starting.
Update progress.md as agents report back.
```

### Teammate 1: Activities Agent (12 tools)

**Branch:** `feat/tools-activities`
**Owns:** `src/garmin_mcp/tools/activities.py`, `tests/test_tools_activities.py`
**Adds to** `client.py` under `# --- Activities methods ---`

| # | Tool | Params |
|---|------|--------|
| 1 | `get_activities` | `start=0, limit=10` |
| 2 | `get_activities_by_date` | `start_date, end_date, activity_type?` |
| 3 | `get_last_activity` | (none) |
| 4 | `count_activities` | (none) |
| 5 | `get_activity` | `activity_id` |
| 6 | `get_activity_details` | `activity_id` |
| 7 | `get_activity_splits` | `activity_id` |
| 8 | `get_activity_weather` | `activity_id` |
| 9 | `get_activity_hr_zones` | `activity_id` |
| 10 | `get_activity_exercise_sets` | `activity_id` |
| 11 | `get_activity_types` | (none) |
| 12 | `get_progress_summary` | `start_date, end_date` |

**Verification:** `uv run pytest tests/test_tools_activities.py -v`

### Teammate 2: Health Agent (14 tools)

**Branch:** `feat/tools-health`
**Owns:** `src/garmin_mcp/tools/health.py`, `tests/test_tools_health.py`
**Adds to** `client.py` under `# --- Health methods ---`

| # | Tool | Params |
|---|------|--------|
| 1 | `get_daily_summary` | `date` |
| 2 | `get_steps` | `date` |
| 3 | `get_steps_chart` | `date` |
| 4 | `get_heart_rate` | `date` |
| 5 | `get_resting_heart_rate` | `date` |
| 6 | `get_stress` | `date` |
| 7 | `get_body_battery` | `start_date, end_date` |
| 8 | `get_body_battery_events` | `date` |
| 9 | `get_respiration` | `date` |
| 10 | `get_spo2` | `date` |
| 11 | `get_intensity_minutes` | `date` |
| 12 | `get_floors` | `date` |
| 13 | `get_hydration` | `date` |
| 14 | `get_daily_events` | `date` |

**Verification:** `uv run pytest tests/test_tools_health.py -v`

### Teammate 3: Training + Trends + Analysis Agent (18 tools)

**Branch:** `feat/tools-training`
**Owns:** `src/garmin_mcp/tools/training.py`, `trends.py`, `analysis.py` + their tests
**Adds to** `client.py` under `# --- Training/Trends/Analysis methods ---`

**Performance & Training (11 tools):**

| # | Tool | Params |
|---|------|--------|
| 1 | `get_vo2max` | `date` |
| 2 | `get_training_readiness` | `date` |
| 3 | `get_training_status` | `date` |
| 4 | `get_hrv` | `date` |
| 5 | `get_endurance_score` | `start_date, end_date` |
| 6 | `get_hill_score` | `start_date, end_date` |
| 7 | `get_race_predictions` | (none) |
| 8 | `get_fitness_age` | `date` |
| 9 | `get_personal_records` | (none) |
| 10 | `get_lactate_threshold` | `latest=True` or `start_date, end_date` |
| 11 | `get_cycling_ftp` | (none) |

**Trends (4 tools):**

| # | Tool | Params |
|---|------|--------|
| 12 | `get_daily_steps_range` | `start_date, end_date` |
| 13 | `get_weekly_steps` | `date` |
| 14 | `get_weekly_stress` | `date` |
| 15 | `get_weekly_intensity_minutes` | `start_date, end_date` |

**Analysis (3 tools):**

| # | Tool | Params |
|---|------|--------|
| 16 | `compare_activities` | `activity_ids: list` (2-5) |
| 17 | `find_similar_activities` | `activity_id, limit=5` |
| 18 | `analyze_training_period` | `start_date, end_date` |

**Verification:** `uv run pytest tests/test_tools_training.py tests/test_tools_trends.py tests/test_tools_analysis.py -v`

### Teammate 4: Body + Sleep Agent (7 tools)

**Branch:** `feat/tools-body-sleep`
**Owns:** `src/garmin_mcp/tools/body.py`, `sleep.py` + their tests
**Adds to** `client.py` under `# --- Body/Sleep methods ---`

**Body Composition (5 tools):**

| # | Tool | Params |
|---|------|--------|
| 1 | `get_body_composition` | `start_date, end_date` |
| 2 | `get_latest_weight` | (none) |
| 3 | `get_daily_weigh_ins` | `date` |
| 4 | `get_weigh_ins` | `start_date, end_date` |
| 5 | `get_blood_pressure` | `start_date, end_date` |

**Sleep (2 tools):**

| # | Tool | Params |
|---|------|--------|
| 6 | `get_sleep_data` | `date` |
| 7 | `get_sleep_data_raw` | `date` |

**Verification:** `uv run pytest tests/test_tools_body.py tests/test_tools_sleep.py -v`

### Teammate 5: Profile + Resources + Prompts Agent (13 tools + 3 resources + 4 prompts)

**Branch:** `feat/resources-prompts-profile`
**Owns:** `src/garmin_mcp/tools/profile.py`, `resources/`, `prompts/` + their tests
**Adds to** `client.py` under `# --- Profile methods ---`

**Profile & Devices (13 tools):**

| # | Tool | Params |
|---|------|--------|
| 1 | `get_user_profile` | (none) |
| 2 | `get_user_settings` | (none) |
| 3 | `get_devices` | (none) |
| 4 | `get_device_settings` | `device_id` |
| 5 | `get_device_last_used` | (none) |
| 6 | `get_primary_training_device` | (none) |
| 7 | `get_gear` | (needs `profile_number` from `get_device_last_used`) |
| 8 | `get_gear_stats` | `gear_uuid` |
| 9 | `get_goals` | (none) |
| 10 | `get_earned_badges` | (none) |
| 11 | `get_workouts` | (none) |
| 12 | `get_workout` | `workout_id` |
| 13 | `get_activity_gear` | `activity_id` |

**Resources (3):**
- `garmin://athlete/profile`
- `garmin://training/readiness`
- `garmin://health/today`

**Prompts (4):**
- `analyze-recent-training`
- `sleep-quality-report`
- `training-readiness-check`
- `health-summary`

**Verification:** `uv run pytest tests/test_tools_profile.py tests/test_resources.py tests/test_prompts.py -v`

### Lead Responsibilities During Phase 1

- Create phase1 docs before spawning agents
- Update `progress.md` as agents report completions/blockers
- Resolve API questions about the `garminconnect` library
- Do NOT touch agent-owned files
- When all 5 report done → write `findings.md` → Phase 2

---

## Phase 2 — Integration & Merge

**Branch:** `main` | **Owner:** Team Lead (single session)
**Docs:** `docs/initiatives/phase2-integration/`

### Tasks

1. Create phase2 docs

2. Merge in order (minimizes `client.py` conflicts):
   ```
   feat/tools-activities       → main
   feat/tools-health           → main
   feat/tools-training         → main
   feat/tools-body-sleep       → main
   feat/resources-prompts-profile → main
   ```

3. Resolve `client.py` conflicts (additive only — keep all method blocks)

4. Wire up `server.py` — import and register all 7 tool modules + resources + prompts

5. Full test suite: `uv run pytest tests/ -v --tb=short`

6. Lint: `uv run ruff check src/ tests/ && uv run ruff format src/ tests/`

7. MCP Inspector smoke test: `uv run mcp dev src/garmin_mcp/server.py`

8. Verify no stdout leaks: `uv run garmin-mcp 2>/dev/null | head`

9. Write `findings.md`

### Acceptance Criteria

- All tests green
- MCP Inspector shows 64 tools, 3 resources, 4 prompts
- No stdout leaks

---

## Phase 3 — Fenix 8 AMOLED Polish & Ship

**Docs:** `docs/initiatives/phase3-fenix8-polish/`

### Track A: `feat/docs-docker`

- Comprehensive `README.md` (install, config for Claude Desktop / Claude Code / Cursor)
- `Dockerfile` (multi-stage, uv-based)
- `.github/workflows/ci.yml` (ruff + pytest on PR)
- Usage examples with natural language queries
- PyPI / uvx installability

### Track B: `feat/fenix8-features`

Fenix 8 AMOLED-specific tools (Phase 3 additions beyond the 64 core):

- `get_running_dynamics(activity_id)` — cadence, GCT, vertical oscillation, stride length, GCT balance
- `get_climbpro_data(activity_id)` — ClimbPro ascent details, remaining climb, gradient
- `get_trail_run_metrics(activity_id)` — trail-specific performance data
- `get_courses()` — downloaded courses and maps
- `get_running_power(activity_id)` — running power data
- `get_training_effect(activity_id)` — aerobic and anaerobic training effect
- `get_activity_power_zones(activity_id)` — power zone distribution

Device-specific resource:
- `garmin://device/fenix8` — device info, firmware, settings, battery level

**No solar tools** — Fenix 8 AMOLED does not have solar charging.

---

## Phase 4 — Connect to Claude

### Claude Desktop

```json
{
  "mcpServers": {
    "garmin": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/garmin-connect-mcp-server", "garmin-mcp"],
      "env": {
        "GARMIN_EMAIL": "your@email.com",
        "GARMIN_PASSWORD": "yourpass"
      }
    }
  }
}
```

### Claude Code

```bash
claude mcp add garmin \
  -e GARMIN_EMAIL=your@email.com \
  -e GARMIN_PASSWORD=yourpass \
  -- uv run --directory /path/to/garmin-connect-mcp-server garmin-mcp
```

### Docker

```json
{
  "mcpServers": {
    "garmin": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "--env-file", "/path/to/garmin.env",
               "-v", "/home/user/.garmin-mcp:/root/.garmin-mcp",
               "garmin-connect-mcp-server:latest"]
    }
  }
}
```

---

## CLAUDE.md

Place at project root. Loaded by every Claude Code session and teammate.

```markdown
# Garmin Connect MCP Server

## Project Context
Python MCP server exposing 64+ Garmin Connect tools from a Fenix 8 AMOLED via FastMCP.
Uses `garminconnect` library as the API adapter. Read-only in Phase 1 (no write/delete ops).

## Stack
- Python 3.11+ with `uv`
- `mcp[cli]` — FastMCP server
- `garminconnect` — Garmin Connect API wrapper (cyberjunky)
- `python-dotenv` — env vars
- `pytest` + `pytest-asyncio` — testing
- `ruff` — lint + format

## Architecture Rules
- **Thin tools, fat client**: Tools are thin wrappers. All API logic in `client.py`.
- **No stdout**: Logging via `logging` to stderr. `print()` forbidden in src/.
- **Type hints everywhere**: FastMCP uses them for schema generation.
- **Docstrings = tool descriptions**: Write as if explaining to an AI what the tool does.
- **ISO dates**: All date params `YYYY-MM-DD`.
- **Structured errors**: Return error dicts, never raise unhandled exceptions.
- **No solar tools**: Fenix 8 AMOLED has no solar.
- **Read-only Phase 1**: No write/delete operations exposed as tools.

## Docs Convention
Each phase in `docs/initiatives/<phase>/` has: `plan.md`, `tasks.md`, `progress.md`, `findings.md`.
See `docs/initiatives/overview.md` for initiative map.

## File Ownership (parallel agents)
- `tools/activities.py` → Activities Agent
- `tools/health.py` → Health Agent
- `tools/training.py`, `trends.py`, `analysis.py` → Training Agent
- `tools/body.py`, `sleep.py` → Body/Sleep Agent
- `tools/profile.py`, `resources/`, `prompts/` → Profile/Resources Agent
- `client.py` → ALL agents (additive only, under section comments)
- `server.py` → Team Lead only
- `tests/` → each agent owns corresponding test files

### Shared file protocol for client.py
Append methods under your section comment. Never modify other sections:
# --- Activities methods (activities agent) ---
# --- Health methods (health agent) ---
# --- Training methods (training agent) ---
# --- Trends methods (training agent) ---
# --- Analysis methods (training agent) ---
# --- Body methods (body/sleep agent) ---
# --- Sleep methods (body/sleep agent) ---
# --- Profile methods (profile agent) ---

## Code Patterns

### Tool definition
```python
@mcp.tool()
async def get_heart_rate(date: str) -> dict:
    """Get heart rate data for a specific date including resting HR, max HR, and time series.

    Use this when the user asks about their heart rate, pulse, or cardiovascular data
    for a particular day.

    Args:
        date: Date in YYYY-MM-DD format
    """
    client = await get_client()
    return await client.get_heart_rate(date)
```

### Client method
```python
async def get_heart_rate(self, date: str) -> dict:
    data = self._garmin.get_heart_rates(date)
    return {
        "date": date,
        "resting_heart_rate": data.get("restingHeartRate"),
        "max_heart_rate": data.get("maxHeartRate"),
        "heart_rate_zones": data.get("heartRateZones", []),
        "time_series": data.get("heartRateValues", [])
    }
```

### Test
```python
async def test_get_heart_rate(mock_garmin):
    client = GarminClient(mock_garmin)
    result = await client.get_heart_rate("2026-03-14")
    assert result["resting_heart_rate"] == 52
```

## Commands
- `uv run pytest tests/ -v` — all tests
- `uv run mcp dev src/garmin_mcp/server.py` — MCP Inspector
- `uv run garmin-mcp` — run server (stdio)
- `uv run ruff check src/ tests/` — lint
- `uv run ruff format src/ tests/` — format

## Git
- Branches: `feat/<scope>`
- Commits: conventional (`feat:`, `fix:`, `test:`, `docs:`)
- PRs: squash merge to main
```

---

## Agent Team Config (add to CLAUDE.md during Phase 1 only)

```markdown
## Agent Team Configuration (Phase 1 — remove after merge)

- **Activities Agent**: 12 tools. Owns `tools/activities.py` + test.
- **Health Agent**: 14 tools. Owns `tools/health.py` + test.
- **Training Agent**: 18 tools. Owns `tools/training.py`, `trends.py`, `analysis.py` + tests.
- **Body/Sleep Agent**: 7 tools. Owns `tools/body.py`, `sleep.py` + tests.
- **Profile/Resources Agent**: 13 tools + 3 resources + 4 prompts. Owns `tools/profile.py`, `resources/`, `prompts/` + tests.

Rules:
1. Read CLAUDE.md fully before starting
2. Only touch files you own
3. Append to `client.py` under your section comment only
4. Write tests for every tool
5. Run your tests before reporting done
6. Report to lead: tools count, tests passing, issues found
```

---

## tmux Session (WSL Ubuntu)

```bash
tmux new-session -s garmin-mcp
cd ~/garmin-connect-mcp-server
claude
# Agent teams auto-creates panes per teammate when tmux is available
```

---

## Reference Repos

| Repo | Role |
|------|------|
| [cyberjunky/python-garminconnect](https://github.com/cyberjunky/python-garminconnect) | API wrapper — core dep. 105+ methods, 1.8k stars. |
| [eddmann/garmin-connect-mcp](https://github.com/eddmann/garmin-connect-mcp) | Architecture ref — resources, prompts design. Python. |
| [Nicolasvegam/garmin-connect-mcp](https://github.com/Nicolasvegam/garmin-connect-mcp) | Tool inventory ref — 61 tools, good coverage. TypeScript. |
| [modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk) | Official MCP Python SDK. FastMCP API. |

---

## Success Criteria

- [ ] `uv run garmin-mcp` starts without errors
- [ ] MCP Inspector shows 64 tools, 3 resources, 4 prompts
- [ ] Activities: "Show me my runs from the last week"
- [ ] Health: "How did I sleep last night?"
- [ ] Training: "Am I ready to train hard today?"
- [ ] Trends: "Show my weekly step trend"
- [ ] Body: "What's my current weight?"
- [ ] Profile: "What gear am I tracking?"
- [ ] Resources auto-provide athlete profile and daily health
- [ ] All tests pass: `uv run pytest tests/ -v`
- [ ] Docker image builds and runs
- [ ] README has Claude Desktop, Claude Code, Cursor configs
- [ ] `docs/initiatives/` fully populated per phase
- [ ] `docs/DECISIONS.md` has key architectural choices