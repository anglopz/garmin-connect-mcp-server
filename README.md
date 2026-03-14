# Garmin Connect MCP Server

A read-only [Model Context Protocol](https://modelcontextprotocol.io/) server that exposes 64+ Garmin Connect tools via [FastMCP](https://github.com/jlowin/fastmcp). Built for the **Fenix 8 AMOLED** and designed to give LLMs full access to your fitness, health, and training data.

## Features

- **64+ tools** across 8 categories -- activities, health, training, trends, analysis, body composition, sleep, and profile/devices
- **3 resources** providing auto-loaded context (athlete profile, daily health, training readiness)
- **4 prompts** with pre-built analysis templates (training analysis, sleep report, readiness check, health summary)
- **OAuth token caching** -- authenticate once, tokens persist in `~/.garmin-mcp/`
- **stdio transport** -- works with Claude Desktop, Claude Code, and any MCP-compatible client
- **Read-only** -- no write or delete operations, safe to use with your real account

## Quick Start

```bash
# Clone and install
git clone https://github.com/YOUR_USERNAME/garmin-connect-mcp-server.git
cd garmin-connect-mcp-server
uv sync

# Set credentials
cp .env.example .env
# Edit .env with your Garmin Connect email and password

# Run the server
uv run garmin-mcp
```

## Installation

### With uv (recommended)

```bash
uv sync
```

### With pip

```bash
pip install -e .
```

### With Docker

```bash
docker build -t garmin-connect-mcp-server .
```

## Configuration

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GARMIN_EMAIL` | Yes (first run) | -- | Your Garmin Connect email |
| `GARMIN_PASSWORD` | Yes (first run) | -- | Your Garmin Connect password |
| `GARMIN_TOKEN_DIR` | No | `~/.garmin-mcp/` | Directory for cached OAuth tokens |

After the first successful authentication, tokens are cached and credentials are no longer required until the tokens expire.

## Usage

### Claude Desktop

Add to your Claude Desktop configuration (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS, `%APPDATA%\Claude\claude_desktop_config.json` on Windows):

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

Build the image, then add to your MCP client configuration:

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

The volume mount persists your OAuth tokens between container runs.

## Tool Reference

| Category | Tools | Description |
|----------|-------|-------------|
| **Activities** | 12 | Activity list, details, splits, weather, HR zones, exercise sets, progress |
| **Health** | 14 | Daily summary, steps, heart rate, stress, body battery, respiration, SpO2, floors, hydration |
| **Profile** | 13 | User profile, settings, devices, gear, goals, badges, workouts |
| **Training** | 11 | VO2max, training readiness/status, HRV, endurance/hill score, race predictions, FTP |
| **Body** | 5 | Body composition, weight, weigh-ins, blood pressure |
| **Trends** | 4 | Daily/weekly steps, weekly stress, intensity minutes |
| **Analysis** | 3 | Compare activities, find similar, analyze training period |
| **Sleep** | 2 | Sleep data (structured), sleep data (raw) |

## Resources

Resources are auto-loaded context that MCP clients can attach to conversations.

| URI | Description |
|-----|-------------|
| `garmin://athlete/profile` | Athlete profile with age, weight, and training zones |
| `garmin://health/today` | Today's health snapshot (steps, stress, body battery, sleep) |
| `garmin://training/readiness` | Current training readiness score and contributing factors |

## Prompts

Prompts are pre-built analysis templates that guide the LLM through structured data retrieval and analysis.

| Prompt | Description |
|--------|-------------|
| `analyze-recent-training` | Analyze training load, recovery, and performance over a period |
| `sleep-quality-report` | Multi-day sleep quality analysis with trends and recommendations |
| `training-readiness-check` | Readiness assessment combining HRV, sleep, stress, and recovery |
| `health-summary` | Comprehensive daily health overview across all metrics |

## Development

```bash
# Clone and install with dev dependencies
git clone https://github.com/YOUR_USERNAME/garmin-connect-mcp-server.git
cd garmin-connect-mcp-server
uv sync

# Run linter
uv run ruff check src/ tests/
uv run ruff format --check src/ tests/

# Run tests
uv run pytest

# Interactive auth setup (caches tokens for development)
uv run python scripts/setup_auth.py

# Launch MCP Inspector for debugging
./scripts/inspect.sh
```

## Architecture

```
Claude / LLM Client
    | (MCP stdio transport)
FastMCP Server (server.py)
    | (tool / resource / prompt dispatch)
Tool Functions (tools/*.py)       Resources (resources/*.py)
    |                                  |
GarminClient (client.py) -- single adapter, all Garmin API logic
    |
Auth Module (auth.py) -- lazy auth, token cache in ~/.garmin-mcp/
    |
garminconnect library (Garth OAuth)
    |
Garmin Connect API
```

**Thin tools, fat client** -- tool functions are one-line async wrappers. All data transformation, error handling, and API logic lives in `GarminClient`. This keeps tools simple and the codebase testable.

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed design decisions.

## License

MIT
