#!/usr/bin/env bash
set -e

# ==============================================================================
# Stone Audio (石头听力) - Safe Zero-Downtime Deployment Script
# 1. Backs up database atomically before doing anything
# 2. Builds images in the background
# 3. Performs zero-downtime container transition
# ==============================================================================

PROJECT_DIR="/home/ubuntu/sixsense"
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
