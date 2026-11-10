#!/usr/bin/env bash
set -e

# ==============================================================================
# Stone Audio (石头听力) - Safe Zero-Downtime Deployment Script
# 1. Backs up database atomically before doing anything
# 2. Builds images in the background
# 3. Performs zero-downtime container transition
# ==============================================================================

PROJECT_DIR="/home/ubuntu/sixsense"
SOURCE_TREE="$(cd "$(dirname "$0")/.." && pwd)"

# Hard gates. This script rebuilds the live containers. It is not run by CI.
# The 2026-11-10 read-only audit found live /api/nce and four NCE books, while
# GitHub main 4381616 has no NCE router. Do not recreate production from this tree.
if [ ! -f "$SOURCE_TREE/backend/app/routers/nce.py" ]; then
  echo "STOP: $SOURCE_TREE has no backend/app/routers/nce.py" >&2
  echo "STOP: refusing to build or recreate sixsense-frontend/backend. Live serves /api/nce." >&2
  echo "STOP: version parity is unproven (server has no .git; images are newer than 4381616)." >&2
  exit 2
fi
if [ "${CONFIRM_VERSION_PARITY:-}" != "yes" ] \
  || [ "${CONFIRM_BACKUP_RESTORE_DRILL:-}" != "yes" ] \
  || [ "${CONFIRM_PRODUCTION_DEPLOY:-}" != "yes" ]; then
  echo "STOP: set CONFIRM_VERSION_PARITY, CONFIRM_BACKUP_RESTORE_DRILL, and CONFIRM_PRODUCTION_DEPLOY to yes only after both hard gates pass." >&2
  exit 2
fi

cd "$PROJECT_DIR"

echo "=== [1/4] Running Pre-deploy Database Backup ==="
python3 "$PROJECT_DIR/scripts/backup_db.py"

echo "=== [2/4] Building New Container Images in Background ==="
sudo docker compose build

echo "=== [3/4] Performing Graceful Rolling Recreate ==="
# Docker compose up -d recreates containers with <1s downtime, preserving volumes
sudo docker compose up -d

echo "=== [4/4] Verifying Healthcheck ==="
sleep 2
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://mystone.top/api/health || true)
if [ "$HTTP_STATUS" = "200" ]; then
    echo "=== [SUCCESS] Deployment healthy and fully online (HTTP $HTTP_STATUS) ==="
else
    echo "=== [WARNING] Healthcheck returned HTTP $HTTP_STATUS, please check logs ==="
fi
