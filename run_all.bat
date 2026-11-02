@echo off
setlocal
cd /d "%~dp0"
py run_all.py
if errorlevel 1 (
  echo.
  echo Project execution failed. Read the error above.
  pause
  exit /b 1
)
echo.
echo Project completed. See results\PROJECT_REPORT.md
pause
