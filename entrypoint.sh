#!/bin/sh

# Для прогонки миграций
#poetry run alembic -c ./src/auth/alembic.ini revision --autogenerate -m "init"
poetry run alembic -c ./src/auth/alembic.ini upgrade head

poetry run uvicorn src.auth.main.main:app --host ${app_host} --port ${app_port} --reload

