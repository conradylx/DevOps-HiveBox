# DevOps HiveBox

A real-world DevOps end-to-end project following the [DevOps Roadmap - HiveBox Project](https://devopsroadmap.io/projects/hivebox/).

## Project Overview

HiveBox is a scalable RESTful API built around [openSenseMap](https://opensensemap.org/) to help beekeepers with their chores by tracking environmental sensor data. This project covers the entire Software Development Life Cycle (SDLC) in iterative phases.

## Current Status: Phase 3 - Laying the Base

✅ **Phase 1**: Project Setup & Planning - COMPLETED
- GitHub repository forked and project board created
- Agile methodology selected (Kanban)
- Documentation structure established

✅ **Phase 2**: Code & Containers - COMPLETED
- 2.2 Code: Basic version endpoint implemented (v0.0.1)
- 2.3 Containers: Dockerfile created with security best practices
- 2.4 Testing: Local testing completed and documented

✅ **Phase 3**: Start - Laying the Base - COMPLETED
- 3.1 Tools: Hadolint and Pylint configured
- 3.2 Code: `/version` and `/temperature` endpoints with OpenSenseMap integration
- 3.3 Containers: Docker best practices applied
- 3.4 CI: GitHub Actions pipeline with linting, testing, and security scanning
- 3.5 Testing: Unit tests (100% coverage) and integration tests in CI

## Project Structure

```
DevOps-HiveBox/
├── .github/
│   └── workflows/
│       └── ci.yml           # CI pipeline
├── app/
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py      # Application configuration
│   ├── services/
│   │   ├── __init__.py
│   │   └── opensensemap.py  # OpenSenseMap API integration
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── version.py       # /version endpoint
│   │   └── temperature.py   # /temperature endpoint
│   ├── tests/               # Unit tests folder
│   │   ├── __init__.py
│   │   ├── test_version.py
│   │   ├── test_opensensemap.py
│   │   └── test_temperature.py
│   ├── __init__.py          
│   ├── main.py              # FastAPI application
│   ├── Dockerfile           # Docker image definition
│   ├── requirements.txt     # Python dependencies
│   ├── requirements-dev.txt # Python dev dependencies
│   └── version.txt          # Stores current app version
├── .coveragearc             # Coverage.py configuration file
├── .pylintrc                # Pylint configuration
├── pytest.ini               # Pytest configuration
├── .gitignore               # Git ignore rules
├── .dockerignore            # Docker ignore rules
├── docker-compose.yml       # Docker Compose configuration
└── README.md                # Documentation file
```

## Technologies Used

### Phase 3 Stack
- **Language**: Python 3.13
- **Framework**: FastAPI
- **HTTP Client**: httpx (async)
- **Testing**: pytest, pytest-asyncio, pytest-cov
- **Linting**: Pylint (Python), Hadolint (Dockerfile)
- **CI/CD**: GitHub Actions
- **Security**: OpenSSF Scorecard
- **Containerization**: Docker (Alpine-based)
- **Version Control**: Git & GitHub with Conventional Commits

## API Endpoints

### `GET /`
Root endpoint returning application version.

**Response:**
```json
{"version": "0.2.0"}
```

### `GET /version`
Returns the current application version.

**Response:**
```json
{"version": "0.2.0"}
```

### `GET /temperature`
Returns average temperature from all configured senseBoxes with data no older than 1 hour.

**Response (Success):**
```json
{
  "average_temperature": 22.5,
  "unit": "°C",
  "samples": 3
}
```

**Response (No Fresh Data - 503):**
```json
{
  "detail": "No fresh temperature data available"
}
```

## Quick Start

### Prerequisites

- Docker 20.10+
- Docker Compose 2.0+
- Python 3.13+ (for local development)

### Running with Docker Compose

1. Clone the repository:
```bash
git clone https://github.com/conradylx/DevOps-HiveBox
cd DevOps-HiveBox
```

2. Start the application:
```bash
docker compose up --build -d
```

3. Test the endpoints:
```bash
# Version endpoint
curl http://localhost:8000/version

# Temperature endpoint
curl http://localhost:8000/temperature
```

4. View logs:
```bash
docker compose logs -f web
```

5. Stop the application:
```bash
docker compose down
```

### Local Development

1. Create virtual environment:
```bash
cd app
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

4. Access API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Running Tests

```bash
cd app

# Run all tests with coverage
pytest --cov=. --cov-report=term-missing

# Run specific test file
pytest tests/test_version.py -v

# Run with verbose output
pytest -v
```

### Code Quality

```bash
# Lint Python code
cd app
pylint --rcfile=../.pylintrc *.py config/ services/ routers/

# Lint Dockerfile (using Docker)
docker run --rm -i hadolint/hadolint < app/Dockerfile
```

### SenseBox Configuration

The application uses 3 senseBox IDs by default. You can configure your own by setting the `SENSEBOX_IDS` environment variable in `docker-compose.yml` or exporting it before running the app.

Default senseBoxes:
- [5eba5fbad46fb8001b799786](https://opensensemap.org/explore/5eba5fbad46fb8001b799786)
- [5c21ff8f919bf8001adf2488](https://opensensemap.org/explore/5c21ff8f919bf8001adf2488)
- [5ade1acf223bd80019a1011c](https://opensensemap.org/explore/5ade1acf223bd80019a1011c)

## CI/CD Pipeline

The project uses GitHub Actions for continuous integration:

### Pipeline Jobs

1. **lint-python**: Lints Python code with Pylint
2. **lint-dockerfile**: Lints Dockerfile with Hadolint
3. **build**: Builds Docker image
4. **test**: Runs unit tests with pytest (100% coverage)
5. **integration-test**: Tests `/version` endpoint in Docker container
6. **scorecard**: Runs OpenSSF Scorecard security analysis (main branch only)

### Triggers

- Push to: `main`, `develop`, `feat/**`, `fix/**`
- Pull requests to: `main`

### Status Badges

```markdown
![CI Pipeline](https://github.com/conradylx/DevOps-HiveBox/workflows/CI%20Pipeline/badge.svg)
[![codecov](https://codecov.io/gh/conradylx/DevOps-HiveBox/branch/main/graph/badge.svg)](https://codecov.io/gh/conradylx/DevOps-HiveBox)
```

## Security Features

### Container Security
- Alpine Linux base (minimal attack surface)
- Image pinned with SHA256 digest
- Non-root user (`hiveboxusr`)
- System-level isolation (`hiveboxgrp`)
- Strict permissions (750)
- No new privileges flag
- All Linux capabilities dropped
- Resource limits (1 CPU, 512MB RAM)

### Code Security
- Pylint for code quality
- Hadolint for Dockerfile best practices
- OpenSSF Scorecard for security analysis
- Dependency scanning in CI
- 100% test coverage

### Runtime Security
- Health checks configured
- Automatic restart policy
- Async HTTP client with timeouts
- Error handling for external API failures

## Development Workflow

This project follows best practices:

1. **Branching Strategy**: Feature branches (`feat/*`, `fix/*`)
2. **Commit Convention**: [Conventional Commits](https://www.conventionalcommits.org/)
   - `feat:` new features
   - `fix:` bug fixes
   - `docs:` documentation
   - `test:` tests
   - `ci:` CI/CD changes
   - `refactor:` code refactoring
3. **Pull Requests**: All changes via PR to `main`
4. **Code Review**: Required before merging
5. **Testing**: 100% coverage requirement

### Example Workflow

```bash
# Create feature branch
git checkout -b feat/add-humidity-endpoint

# Make changes and commit using Conventional Commits
git add .
git commit -m "feat: add humidity endpoint to API"

# Push and create PR
git push origin feat/add-humidity-endpoint
```

## Testing

### Unit Tests
- All endpoints tested
- 100% code coverage
- Mock external API calls
- Test error scenarios

### Integration Tests
- Docker container validation
- Endpoint accessibility
- Version verification
- HTTP status code checks

### Test Coverage Report
```bash
cd app
pytest --cov=. --cov-report=html
# Open htmlcov/index.html in browser
```

## Phase Requirements Checklist

### Phase 1 ✅
- [x] Fork repository
- [x] Create project board (Kanban)
- [x] Select Agile methodology
- [x] Document workflow

### Phase 2 ✅
- [x] Semantic versioning (v0.0.1 → v0.1.0)
- [x] Basic version endpoint
- [x] Dockerfile with best practices
- [x] Docker Compose configuration
- [x] Local testing documentation

### Phase 3 ✅
- [x] Hadolint and Pylint setup
- [x] Conventional Commits adopted
- [x] `/version` endpoint
- [x] `/temperature` endpoint with OpenSenseMap
- [x] Data freshness validation (< 1 hour)
- [x] Unit tests (100% coverage)
- [x] Container best practices
- [x] GitHub Actions CI pipeline
- [x] Code and Dockerfile linting
- [x] Docker image build in CI
- [x] Unit tests in CI
- [x] Integration test for `/version`
- [x] OpenSSF Scorecard integration

### Phase 4 (Upcoming)
- [ ] Kubernetes deployment
- [ ] Prometheus metrics endpoint
- [ ] Temperature status field
- [ ] Integration tests
- [ ] SonarQube analysis
- [ ] Container registry publishing

## Project Roadmap

### Completed Phases
- ✅ **Phase 1**: Kickoff & Preparation
- ✅ **Phase 2**: Basics - Code & Containers
- ✅ **Phase 3**: Start - Laying the Base

### Current Phase
- 🎯 **Phase 4**: Expand - Constructing a Shell (Next up!)

### Upcoming Phases
- **Phase 4**: Expand - Kubernetes, Metrics, Integration Tests
- **Phase 5**: Transform - Caching, Storage, IaC
- **Phase 6**: Optimize - GitOps, Production Ready
- **Phase 7**: Capstone Project

## Troubleshooting

### Container won't start
```bash
# Check logs
docker compose logs web

# Check health status
docker compose ps

# Rebuild from scratch
docker compose down
docker compose up --build
```

### Temperature endpoint returns 503
This means no fresh data (< 1 hour old) is available from senseBoxes. This is expected if:
- SenseBoxes are offline
- No recent measurements
- Network issues

### Tests failing locally
```bash
# Ensure in correct directory
cd app

# Install all dependencies
pip install -r requirements.txt

# Run tests with verbose output
pytest -v
```

## Resources

- [Project Specification](https://devopsroadmap.io/projects/hivebox/)
- [OpenSenseMap API Documentation](https://docs.opensensemap.org/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

## Contributing

This is a learning project following DevOps best practices:
- Use feature branches for development
- Create pull requests against `main` branch
- Never push directly to `main`
- Follow Conventional Commits (from Phase 3)
- Document changes as you go

## License

Educational project - open source for learning purposes.