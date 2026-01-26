# DevOps HiveBox

A real-world DevOps end-to-end project following the [DevOps Roadmap - HiveBox Project](https://devopsroadmap.io/projects/hivebox/).

## Project Overview

HiveBox is a scalable RESTful API built around [openSenseMap](https://opensensemap.org/) to help beekeepers with their chores by tracking environmental sensor data. This project covers the entire Software Development Life Cycle (SDLC) in iterative phases.

## Current Status: Phase 2 - Basics (DevOps Core)

✅ **Phase 1**: Project Setup & Planning - COMPLETED
- GitHub repository forked and project board created
- Agile methodology selected (Kanban)
- Documentation structure established

✅ **Phase 2**: Code & Containers - COMPLETED
- ✅ 2.2 Code: Basic version endpoint implemented (`v0.0.1`)
- ✅ 2.3 Containers: Dockerfile created with security best practices
- ✅ 2.4 Testing: Local testing completed and documented

## Project Structure

```
DevOps-HiveBox/
├── app/
│   ├── main.py              # FastAPI application
│   ├── Dockerfile           # Docker image definition
│   └── requirements.txt     # Python dependencies
├── docker-compose.yml      # Docker Compose configuration
├── version.txt             # Stores current app version
├── .gitignore              # Git ignore rules
├── .dockerignore           # Docker ignore rules
└── README.md               # Documentation file
```

## Technologies Used (Phase 2)

- **Language**: Python 3.13.7
- **Framework**: FastAPI
- **Containerization**: Docker (Alpine-based)
- **Version Control**: Git & GitHub
- **Base Image**: python:3.13.7-alpine (pinned with SHA256)

## Quick Start

### Prerequisites

- Docker 20.10+
- Docker Compose 2.0+
- Python 3.13+ (optional, for local development)

### Setup

1. Clone your forked repository:
```bash
git clone https://github.com/conradylx/DevOps-HiveBox
cd DevOps-HiveBox
```

2. Ensure `requirements.txt` has hashes (for `--require-hashes` flag):
```bash
# Generate hashes if needed
cat ./app/requirement.txt | while read package; do
  hashin "$package" --requirements-file=./app/requirement.txt
done```

3. Run with Docker Compose:
```bash
docker compose up --build
```

4. Test the application:
```bash
curl http://localhost:8000/
# Expected: {"version": "0.0.1"}

# Check health status
docker compose ps
# Should show "healthy" status after ~60 seconds
```

5. View logs:
```bash
docker compose logs -f web
```

6. Stop the application:
```bash
docker compose down
```

### Local Development (Optional)
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r app/requirements.txt

# Run application
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Phase 2 Requirements

### 2.2 Code ✅
- [x] Implement semantic versioning (v0.0.1)
- [x] Create function that prints current app version

### 2.3 Containers ✅
- [x] Create Dockerfile with security best practices:
  - Alpine-based image (smaller footprint)
  - Image pinned with SHA256 digest
  - Non-root user (`hiveboxusr`)
  - Dedicated group (`hiveboxgrp`)
  - Strict permissions (750)
  - `--require-hashes` for pip dependencies
  - Security options: `no-new-privileges`, all capabilities dropped
  - Resource limits (1 CPU, 512MB RAM)
  - Health checks configured
- [x] Build and run Docker image locally
- [x] Configure Docker Compose with production-ready settings

### 2.4 Testing ✅
- [x] Run app container and verify correct output
- [x] Document testing procedures (see Testing section below)

## Next Steps (Phase 3)

Phase 3 will introduce:
- Code linting (Hadolint, Pylint)
- Conventional Commits
- New endpoints: `/version` and `/temperature`
- Unit tests
- CI/CD with GitHub Actions
- Container best practices

## Project Roadmap

### Completed Phases
- ✅ **Phase 1**: Kickoff & Preparation
- ✅ **Phase 2**: Basics - Code & Containers

### Current Phase
- 🎯 **Phase 3**: Start - Laying the Base (Next up!)

### Upcoming Phases
- **Phase 3**: Start - Laying the Base (Linting, Testing, CI)
- **Phase 4**: Expand - Constructing a Shell (Kubernetes, Metrics)
- **Phase 5**: Transform - Finishing the Structure (Caching, Storage, IaC)
- **Phase 6**: Optimize - Keep Improving (GitOps, Production Ready)
- **Phase 7**: Capstone Project (Your Own Design)

## Security Features

Current implementation includes comprehensive security hardening:

**Container Security:**
- Alpine Linux base (minimal attack surface)
- Image pinned with SHA256 digest (supply chain security)
- Non-root container user (`hiveboxusr`)
- System-level user and group isolation (`hiveboxgrp`)
- Strict file permissions (750)
- No new privileges flag enabled
- All Linux capabilities dropped
- Resource limits enforced (CPU and memory)

**Dependency Security:**
- Pip packages installed with `--require-hashes`
- No cache for package installation
- Upgraded pip before package installation

**Runtime Security:**
- Health checks configured (monitors `/version` endpoint)
- Automatic restart policy (`unless-stopped`)
- Python unbuffered output for better logging
- Volume mounting for development hot-reload

## Testing

### Phase 2 Testing Procedures

The Phase 2 testing validates that:
1. The application container builds successfully
2. The container runs without errors
3. The `/version` endpoint returns the correct version from environment variable

**Test Steps:**

1. **Build and start the container:**
```bash
docker compose up --build -d
```

2. **Wait for health check to pass:**
```bash
# Watch container status
docker compose ps

# Wait until status shows "healthy" (~60 seconds)
```

3. **Test the version endpoint:**
```bash
# Test the root endpoint
curl http://localhost:8000/

# Expected output:
# {"version":"0.0.1"}
```

4. **Check container logs:**
```bash
docker compose logs web

# Should show uvicorn startup messages without errors
```

5. **Verify security settings:**
```bash
# Check that container runs as non-root user
docker compose exec web whoami
# Expected: hiveboxusr

# Check container capabilities
docker inspect devops-hivebox-web-1 | grep -A 10 CapDrop
# Expected: all capabilities dropped
```

### Test Results

All tests should pass with:
- ✅ Container builds without errors
- ✅ Container runs as non-root user (hiveboxusr)
- ✅ Health check passes after startup period
- ✅ Endpoint returns correct version from version.txt
- ✅ Version changes when version.txt file is updated
- ✅ No errors in container logs

## API Documentation

Once running, access interactive API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Contributing

This is a learning project following DevOps best practices:
- Use feature branches for development
- Create pull requests against `main` branch
- Never push directly to `main`
- Follow Conventional Commits (from Phase 3)
- Document changes as you go

## Resources

- [Project Specification](https://devopsroadmap.io/projects/hivebox/)
- [openSenseMap API](https://docs.opensensemap.org/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

## License

Educational project - open source for learning purposes.