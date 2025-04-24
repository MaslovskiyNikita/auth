#!/bin/sh

echo "Applying database migrations..."
poetry run alembic upgrade head

echo "Checking for schema changes..."
poetry run alembic revision --autogenerate -m "auto_$(date +%Y%m%d_%H%M%S)" || echo "No changes detected"

echo "Applying new migrations if any..."
poetry run alembic upgrade head

echo "Starting application server..."
poetry run uvicorn src.auth.main.main:app --host ${app_host} --port ${app_port} --reload

