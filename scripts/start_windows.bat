@echo off
setlocal
cd /d %~dp0..

echo ==============================================
echo   CyberFusion - Local Security Console
echo ==============================================

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
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 (
  echo.
  echo Dependency installation failed.
  echo If Windows Device Guard blocks pip.exe, use this exact manual command:
  echo .venv\Scripts\python.exe -m pip install -r requirements.txt
  goto :error
)

echo [4/4] Starting CyberFusion...
start "CyberFusion API" cmd /k "cd /d %~dp0.. && .venv\Scripts\python.exe -m uvicorn backend.main:app --host 127.0.0.1 --port 8000"

echo Waiting for CyberFusion API...
set "READY="
for /L %%I in (1,1,20) do (
  powershell -NoProfile -Command "try { (Invoke-WebRequest -UseBasicParsing http://127.0.0.1:8000/api/health -TimeoutSec 1).StatusCode } catch { exit 1 }" >nul 2>&1
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
  echo CyberFusion is running at http://127.0.0.1:8000/
  echo Login: admin
  echo Password: ChangeMe123!
  exit /b 0
)

echo.
echo The API did not become ready within the expected time.
echo Check the CyberFusion API window for the startup error.
goto :error

:error
echo.
echo CyberFusion could not start. Check the message above.
pause
exit /b 1
