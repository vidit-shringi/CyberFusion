@echo off
setlocal EnableExtensions
cd /d "%~dp0.."

echo ==============================================
echo   CyberFusion - Local Security Intelligence
echo ==============================================
echo.

where python >nul 2>&1
if errorlevel 1 (
  echo ERROR: Python was not found in PATH.
  echo Install Python 3.12 and enable "Add Python to PATH".
  goto :error
)

if not exist .venv (
  echo [1/4] Creating Python virtual environment...
  python -m venv .venv
  if errorlevel 1 goto :error
) else (
  echo [1/4] Virtual environment already exists.
)

if not exist .env (
  echo [2/4] Creating local configuration...
  copy /Y .env.example .env >nul
  if errorlevel 1 goto :error
) else (
  echo [2/4] Local configuration already exists.
)

echo [3/4] Installing Python dependencies...
echo Using Python module invocation to avoid direct pip.exe execution.
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 (
  echo.
  echo Dependency installation failed.
  echo.
  echo If Windows reports Device Guard / App Control blocking pip.exe,
  echo DO NOT run pip.exe directly. Run:
  echo   .venv\Scripts\python.exe -m pip install -r requirements.txt
  echo.
  echo If your organization blocks Python package installation entirely,
  echo use the Docker deployment path instead.
  goto :error
)

echo [4/4] Starting CyberFusion...
start "CyberFusion API" cmd /k "cd /d %~dp0.. && .venv\Scripts\python.exe -m uvicorn backend.main:app --host 127.0.0.1 --port 8000"

echo Waiting for CyberFusion API...
set "READY="
for /L %%I in (1,1,30) do (
  powershell -NoProfile -Command "try { if ((Invoke-WebRequest -UseBasicParsing http://127.0.0.1:8000/api/health -TimeoutSec 1).StatusCode -eq 200) { exit 0 } else { exit 1 } } catch { exit 1 }" >nul 2>&1
  if not errorlevel 1 (
    set "READY=1"
    goto :ready
  )
  timeout /t 1 /nobreak >nul
)

:ready
if defined READY (
  start "" http://127.0.0.1:8000/
  echo.
  echo ==============================================
  echo CyberFusion is RUNNING
  echo URL      : http://127.0.0.1:8000/
  echo API Docs : http://127.0.0.1:8000/docs
  echo Health   : http://127.0.0.1:8000/api/health
  echo.
  echo Local administrator credentials:
  echo Username : admin
  echo Password : ChangeMe123!
  echo ==============================================
  echo.
  echo Keep the CyberFusion API window open while using the console.
  exit /b 0
)

echo.
echo The API did not become ready within 30 seconds.
echo Check the CyberFusion API window for the exact startup error.
goto :error

:error
echo.
echo CyberFusion could not start.
echo Read the error above and see README.md - Troubleshooting.
pause
exit /b 1
