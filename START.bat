@echo off
title Mini-Trello - Starting Servers
echo ============================================
echo   Mini-Trello - Starting Application
echo ============================================
echo.
set "ROOT=%~dp0"

REM ----- Dependency checks (run INSTALL.bat once first) -----
pip show flask >nul 2>nul
if errorlevel 1 (
    echo Backend packages are missing.
    echo Please run INSTALL.bat once first, then start again.
    echo.
    pause
    exit /b 1
)
if not exist "%ROOT%frontend\node_modules\.bin\vite.cmd" (
    echo Frontend packages are missing.
    echo Please run INSTALL.bat once first, then start again.
    echo.
    pause
    exit /b 1
)

REM ----- 1) Backend (Flask) -----
echo [1/2] Starting Backend (Flask) on http://127.0.0.1:5000
start "Mini-Trello Backend" cmd /k "cd /d ""%ROOT%backend"" && python run.py"
echo.

REM ----- 2) Frontend (React + Vite) -----
echo [2/2] Starting Frontend (React) on http://localhost:5173
start "Mini-Trello Frontend" cmd /k "cd /d ""%ROOT%frontend"" && npm run dev"
echo.

REM ----- Wait for servers, then open the browser automatically -----
timeout /t 4 /nobreak >nul
echo Opening browser at http://localhost:5173 ...
start "" http://localhost:5173

echo.
echo ============================================
echo   Both servers are running.
echo   If a browser tab did not open, go to:
echo     http://localhost:5173
echo   Backend API: http://127.0.0.1:5000/api/tasks
echo   To STOP the app: close the two server windows.
echo ============================================
pause