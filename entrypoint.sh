#!/bin/sh

poetry run uvicorn auth.main:app --host ${app_host} --port ${app_port} --reload