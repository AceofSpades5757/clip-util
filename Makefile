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
.PHONY: help test build clean publish


help:
	@echo "---------------HELP---------------------------"
	@echo "Manage $(PROJECT_NAME). Usage:"
	@echo "make test    - Test."
	@echo "make clean   - Clean build directories, temporary files, and caches."
	@echo "make build   - Build with setup.py."
	@echo "make publish - Publish to PyPi."
	@echo "----------------------------------------------"

venv: $(VENV_DIR)

$(VENV_DIR):
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install --upgrade virtualenv
	$(PYTHON) -m virtualenv $(VENV_DIR)
	-$(VENV_PYTHON) -m pip install --upgrade pip
	$(VENV_PYTHON) -m pip install --upgrade -r requirements.txt
	$(VENV_PYTHON) -m pip install --upgrade -r dev-requirements.txt

test: venv
	@echo "Testing $(PROJECT_NAME)."
	$(VENV_BIN)/tox

clean:
	@echo "Removing temporary files and caches."
	# Virtual Environment
	rm -rf $(VENV_DIR)
	# Build Directories
	rm -rf build/
	rm -rf dist/
	# Temporary Files
	rm -rf **/__pycache__/
	rm -rf **/*.egg-info/

build: venv
	@echo "Building $(PROJECT_NAME)."
	# Build
	$(VENV_PYTHON) setup.py sdist bdist_wheel

publish: build
	@echo "Publishing $(PROJECT_NAME) to PyPi."
	$(VENV_PYTHON) -m pip install --upgrade twine
	$(VENV_PYTHON) -m twine upload dist/*
