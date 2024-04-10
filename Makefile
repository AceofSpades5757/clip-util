# Variables
PROJECT_NAME = clip-util
VENV_DIR = .venv

ifeq ($(OS),Windows_NT)
	PYTHON = py
	VENV_BIN = ./.venv/Scripts
else
	PYTHON = python3
	VENV_BIN = ./.venv/bin
endif
VENV_PYTHON = $(VENV_BIN)/python

# Settings
.DEFAULT_GOAL = help
.PHONY: help test build clean mostlyclean publish format format-update type


help:
	@echo "---------------HELP---------------------------"
	@echo "Manage $(PROJECT_NAME). Usage:"
	@echo "make test        - Test."
	@echo "make mostlyclean - Clean temporary files, and caches."
	@echo "make clean       - Clean all."
	@echo "make build       - Build with setup.py."
	@echo "make publish     - Publish to PyPi."
	@echo ""
	@echo "make format         - Run formatters."
	@echo "make format-update  - Update formatters."
	@echo "make type           - Run type checkers."
	@echo "----------------------------------------------"

venv: $(VENV_DIR)

$(VENV_DIR):
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install --upgrade virtualenv
	$(PYTHON) -m virtualenv $(VENV_DIR)
	$(VENV_PYTHON) -m pip install --upgrade pip
	$(VENV_PYTHON) -m pip install --editable .[dev]

test: venv
	@echo "Testing $(PROJECT_NAME)."
	$(VENV_BIN)/tox

mostlyclean:
	@echo "Removing temporary files and caches."
	# Build Directories
	rm -rf build/
	rm -rf dist/
	# Temporary Files and Caches
	rm -rf **/__pycache__/
	rm -rf **/*.egg-info/
	rm -rf .mypy_cache

clean: mostlyclean
	@echo "Removing temporary files and caches."
	# Virtual Environment
	rm -rf $(VENV_DIR)

build: venv
	@echo "Building $(PROJECT_NAME)."
	# Build
	$(VENV_PYTHON) setup.py sdist bdist_wheel

publish: build
	@echo "Publishing $(PROJECT_NAME) to PyPi."
	$(VENV_PYTHON) -m pip install --upgrade twine
	$(VENV_PYTHON) -m twine upload dist/*

format: venv
	$(VENV_BIN)/pre-commit run --all-files

format-update: venv
	$(VENV_BIN)/pre-commit autoupdate

type: venv
	$(VENV_BIN)/mypy ./src
