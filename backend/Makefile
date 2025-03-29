# app
runapp:
	uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

format:
	uv run ruff check --select I --fix
	uv run ruff format .

format_check:
	uv run ruff check

testapp:
	uv run pytest

type:
	uv run mypy . --explicit-package-bases