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
) else (
  echo [2/4] Local configuration already exists.
)

echo [3/4] Installing Python dependencies...
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 (
  echo.
  echo Dependency installation failed.
  echo If Windows Device Guard blocks pip.exe, this launcher uses Python -m pip to avoid direct pip.exe execution.
  goto :error
)

echo [4/4] Starting CyberFusion...
start "CyberFusion API" cmd /k "cd /d %~dp0.. && .venv\Scripts\python.exe -m uvicorn backend.main:app --host 127.0.0.1 --port 8000"
timeout /t 2 /nobreak >nul
start "" http://127.0.0.1:8000/
echo.
echo CyberFusion is running at http://127.0.0.1:8000/
exit /b 0

:error
echo.
echo CyberFusion could not start. Check the message above.
pause
exit /b 1
