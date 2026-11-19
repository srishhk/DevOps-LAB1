#!/usr/bin/env bash
# Lab 1 deployment script: builds the Docker image, replaces the running
# container, and runs a smoke test against /health.
# Usage: ./deploy.sh [build_number]
set -euo pipefail

APP_NAME="lab1-flask-app"
BUILD="${1:-${BUILD_NUMBER:-local}}"
IMAGE="${APP_NAME}:${BUILD}"
PORT="${PORT:-5000}"

echo "==> Building image ${IMAGE}"
docker build --build-arg BUILD_NUMBER="${BUILD}" -t "${IMAGE}" -t "${APP_NAME}:latest" .

echo "==> Removing old container (if any)"
docker rm -f "${APP_NAME}" >/dev/null 2>&1 || true

echo "==> Starting new container on port ${PORT}"
docker run -d --name "${APP_NAME}" --restart unless-stopped -p "${PORT}:5000" "${IMAGE}"

echo "==> Smoke test"
for i in $(seq 1 10); do
  if curl -fs "http://localhost:${PORT}/health"; then
    echo
    echo "==> Deployment of build ${BUILD} succeeded"
    exit 0
  fi
  echo "   waiting for app (attempt ${i}/10)..."
  sleep 2
done

echo "==> Smoke test failed; container logs:"
docker logs "${APP_NAME}" || true
exit 1
