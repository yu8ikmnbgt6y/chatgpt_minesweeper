@echo off

REM Change the working directory to the script's location
cd %~dp0

REM Activate the virtual environment
call venv\Scripts\activate

REM Run pytest with the specified options
python -m pytest --cov=src --cov-report=html:htmlcov tests/

REM Deactivate the virtual environment
call venv\Scripts\deactivate.bat

pause