# Phase 0 — Scaffolding

## Objective
Create the complete project skeleton: directory structure, all module stubs, configuration, documentation, and initial CLAUDE.md. The foundation that Phase 1 agents build on.

## Scope
- uv project initialization with all dependencies
- Full directory tree with `__init__.py` files
- `server.py` with bare FastMCP instance
- `auth.py` with token-caching authentication
- `client.py` with all 64+ method stubs organized by section comments
- `conftest.py` with mock fixtures
- `pyproject.toml` with entry point
- CLAUDE.md with project conventions and agent file ownership
- Docs skeleton (ARCHITECTURE.md, DECISIONS.md, API reference)
- GitHub repo creation and initial push

## Owner
Team Lead (single session — no agents needed)

## Acceptance Criteria
- `uv run python -c "from garmin_mcp.server import mcp; print('Server OK')"` passes
- `uv run pytest tests/ -v` passes (no test failures, empty tests OK)
- All directories and files from PLAN.md exist
- CLAUDE.md contains file ownership rules for Phase 1 agents
- GitHub repo exists with initial commit on main
