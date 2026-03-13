# Customer Success Digital FTE - Backend

Backend API for the Customer Success Digital FTE project - a 24/7 autonomous AI employee for multi-channel customer support.

## Tech Stack

- **Framework:** FastAPI
- **Package Manager:** UV
- **Database:** PostgreSQL 15+ with pgvector
- **ORM:** SQLModel
- **Async Driver:** asyncpg
- **Message Queue:** Apache Kafka
- **AI:** OpenAI Agents SDK with multi-provider fallback

## Quick Start

### Prerequisites

- Python 3.11+
- UV package manager
- Docker & Docker Compose
- PostgreSQL 15+ (or use Docker)

### Installation

1. **Install dependencies:**
   ```bash
   uv sync
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

3. **Start infrastructure (PostgreSQL, Kafka):**
   ```bash
   # Using Docker Compose
   docker-compose up -d postgres kafka kafka-init
   
   # Or use the start script
   ./docker-start.sh
   ```

4. **Run database migrations:**
   ```bash
   uv run alembic upgrade head
   ```

5. **Start the development server:**
   ```bash
   uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

6. **Access the API:**
   - API: http://localhost:8000
   - Docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Docker Commands

```bash
# Start infrastructure only
./docker-start.sh

# Start infrastructure + backend
./docker-start.sh backend

# Stop all services
./docker-stop.sh

# View logs
docker-compose logs -f

# Check service status
docker-compose ps
```

## Project Structure

```
backend/
├── app/
│   ├── api/          # API routes
│   ├── core/         # Core utilities, security
│   ├── crud/         # CRUD operations
│   ├── models/       # SQLModel database models
│   ├── schemas/      # Pydantic schemas
│   ├── services/     # External service integrations
│   ├── config.py     # Application configuration
│   ├── database.py   # Database connection
│   └── main.py       # FastAPI application
├── alembic/          # Database migrations
├── tests/            # Test files
├── pyproject.toml    # Project dependencies
├── docker-compose.yml
└── .env.example
```

## API Endpoints

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/` | GET | No | Welcome message |
| `/health` | GET | No | Health check |
| `/api/v1/tickets` | GET/POST | Yes | List/Create tickets |
| `/api/v1/customers` | GET/POST | Yes | List/Create customers |
| `/api/v1/agent/respond` | POST | Yes | Generate AI response |
| `/api/v1/web/support` | POST | No | Public support form |

## Development

### Run Tests
```bash
uv run pytest
```

### Run Linting
```bash
uv run ruff check .
```

### Type Checking
```bash
uv run mypy .
```

## License

MIT
