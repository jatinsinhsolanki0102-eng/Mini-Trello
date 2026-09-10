@echo off
title Mini-Trello - Installing Dependencies
echo ============================================
echo   Mini-Trello - First Time Setup
echo ============================================
echo.

echo [1/3] Checking Python...
where python >nul 2>nul
if errorlevel 1 (
    echo.
    echo ERROR: Python not found.
    echo Install Python 3.9+ from https://www.python.org/downloads/
    echo IMPORTANT: tick "Add Python to PATH" during installation.
    pause
    exit /b 1
)
echo       Python found.
echo.

echo [2/3] Installing backend dependencies (pip install)...
cd /d "%~dp0backend"
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo ERROR: Backend install failed. Check your internet connection and try again.
    pause
    exit /b 1
)
echo       Backend dependencies installed.
echo.

echo [3/3] Installing frontend dependencies (npm install)...
echo       Checking Node.js...
where node >nul 2>nul
if errorlevel 1 (
    echo.
    echo ERROR: Node.js not found.
    echo Install Node.js 18+ from https://nodejs.org/
    pause
    exit /b 1
)
echo       Node.js found. Installing, please wait...
cd /d "%~dp0frontend"
call npm install --no-audit --no-fund
if errorlevel 1 (
    echo.
    echo ERROR: Frontend install failed. Check your internet connection and try again.
    pause
    exit /b 1
)
echo.

if not exist "%~dp0frontend\node_modules\.bin\vite.cmd" (
    echo.
    echo ERROR: vite was not installed successfully.
    echo Try:  cd frontend   then   npm install
    pause
    exit /b 1
)

echo ============================================
echo   Setup Complete!
echo   Now double-click START.bat to run the app.
echo ============================================
pause