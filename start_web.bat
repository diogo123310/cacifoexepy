@echo off
title Locker System - Web Interface
echo.
echo ================================================
echo    LOCKER SYSTEM - WEB INTERFACE AUTO-START
echo ================================================
echo.

cd /d "%~dp0"

echo 🔍 Checking Python virtual environment...
if exist ".venv\Scripts\python.exe" (
    echo ✅ Virtual environment found
    set PYTHON_CMD=.venv\Scripts\python.exe
) else (
    echo ⚠️  Virtual environment not found, using system Python
    set PYTHON_CMD=python
)

echo.
echo 🚀 Starting web interface...
echo.
echo 📱 Web Interface will open at: http://localhost:5000
echo 🌐 Network access: http://YOUR_IP:5000
echo 🛑 Press Ctrl+C to stop the server
echo.
echo ================================================

%PYTHON_CMD% database_api.py

echo.
echo 👋 Web interface stopped.
pause