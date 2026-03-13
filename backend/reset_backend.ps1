# =============================================================================
# Customer Success Digital FTE - Backend Environment Reset Script
# =============================================================================
# This script completely rebuilds the Python virtual environment and installs
# all required dependencies from scratch.
#
# Usage:
#   cd backend
#   .\reset_backend.ps1
# =============================================================================

Write-Host "=============================================================================" -ForegroundColor Cyan
Write-Host "  Customer Success Digital FTE - Backend Environment Reset" -ForegroundColor Cyan
Write-Host "=============================================================================" -ForegroundColor Cyan
Write-Host ""

# Get the script directory (backend folder)
$BackendDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $BackendDir

Write-Host "Working directory: $BackendDir" -ForegroundColor Gray
Write-Host ""

# =============================================================================
# Step 1: Remove existing virtual environment
# =============================================================================
Write-Host "[1/6] Removing existing virtual environment..." -ForegroundColor Yellow

if (Test-Path ".venv") {
    Remove-Item -Recurse -Force ".venv"
    Write-Host "  Deleted .venv folder" -ForegroundColor Green
} else {
    Write-Host "  No existing .venv found" -ForegroundColor Gray
}
Write-Host ""

# =============================================================================
# Step 2: Create fresh virtual environment
# =============================================================================
Write-Host "[2/6] Creating fresh virtual environment..." -ForegroundColor Yellow

python -m venv .venv

if (Test-Path ".venv\Scripts\python.exe") {
    Write-Host "  Virtual environment created successfully" -ForegroundColor Green
} else {
    Write-Host "  Failed to create virtual environment" -ForegroundColor Red
    Write-Host "  Make sure Python 3.11+ is installed" -ForegroundColor Red
    exit 1
}
Write-Host ""

# =============================================================================
# Step 3: Ensure pip is available
# =============================================================================
Write-Host "[3/6] Ensuring pip is available..." -ForegroundColor Yellow

& ".venv\Scripts\python.exe" -m ensurepip --upgrade

if ($LASTEXITCODE -eq 0) {
    Write-Host "  pip installed and upgraded" -ForegroundColor Green
} else {
    Write-Host "  ensurepip had issues, trying alternative..." -ForegroundColor Yellow
    Invoke-WebRequest -Uri "https://bootstrap.pypa.io/get-pip.py" -OutFile "get-pip.py"
    & ".venv\Scripts\python.exe" get-pip.py
    Remove-Item "get-pip.py" -Force
}
Write-Host ""

# =============================================================================
# Step 4: Upgrade pip, setuptools, and wheel
# =============================================================================
Write-Host "[4/6] Upgrading pip, setuptools, and wheel..." -ForegroundColor Yellow

& ".venv\Scripts\python.exe" -m pip install --upgrade pip setuptools wheel

if ($LASTEXITCODE -eq 0) {
    Write-Host "  pip, setuptools, and wheel upgraded" -ForegroundColor Green
} else {
    Write-Host "  Some upgrades failed, continuing..." -ForegroundColor Yellow
}
Write-Host ""

# =============================================================================
# Step 5: Install all required packages
# =============================================================================
Write-Host "[5/6] Installing all required packages..." -ForegroundColor Yellow
Write-Host ""

$packages = @(
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.30.0",
    "sqlmodel>=0.0.21",
    "sqlalchemy>=2.0.0",
    "asyncpg>=0.29.0",
    "psycopg2-binary>=2.9.9",
    "alembic>=1.13.0",
    "pgvector>=0.4.2",
    "pydantic>=2.8.0",
    "pydantic-settings>=2.3.0",
    "python-jose[cryptography]>=3.3.0",
    "passlib[bcrypt]>=1.7.4",
    "python-multipart>=0.0.9",
    "openai>=1.35.0",
    "google-generativeai>=0.8.6",
    "litellm>=1.50.0",
    "openai-agents>=0.10.0",
    "kafka-python-ng>=2.2.0",
    "httpx>=0.27.0",
    "python-dotenv>=1.2.1",
    "email-validator>=2.3.0"
)

Write-Host "  Installing packages (this may take a few minutes)..." -ForegroundColor Gray
Write-Host ""

& ".venv\Scripts\pip.exe" install $packages --quiet

if ($LASTEXITCODE -eq 0) {
    Write-Host "  All packages installed successfully" -ForegroundColor Green
} else {
    Write-Host "  Some packages failed to install" -ForegroundColor Red
}

Write-Host ""
Write-Host "  Installing project in editable mode..." -ForegroundColor Gray
& ".venv\Scripts\pip.exe" install -e . --quiet

Write-Host ""
Write-Host "=============================================================================" -ForegroundColor Cyan
Write-Host "  Environment Reset Complete!" -ForegroundColor Green
Write-Host "=============================================================================" -ForegroundColor Cyan
Write-Host ""

# =============================================================================
# Step 6: Verify installation
# =============================================================================
Write-Host "[6/6] Verifying installation..." -ForegroundColor Yellow
Write-Host ""

$tests = @(
    @{"cmd" = "import fastapi"; "name" = "FastAPI"},
    @{"cmd" = "import uvicorn"; "name" = "Uvicorn"},
    @{"cmd" = "import pydantic"; "name" = "Pydantic"},
    @{"cmd" = "import sqlalchemy"; "name" = "SQLAlchemy"},
    @{"cmd" = "import openai_agents"; "name" = "OpenAI Agents SDK"},
    @{"cmd" = "import litellm"; "name" = "LiteLLM"},
    @{"cmd" = "import google.generativeai"; "name" = "Google Generative AI"},
    @{"cmd" = "import dotenv"; "name" = "python-dotenv"}
)

$all_passed = $true

foreach ($test in $tests) {
    $result = & ".venv\Scripts\python.exe" -c $test.cmd 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  OK: $($test.name)" -ForegroundColor Green
    } else {
        Write-Host "  FAILED: $($test.name)" -ForegroundColor Red
        $all_passed = $false
    }
}

Write-Host ""

if ($all_passed) {
    Write-Host "All packages installed successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "  1. Activate: .\.venv\Scripts\activate" -ForegroundColor White
    Write-Host "  2. Verify:   python test_env.py" -ForegroundColor White
    Write-Host "  3. Start:    uvicorn main:app --reload" -ForegroundColor White
} else {
    Write-Host "Some packages failed to install. Check errors above." -ForegroundColor Yellow
}

Write-Host ""
