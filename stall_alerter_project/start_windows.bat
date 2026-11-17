@echo off
setlocal
cd /d "%~dp0"
echo Hiring Stall Alerter - Windows launcher
if not exist ".venv\Scripts\python.exe" (
    echo Creating a local Python environment...
    py -3 -m venv .venv 2>nul
    if errorlevel 1 python -m venv .venv
    if errorlevel 1 goto fail
)
echo Installing required Python packages...
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto fail
echo Starting the dashboard. Keep this window open while you use it.
".venv\Scripts\python.exe" -m streamlit run app.py
if errorlevel 1 goto fail
exit /b 0
:fail
echo.
echo Setup could not finish. Check that Python is installed and your internet is connected.
pause
exit /b 1
