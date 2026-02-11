#!/bin/bash
set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}================================${NC}"
echo -e "${YELLOW}HiveBox E2E Tests with Venom${NC}"
echo -e "${YELLOW}================================${NC}"
echo ""

if ! command -v venom &> /dev/null; then
    echo -e "${YELLOW}Venom not found. Installing...${NC}"
    
    OS=$(uname -s | tr '[:upper:]' '[:lower:]')
    ARCH=$(uname -m)
    
    if [ "$ARCH" = "x86_64" ]; then
        ARCH="amd64"
    elif [ "$ARCH" = "aarch64" ] || [ "$ARCH" = "arm64" ]; then
        ARCH="arm64"
    fi
    
    VENOM_VERSION="v1.2.0"
    VENOM_URL="https://github.com/ovh/venom/releases/download/${VENOM_VERSION}/venom.${OS}-${ARCH}"
    
    curl -L "$VENOM_URL" -o /tmp/venom
    chmod +x /tmp/venom
    sudo mv /tmp/venom /usr/local/bin/venom
    
    echo -e "${GREEN}Venom installed${NC}"
fi

venom version
echo ""

if ! minikube status &> /dev/null; then
    echo -e "${RED}Minikube is not running!${NC}"
    echo "Start it with: minikube start"
    exit 1
fi

if ! kubectl get deployment hivebox -n hivebox &> /dev/null; then
    echo -e "${RED}HiveBox is not deployed!${NC}"
    echo "Deploy it with: kubectl apply -k k8s/overlays/dev/"
    exit 1
fi

echo -e "${YELLOW}Waiting for HiveBox to be ready...${NC}"
kubectl wait --for=condition=available --timeout=120s deployment/hivebox -n hivebox

echo -e "${YELLOW}Setting up port forward...${NC}"
kubectl port-forward -n hivebox svc/hivebox 8000:8000 &
PF_PID=$!

sleep 3

cleanup() {
    echo ""
    echo -e "${YELLOW}Cleaning up...${NC}"
    kill $PF_PID 2>/dev/null || true
}
trap cleanup EXIT

echo -e "${YELLOW}Testing connection...${NC}"
if ! curl -sf http://localhost:8000/healthz > /dev/null; then
    echo -e "${RED}Cannot connect to HiveBox!${NC}"
    exit 1
fi
echo -e "${GREEN}Connection OK${NC}"
echo ""

echo -e "${YELLOW}Running E2E tests...${NC}"
echo ""

cd tests/e2e

venom run \
    --var="base_url=http://localhost:8000" \
    --format=xml \
    --output-dir=./reports \
    hivebox.yaml

VENOM_EXIT_CODE=$?

cd ../..

echo ""
if [ $VENOM_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}================================${NC}"
    echo -e "${GREEN}  All E2E tests passed!${NC}"
    echo -e "${GREEN}================================${NC}"
else
    echo -e "${RED}================================${NC}"
    echo -e "${RED}  Some E2E tests failed${NC}"
    echo -e "${RED}================================${NC}"
    exit 1
fi

echo ""
echo "Test reports available in: tests/e2e/reports/"