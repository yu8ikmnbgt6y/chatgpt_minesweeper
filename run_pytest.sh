#!/bin/bash

# Activate the virtual environment
source venv/bin/activate

# Run pytest with the specified options
pytest --cov=src --cov-report=html:htmlcov tests/

# Deactivate the virtual environment
deactivate