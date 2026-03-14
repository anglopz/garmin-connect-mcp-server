# Architecture Decision Records

## ADR-001: Python over TypeScript

**Status:** Accepted
**Date:** 2026-03-14

### Context
The garmin-connect-mcp ecosystem has implementations in both TypeScript and Python. We need to choose a language for this server.

### Decision
Python, using the official MCP Python SDK (`mcp[cli]` / FastMCP).

### Rationale
- `garminconnect` (cyberjunky) is the most mature Garmin API wrapper — Python-only, 1.8k stars
- FastMCP's decorator-based API (`@mcp.tool()`) with type hints auto-generates JSON schemas
- Python docstrings become tool descriptions with zero extra work
- The target user (Fenix 8 AMOLED owner) benefits from the data science ecosystem for future analysis tools
- `uv` makes Python dependency management fast and reproducible

### Alternatives Considered
- **TypeScript**: Nicolasvegam's garmin-connect-mcp has 61 tools but uses a less mature Garmin API library
- **Go**: No mature Garmin Connect API wrapper exists

## ADR-002: Read-Only in Phase 1

**Status:** Accepted
**Date:** 2026-03-14

### Context
The `garminconnect` library supports write operations (delete activities, upload workouts, set weigh-ins).

### Decision
Phase 1 exposes only read operations. No write/delete tools.

### Rationale
- MCP tools are invoked by AI — accidental deletion or modification is a real risk
- Read-only is safe to iterate on rapidly
- Write operations can be added in a future phase with confirmation prompts

## ADR-003: Lazy Authentication

**Status:** Accepted
**Date:** 2026-03-14

### Context
Garmin Connect requires OAuth authentication. The server starts via stdio transport before any tool call.

### Decision
Authenticate on first tool call, not on server startup. Cache tokens in `~/.garmin-mcp/`.

### Rationale
- Server starts instantly (important for MCP client UX)
- Token caching avoids repeated logins
- Failed auth surfaces as a clear tool error, not a startup crash

## ADR-004: No Solar Tools

**Status:** Accepted
**Date:** 2026-03-14

### Context
The `garminconnect` library has `get_device_solar_data()`.

### Decision
Exclude solar tools entirely.

### Rationale
- Target device is Fenix 8 AMOLED, which does not have solar charging
- Including it would confuse users and return empty/error data
