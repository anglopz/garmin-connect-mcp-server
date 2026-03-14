# Architecture

## Data Flow

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

## Key Design Decisions

### Thin Tools, Fat Client
Tool functions are one-line async wrappers that call `GarminClient` methods. All data transformation, error handling, and API interaction lives in the client. This keeps tools testable and the server module clean.

### Singleton Client
`get_client()` returns a module-level singleton. Authentication happens lazily on first tool call, using cached OAuth tokens when available.

### No stdout
The MCP stdio transport uses stdout for JSON-RPC messages. All logging goes to stderr via Python's `logging` module. `print()` is forbidden in `src/`.

### Structured Returns
All client methods return dicts or lists of dicts. Never raw API responses — always transform to a consistent shape with meaningful keys.

### Module Registration
Tool modules register with the server by importing `mcp` from `server.py` and using `@mcp.tool()` decorators. Importing the module in `server.py` is enough to register all its tools.

## Directory Layout

- `src/garmin_mcp/server.py` — FastMCP instance, module imports, `main()` entry point
- `src/garmin_mcp/auth.py` — Garmin Connect authentication with token caching
- `src/garmin_mcp/client.py` — `GarminClient` adapter with all API methods
- `src/garmin_mcp/tools/` — MCP tool definitions, one file per domain
- `src/garmin_mcp/resources/` — MCP resources (auto-provided context)
- `src/garmin_mcp/prompts/` — MCP prompts (analysis templates)
- `tests/` — pytest tests, one file per module
- `scripts/` — utility scripts for auth setup and inspection
