![CI Pipeline](https://github.com/conradylx/DevOps-HiveBox/workflows/CI%20Pipeline/badge.svg)
![CD Pipeline](https://github.com/conradylx/DevOps-HiveBox/workflows/CD%20Pipeline/badge.svg)
[![codecov](https://codecov.io/gh/conradylx/DevOps-HiveBox/graph/badge.svg?token=X43GELVCX6)](https://codecov.io/gh/conradylx/DevOps-HiveBox)

# DevOps HiveBox

A real-world DevOps end-to-end project following the [DevOps Roadmap - HiveBox Project](https://devopsroadmap.io/projects/hivebox/).

## Project Overview

HiveBox is a scalable RESTful API built around [openSenseMap](https://opensensemap.org/) to help beekeepers with their chores by tracking environmental sensor data. This project covers the entire Software Development Life Cycle (SDLC) in iterative phases.

## Current Status: Phase 4 - Constructing a Shell

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

✅ **Phase 4**: Expand - Constructing a Shell - COMPLETED
- 4.1 Tools: Kind and Kubectl configured
- 4.2 Code: `/metrics` endpoint with Prometheus, temperature status field
- 4.3 Containers: Kubernetes manifests (Deployment, Service, Ingress, - ConfigMap, NetworkPolicy)
- 4.4 CI: Extended pipeline with SonarQube and Terrascan
- 4.5 CD: GitHub Actions workflow for GHCR publishing

✅ **Phase 5**: Transform - Finishing the Structure - COMPLETED
- 5.1 Tools: Kubernetes, kubectl, Helm
- 5.2 Code: Valkey caching, MinIO storage, /store, /metrics, /readyz, /healthz endpoints
- 5.3 Containers: Helm chart, Kustomize overlays, security best practices
- 5.4 Infrastructure as Code: Prometheus + Grafana monitoring stack
- 5.5 CI: End-to-End tests with Venom (13 tests passing)
- 5.6 CD: Security scanning with Trivy, best practices

## Project Structure

```
DevOps-HiveBox/
├── .github/
│   └── workflows/
│       ├── ci.yml           # CI pipeline
│       ├── cd.yml           # CD pipeline
│       ├── e2e.yml          # E2E tests with Venom
│       └── security-scan.yml # Trivy security scanning
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
│   │   ├── temperature.py   # /temperature endpoint
│   │   └── metrics.py       # /metrics endpoint (Prometheus)
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_version.py
│   │   ├── test_temperature.py
│   │   ├── test_opensensemap.py
│   │   └── test_metrics.py  # Metrics tests
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── Dockerfile           # Docker image definition
│   ├── requirements.txt     # Python dependencies
│   ├── requirements-dev.txt # Python dev dependencies
│   └── version.txt          # Stores current app version
├── helm-chart/              # Helm chart for deployment
│   ├── Chart.yaml
│   ├── values.yaml          # Default values
│   ├── values-dev.yaml      # Development environment
│   ├── values-prod.yaml     # Production environment
│   └── templates/
│       ├── deployment.yaml
│       ├── service.yaml
│       ├── ingress.yaml
│       ├── configmap.yaml
│       ├── networkpolicy.yaml
│       └── _helpers.tpl
├── k8s/                     # Kubernetes manifests
│   ├── base/                # Base manifests
│   │   ├── namespace.yaml
│   │   ├── configmap.yaml
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   ├── ingress.yaml
│   │   ├── networkpolicy.yaml
│   │   └── kustomization.yaml
│   ├── infrastructure/      # Infrastructure components
│   │   ├── valkey/         # Valkey cache
│   │   │   ├── deployment.yaml
│   │   │   ├── service.yaml
│   │   │   └── kustomization.yaml
│   │   └── minio/          # MinIO storage
│   │       ├── deployment.yaml
│   │       ├── service.yaml
│   │       └── kustomization.yaml
│   ├── overlays/           # Environment-specific configs
│   │   ├── dev/
│   │   │   ├── kustomization.yaml
│   │   │   └── patches/
│   │   │       ├── configmap.yaml
│   │   │       ├── image.yaml
│   │   │       └── replicas.yaml
│   │   ├── stg/
│   │   │   ├── kustomization.yaml
│   │   │   └── patches/
│   │   │       ├── configmap.yaml
│   │   │       ├── image.yaml
│   │   │       └── replicas.yaml
│   │   └── prod/
│   │       ├── kustomization.yaml
│   │   │   └── patches/
│   │   │       ├── configmap.yaml
│   │   │       ├── image.yaml
│   │   │       └── replicas.yaml
│   └── monitoring/         # Monitoring stack
│       ├── monitoring-values.yaml
│       ├── service-monitor.yaml
│       ├── grafana-values.yaml
│       └── grafana-dashboard-hivebox.yaml
├── tests/e2e/              # End-to-End tests
│   ├── hivebox.yaml        # Venom test suite (13 tests)
│   ├── .venomrc            # Venom configuration
│   └── reports/            # Test reports
├── scripts/
│   └── run-e2e-tests.sh    # Local E2E testing script
├── .coveragerc              # Coverage.py configuration
├── .pylintrc                # Pylint configuration
├── pytest.ini               # Pytest configuration
├── .gitignore               # Git ignore rules
├── .dockerignore            # Docker ignore rules
├── docker-compose.yml       # Docker Compose configuration
└── README.md                # Documentation file
```

## Technologies Used

### Phase 5 Stack
- **Caching**: Valkey 8.0.1 (Redis-compatible)
- **Storage**: MinIO (S3-compatible)
- **Orchestration**: Helm 3.x, Kustomize
- **Monitoring**: Prometheus + Grafana (kube-prometheus-stack)
- **E2E Testing**: Venom
- **Security Scanning**: Trivy, Kubesec

### Phase 4 Stack
- **Orchestration**: Kubernetes 1.28+
- **Ingress**: NGINX Ingress Controller
- **Container Registry**: GitHub Container Registry (ghcr.io)
- **Code Quality**: SonarQube
- **Security**: Terrascan, OpenSSF Scorecard

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
{"version": "0.3.0"}
```

### `GET /version`
Returns the current application version.

**Response:**
```json
{"version": "0.3.0"}
```

### `GET /temperature`
Returns average temperature from all configured senseBoxes with data no older than 1 hour.

**Response (Success):**
```json
{
  "average_temperature": 22.5,
  "unit": "°C",
  "samples": 3,
  "status": "Good"
}
```

**Response (No Fresh Data - 503):**
```json
{
  "detail": "No fresh temperature data available"
}
```

### `GET /metrics`
Returns Prometheus metrics for application monitoring.

**Response (Prometheus format):**
```prometheus
# HELP hivebox_temperature_requests_total Total number of temperature requests
# TYPE hivebox_temperature_requests_total counter
hivebox_temperature_requests_total 42.0
# HELP hivebox_version_requests_total Total number of version requests
# TYPE hivebox_version_requests_total counter
hivebox_version_requests_total 128.0
```

### `GET /store`
Force immediate storage of current temperature data to MinIO.

**Response:**
```json
{
  "status": "success",
  "message": "Data stored to MinIO",
  "filename": "temperature_manual_20250129_143022.json",
  "timestamp": "2025-01-29T14:30:22.123456Z"
}
```

### `GET /readyz`
Readiness probe with intelligent health checking.

**Response:**
```json
{
  "status": "ready",
  "valkey": "connected",
  "minio": "connected",
  "checks": {
    "senseBoxes": "ok"
  }
}
```

### `GET /healthz`
Liveness probe for Kubernetes health checks.

**Response:**
```json
{
  "status": "healthy"
}
```

## Quick Start

### Prerequisites

- Docker 20.10+
- Docker Compose 2.0+
- Python 3.13+ (for local development)
- kubectl 1.28+ (for Kubernetes)
- KIND 0.20+ or Minikube (for local Kubernetes cluster)
- Helm 3.x (for Helm deployments)

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

# Metrics endpoint
curl http://localhost:8000/metrics

# Store endpoint
curl -X POST http://localhost:8000/store

# Readiness check
curl http://localhost:8000/readyz

# Health check
curl http://localhost:8000/healthz
```

4. View logs:
```bash
docker compose logs -f web
```

5. Stop the application:
```bash
docker compose down
```

### Running on Kubernetes with Helm (Recommended)
```bash
# Start Minikube
minikube start --cpus=4 --memory=8192

# Enable addons
minikube addons enable ingress
minikube addons enable metrics-server

# Build image in Minikube
eval $(minikube docker-env)
VERSION=$(cat app/version.txt)
docker build -t hivebox:${VERSION} -f app/Dockerfile app/
eval $(minikube docker-env -u)

# Install with Helm
helm install hivebox helm-chart/ \
  --namespace hivebox \
  --create-namespace \
  -f helm-chart/values-dev.yaml \
  --set image.tag=${VERSION} \
  --set image.pullPolicy=Never

# Check status
helm status hivebox -n hivebox
kubectl get all -n hivebox

# Access application
kubectl port-forward -n hivebox svc/hivebox 8000:8000
curl http://localhost:8000/version
```

### Running on Kubernetes with Kustomize
```bash
# Start Minikube
minikube start --cpus=4 --memory=8192
minikube addons enable ingress

# Build image
eval $(minikube docker-env)
docker build -t hivebox:0.3.0 -f app/Dockerfile app/
eval $(minikube docker-env -u)

# Deploy to dev environment
kubectl apply -k k8s/overlays/dev/

# Check status
kubectl get all -n hivebox

# Deploy to staging
kubectl apply -k k8s/overlays/stg/

# Deploy to production
kubectl apply -k k8s/overlays/prod/
```

### Monitoring Stack (Prometheus + Grafana)
```bash
# Add Helm repo
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Install Prometheus + Grafana
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace \
  -f k8s/monitoring/monitoring-values.yaml

# Deploy ServiceMonitor
kubectl apply -f k8s/monitoring/service-monitor.yaml

# Access Grafana
kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80
# Open: http://localhost:3000 (admin/admin)

# Access Prometheus
kubectl port-forward -n monitoring svc/prometheus-kube-prometheus-prometheus 9090:9090
# Open: http://localhost:9090
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

### End-to-End Tests (Phase 5)
```bash
# Make script executable
chmod +x scripts/run-e2e-tests.sh

# Deploy application first
kubectl apply -k k8s/overlays/dev/

# Run E2E tests
./scripts/run-e2e-tests.sh

# Test reports available in: tests/e2e/reports/
```

E2E Test Coverage:

- ✅ Health check endpoint
- ✅ Version endpoint
- ✅ Root endpoint
- ✅ Temperature endpoint (cache miss)
- ✅ Temperature endpoint (cache hit)
- ✅ Readiness probe logic
- ✅ Metrics endpoint format
- ✅ API documentation
- ✅ OpenAPI schema
- ✅ Invalid endpoints (404)
- ✅ Cache performance
- ✅ Valkey connection
- ✅ MinIO connection

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

### Kubernetes Configuration
The project includes the following Kubernetes resources:
- Namespace: Isolates application resources
- ConfigMap: Stores environment variables (VERSION, SENSEBOX_IDS)
- Deployment: Manages pod replicas with security context
- Service: Exposes application internally (ClusterIP)
- Ingress: Routes external traffic to the service
- NetworkPolicy: Controls pod-to-pod communication

### Helm Chart
Multi-environment deployment with Helm:
```bash
# Install
helm install hivebox helm-chart/ -n hivebox --create-namespace -f helm-chart/values-dev.yaml

# Upgrade
helm upgrade hivebox helm-chart/ -f helm-chart/values-dev.yaml

# Uninstall
helm uninstall hivebox -n hivebox

# View values
helm get values hivebox -n hivebox
```

### Monitoring with Prometheus and Grafana
Custom Metrics:

- hivebox_temperature_requests_total - Total temperature requests
- hivebox_temperature_cache_hits - Cache hits counter
- hivebox_temperature_cache_misses - Cache misses counter
- hivebox_temperature_celsius - Current temperature gauge
- hivebox_temperature_request_duration_seconds - Request duration histogram
- hivebox_valkey_connected - Valkey connection status (1/0)
- hivebox_minio_connected - MinIO connection status (1/0)
- hivebox_sensebox_available - Available senseBoxes count
- hivebox_storage_operations_total - Storage operations counter

## Useful Prometheus Queries
```promql
# Request rate
rate(hivebox_temperature_requests_total[5m])

# Cache hit ratio
rate(hivebox_temperature_cache_hits[5m]) / 
(rate(hivebox_temperature_cache_hits[5m]) + rate(hivebox_temperature_cache_misses[5m])) * 100

# Current temperature
hivebox_temperature_celsius

# Request duration p95
histogram_quantile(0.95, rate(hivebox_temperature_request_duration_seconds_bucket[5m]))
```

## CI/CD Pipeline

The project uses GitHub Actions for continuous integration:

### Pipeline Jobs

1. **lint-python**: Lints Python code with Pylint
2. **lint-dockerfile**: Lints Dockerfile with Hadolint
3. **build**: Builds Docker image
4. **test**: Runs unit tests with pytest (100% coverage)
5. **integration-test**: Tests `/version` endpoint in Docker container
6. **terrascan**: Kubernetes manifest security scanning
7. **sonarqube**: Code quality and security analysis
8. **scorecard**: Runs OpenSSF Scorecard security analysis (main branch only)

### Triggers

- Push to: `main`, `develop`, `feat/**`, `fix/**`
- Pull requests to: `main`

## End-to-End Tests
Pipeline Steps:

1. Setup Minikube cluster
2. Deploy infrastructure (Valkey, MinIO)
3. Deploy HiveBox application
4. Run 13 Venom E2E tests
5. Upload test reports

### Triggers
- Pull requests to main
- Push to main, develop
- Manual workflow dispatch

## Security scanning
Security Scanning 
- Trivy Image Scan: Docker image vulnerabilities
- Trivy Dockerfile Scan: Dockerfile misconfigurations
- Trivy K8s Scan: Kubernetes manifest issues
- Kubesec: K8s security best practices

### Triggers
- Push to main, develop
- Pull requests to main
- Daily schedule (2 AM UTC)

## Continuous Deployment (CD)
Automated deployment to GitHub Container Registry (GHCR):
- Read version from app/version.txt
- Build Docker image with version tag
- Push to GitHub Container Registry
- Generate build provenance attestation

### Published images:

- ghcr.io/conradylx/devops-hivebox:latest (from main)
- ghcr.io/conradylx/devops-hivebox:v0.1.0 (from tags)
- ghcr.io/conradylx/devops-hivebox:main-sha-abc123 (commit SHA)

### Triggers

- Push to: `main`
- Git tags (e.g., v0.1.0)

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

### Kubernetes Security
- Pod Security Context (runAsNonRoot, seccompProfile)
- Container Security Context (no privilege escalation, capabilities - dropped)
- Network Policies for traffic control
- No automount of service account tokens
- Terrascan scanning for misconfigurations
- Liveness and readiness probes

### Code Security

- Pylint for code quality
- Hadolint for Dockerfile best practices
- OpenSSF Scorecard for security analysis
- SonarQube for SAST
- Dependency scanning in CI
- 100% test coverage

### Runtime Security
- Health checks configured
- Automatic restart policy
- Async HTTP client with timeouts
- Error handling for external API failures
- Prometheus metrics for observability

## Development Workflow

This project follows best practices:

1. **Branching Strategy**: Feature branches (`feat/*`, `fix/*`)
2. **Commit Convention**: [Conventional Commits](https://www.conventionalcommits.org/)
   - `feat:` new features
   - `fix:` bug fixes
   - `docs:` documentation
   - `test:` tests
   - `ci:` CI/CD changes
   - `k8s`: Kubernetes changes
   - `refactor:` code refactoring
3. **Pull Requests**: All changes via PR to `main`
4. **Code Review**: Required before merging
5. **Testing**: 100% coverage requirement
6. **Security**: Automated scanning in CI

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
- Prometheus metrics validation
- Valkey cache behavior
- MinIO storage operations

### Integration Tests
- Docker container validation
- Endpoint accessibility
- Version verification
- HTTP status code checks
- Temperature status field validation
- Metrics endpoint format validation

### Kubernetes Tests

- Deployment health checks
- Service connectivity
- Ingress routing
- Pod security context
- Resource limits enforcement
- Network policy validation

### End-to-End Tests

- 13 Venom test cases
- Full application flow testing
- Cache performance validation
- Infrastructure connectivity
- API documentation checks
- Error handling verification

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

### Phase 4 ✅
- [x] Kubernetes deployment
- [x] Kubernetes manifests (Deployment, Service, Ingress)
- [x] Prometheus metrics endpoint
- [x] Temperature status field
- [x] Integration tests
- [x] SonarQube analysis
- [x] Container registry publishing
- [x] CD pipeline for GHCR

### Phase 5 ✅

- [x] Valkey (Redis) caching layer
- [x] MinIO (S3) storage layer
- [x] /store endpoint
- [x] /readyz health check endpoint
- [x] /healthz liveness endpoint
- [x] Helm charts (dev, prod values)
- [x] Kustomize overlays (dev, stg, prod)
- [x] Prometheus + Grafana monitoring
- [x] Custom Prometheus metrics
- [x] ServiceMonitor for metrics scraping
- [x] End-to-End tests with Venom (13 tests)
- [x] Security scanning with Trivy
- [x] Kubesec for K8s best practices

### Phase 6 (Upcoming)

- [ ] ArgoCD GitOps deployment
- [ ] ExternalDNS for DNS management
- [ ] Cert-Manager for TLS certificates
- [ ] Dependabot for dependency updates
- [ ] Kyverno for Policy as Code
- [ ] Multi-cluster setup (Dev/Stage/Prod)

## Project Roadmap

### Completed Phases
- ✅ **Phase 1**: Kickoff & Preparation
- ✅ **Phase 2**: Basics - Code & Containers
- ✅ **Phase 3**: Start - Laying the Base
- ✅ **Phase 4**: Expand - Constructing a Shell

### Current Phase
- 🎯 Phase 6: Optimize - Improving

### Upcoming Phases
- **Phase 6**: Optimize - GitOps, Production Hardening
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
- Ensure ~100% test coverage
- Run linters before committing

## License

Educational project - open source for learning purposes.
