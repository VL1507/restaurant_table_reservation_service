# app
runapp:
	uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

format:
	uv run ruff check --select I --fix
	uv run ruff format .

format_check:
	uv run ruff check

test:
	uv run pytest

type_check:
	uv run mypy . --explicit-package-bases

precommit:
	make format_check
	make test
	make type_check