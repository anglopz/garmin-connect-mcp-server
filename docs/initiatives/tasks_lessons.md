# Cross-Phase Lessons

This file accumulates patterns and gotchas discovered across phases.

## Phase 0
- `uv` may not be on PATH in fresh WSL environments — install and export PATH
- `pytest-asyncio` needs `asyncio_mode = "auto"` in pyproject.toml
