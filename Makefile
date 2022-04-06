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

# Settings
.DEFAULT_GOAL = help


help:
	@echo "---------------HELP---------------------------"
	@echo "Manage $(PROJECT_NAME). Usage:"
	@echo "make test    - Test."
	@echo "make clean   - Clean build directories, temporary files, and caches."
	@echo "make build   - Build with setup.py."
	@echo "make release - Deploy to PyPi."
	@echo "----------------------------------------------"

venv:
	$(PYTHON) -m venv $(VENV_DIR)
	${VENV_BIN}/pip install --upgrade pip
	$(VENV_BIN)/pip install --upgrade -r requirments.txt
	$(VENV_BIN)/pip install --upgrade -r requirments-dev.txt

test:
	@echo "Testing $(PROJECT_NAME)."
	${VENV_BIN}/pip install --upgrade pip
	${VENV_BIN}/pip install tox tox-gh-actions
	${VENV_BIN}/tox

clean:
	@echo "Removing temporary files and caches."
	# Build Directories
	rm -rf build/
	rm -rf dist/
	# Temporary Files
	rm -rf **/__pycache__/
	rm -rf **/*.egg-info/

build:
	@echo "Building $(PROJECT_NAME)."
	# Build
	${VENV_BIN}/python setup.py sdist bdist_wheel

release: clean build
	@echo "Deploying $(PROJECT_NAME) to PyPi."
	${VENV_BIN}/pip install --upgrade twine
	${VENV_BIN}/python -m twine upload dist/*
