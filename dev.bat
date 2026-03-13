@echo off
REM ===========================================
REM Customer Success Digital FTE - Dev Launcher
REM ===========================================
REM Opens two terminals:
REM   1. Backend (FastAPI on port 8000)
REM   2. Frontend (Next.js on port 3000)
REM ===========================================

echo Starting Customer Success Digital FTE Development Environment...
echo.

REM Get script directory
set SCRIPT_DIR=%~dp0

REM Start Backend Terminal
echo Starting Backend (FastAPI)...
start "Backend - FastAPI" cmd /k "cd %SCRIPT_DIR%backend && uv run uvicorn main:app --reload --port 8000"

REM Wait a moment for backend to start
timeout /t 3 /nobreak > nul

REM Start Frontend Terminal
echo Starting Frontend (Next.js)...
start "Frontend - Next.js" cmd /k "cd %SCRIPT_DIR%frontend && npm run dev"

echo.
echo ===========================================
echo Development servers starting...
echo ===========================================
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Press any key to exit this window...
pause > nul
