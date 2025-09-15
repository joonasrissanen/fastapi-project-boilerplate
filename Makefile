.PHONY: install hooks lint typecheck clean dev server

install:
	uv sync

hooks:
	uv run pre-commit install --install-hooks

lint:
	uv run ruff check --fix .

format:
	uv run ruff check --fix --select I .

typecheck:
	uv run pyright

test:
	uv run pytest -s -v tests

check: lint format typecheck test

infra-up:
	docker-compose up -d postgres

infra-down:
	docker-compose down -v

server:
	uv run fastapi dev

dev: infra-up server

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +

