#!/usr/bin/env bash
# SixSense Stop Script

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$BASE_DIR"

echo "=== Stopping SixSense Services ==="

if [ -f "$BASE_DIR/.backend.pid" ]; then
    kill "$(cat "$BASE_DIR/.backend.pid")" 2>/dev/null
    rm -f "$BASE_DIR/.backend.pid"
    echo "Backend stopped."
fi

if [ -f "$BASE_DIR/.frontend.pid" ]; then
    kill "$(cat "$BASE_DIR/.frontend.pid")" 2>/dev/null
    rm -f "$BASE_DIR/.frontend.pid"
    echo "Frontend stopped."
fi

# Fallback port killers
fuser -k 8000/tcp 2>/dev/null
fuser -k 3000/tcp 2>/dev/null

echo "All services stopped."
