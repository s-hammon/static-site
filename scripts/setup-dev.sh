#!/bin/bash

# Install Ruff, a Python linter
if [ ! -x "$(command -v ruff)" ]; then
    curl -LsSf https://astral.sh/ruff/install.sh | sh
else
    # get installed Ruff version
    INSTALLED_RUFF_VERSION=$(ruff --version)
    echo "Ruff version: $INSTALLED_RUFF_VERSION (already installed)"
fi