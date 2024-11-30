#!/bin/bash

# Install Ruff, a Python linter
if [ ! -x "$(command -v ruff)" ]; then
    curl -LsSf https://astral.sh/ruff/install.sh | sh
else
    # get installed Ruff version
    INSTALLED_RUFF_VERSION=$(ruff --version)
    echo "Ruff version: $INSTALLED_RUFF_VERSION (already installed)"
fi

# Install the Coverage.py package
# TODO: get pip executable path
if [ ! -x "$(command -v coverage)" ]; then
    pip install coverage
else
    # get installed Coverage.py version
    INSTALLED_COVERAGE_VERSION=$(pip show coverage | grep Version | awk '{print $2}')
    echo "Coverage.py version: $INSTALLED_COVERAGE_VERSION (already installed)"
fi