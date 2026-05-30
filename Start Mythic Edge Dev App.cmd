@echo off
setlocal

set "REPO_ROOT=%~dp0"
set "FRONTEND_URL=http://127.0.0.1:5173"

pushd "%REPO_ROOT%" >nul
if errorlevel 1 (
  echo Could not open the Mythic Edge repo folder.
  pause
  exit /b 1
)

echo Checking whether Mythic Edge is already running...
powershell -NoProfile -ExecutionPolicy Bypass -Command "$ErrorActionPreference = 'Stop'; $response = Invoke-WebRequest -Uri '%FRONTEND_URL%' -UseBasicParsing -TimeoutSec 2; if ($response.StatusCode -ge 200 -and $response.StatusCode -lt 500) { exit 0 }; exit 1" >nul 2>nul
if not errorlevel 1 (
  echo Mythic Edge is already running.
  echo Opening %FRONTEND_URL% ...
  start "" "%FRONTEND_URL%"
  echo.
  echo This window can be closed. The existing app process will keep running.
  popd >nul
  pause
  exit /b 0
)

echo Starting Mythic Edge local developer app...
echo.
echo Backend:  http://127.0.0.1:8765
echo Frontend: %FRONTEND_URL%
echo.
echo Press Ctrl+C in this window to stop the app.
echo.

powershell -NoProfile -ExecutionPolicy Bypass -File "tools\dev_app\start_mythic_edge_dev_app.ps1" -Start
set "EXIT_CODE=%ERRORLEVEL%"

popd >nul
echo.
echo Mythic Edge local developer app stopped.
pause
exit /b %EXIT_CODE%
