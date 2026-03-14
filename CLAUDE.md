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
```
# --- Activities methods (activities agent) ---
# --- Health methods (health agent) ---
# --- Training methods (training agent) ---
# --- Trends methods (training agent) ---
# --- Analysis methods (training agent) ---
# --- Body methods (body/sleep agent) ---
# --- Sleep methods (body/sleep agent) ---
# --- Profile methods (profile agent) ---
```

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
