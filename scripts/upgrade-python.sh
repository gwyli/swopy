#!/bin/sh

deactivate || true
uv self update
. .venv/bin/activate
uv python upgrade
uv python pin "$1"
uv sync --all-groups