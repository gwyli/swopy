#!/bin/sh

ruff check --fix
ruff format
pytest --cov-report term-missing --cov=numberology
pytest --doctest-modules numberology/
pyright --verifytypes numberology

exit