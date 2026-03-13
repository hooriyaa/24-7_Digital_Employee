@echo off
REM =============================================================================
REM Customer Success Digital FTE - Start All Services
REM =============================================================================
REM This script:
REM 1. Installs all backend dependencies (including litellm)
REM 2. Seeds the database if empty
REM 3. Starts the backend server
REM 4. Starts the frontend development server
REM =============================================================================

setlocal enabledelayedexpansion

echo.
echo =============================================================================
echo  Customer Success Digital FTE - Starting All Services
echo =============================================================================
echo.

REM -----------------------------------------------------------------------------
REM Step 1: Install Backend Dependencies
REM -----------------------------------------------------------------------------
echo [1/5] Installing backend dependencies...
cd /d "%~dp0backend"

if exist ".venv" (
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
) else (
    echo Creating virtual environment...
    python -m venv .venv
    call .venv\Scripts\activate.bat
)

echo Installing dependencies with uv...
uv pip install -e .

REM Check if litellm is installed
python -c "import litellm" 2>nul
if errorlevel 1 (
    echo Installing litellm separately...
    uv pip install litellm
)

echo Backend dependencies installed successfully.
echo.

REM -----------------------------------------------------------------------------
REM Step 2: Check and Seed Database
REM -----------------------------------------------------------------------------
echo [2/5] Checking database status...
cd /d "%~dp0backend"

REM Run database migrations
echo Applying database migrations...
python -c "from app.database import run_migrations; import asyncio; asyncio.run(run_migrations())" 2>nul || echo Migration check completed.

REM Seed database if empty
echo Checking if database needs seeding...
python app\seed.py || echo Seed script completed or not available.
echo.

REM -----------------------------------------------------------------------------
REM Step 3: Start Backend Server
REM -----------------------------------------------------------------------------
echo [3/5] Starting backend server on http://localhost:8000...
cd /d "%~dp0backend"

start "Backend Server" cmd /k "cd /d %~dp0backend && .venv\Scripts\activate && uvicorn main:app --reload --host 0.0.0.0 --port 8000"

REM Wait for backend to start
echo Waiting for backend to initialize (10 seconds)...
timeout /t 10 /nobreak >nul
echo.

REM -----------------------------------------------------------------------------
REM Step 4: Install Frontend Dependencies (if needed)
REM -----------------------------------------------------------------------------
echo [4/5] Checking frontend dependencies...
cd /d "%~dp0frontend"

if not exist "node_modules" (
    echo Installing frontend dependencies...
    call npm install
) else (
    echo Frontend dependencies already installed.
)
echo.

REM -----------------------------------------------------------------------------
REM Step 5: Start Frontend Server
REM -----------------------------------------------------------------------------
echo [5/5] Starting frontend server on http://localhost:3000...
cd /d "%~dp0frontend"

start "Frontend Server" cmd /k "cd /d %~dp0frontend && npm run dev"

REM -----------------------------------------------------------------------------
REM Completion
REM -----------------------------------------------------------------------------
echo.
echo =============================================================================
echo  All Services Started Successfully!
echo =============================================================================
echo.
echo  Backend API:  http://localhost:8000
echo  API Docs:     http://localhost:8000/docs
echo  Frontend:     http://localhost:3000
echo.
echo  Two terminal windows have been opened:
echo  - Backend Server (running FastAPI with uvicorn)
echo  - Frontend Server (running Next.js development server)
echo.
echo  To stop the servers, close the terminal windows or press Ctrl+C in each.
echo =============================================================================
echo.

endlocal
