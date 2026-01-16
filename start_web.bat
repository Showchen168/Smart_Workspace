@echo off
chcp 65001 >nul 2>&1
echo ====================================
echo    Smart Workspace
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [Error] Python not found, please install Python 3.8+
    pause
    exit /b 1
)

REM Check .env file
if not exist .env (
    echo [Warning] .env file not found
    echo Creating from .env.example...
    copy .env.example .env
    echo.
    echo [Important] Please edit .env file and add your GEMINI_API_KEY
    echo.
    pause
)

REM Check dependencies
echo Checking dependencies...
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo [Info] Installing dependencies...
    pip install -r requirements.txt
)

REM Start application
echo.
echo Starting Smart Workspace...
echo Open browser: http://localhost:5000
echo.
python app.py

pause
