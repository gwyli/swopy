#!/bin/sh

# Upgrades the Python version
# Steps:
# 1. Run this script
# 2. Run sh bin/checks.sh to ensure everything is working
# 3. Commit the changes and push

deactivate || true
uv self update
. .venv/bin/activate
uv python upgrade "$1"
uv python pin "$1"
uv sync --all-groups