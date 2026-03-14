Run the full build verification: lint, format check, and all tests.

```bash
uv run ruff check src/ tests/
uv run ruff format --check src/ tests/
uv run pytest tests/ -v --tb=short
```
