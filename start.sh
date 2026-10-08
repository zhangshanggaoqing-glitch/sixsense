#!/usr/bin/env bash
# SixSense Production Start Script

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$BASE_DIR"
export PYTHONPATH="$BASE_DIR"

echo "=== Starting SixSense Services ==="

# 1. Start Backend FastAPI
if lsof -i :8000 >/dev/null 2>&1; then
    echo "Backend already running on port 8000."
else
    echo "Starting backend on http://localhost:8000..."
    nohup python3 -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 > "$BASE_DIR/backend.log" 2>&1 &
    BACKEND_PID=$!
    echo $BACKEND_PID > "$BASE_DIR/.backend.pid"
    disown $BACKEND_PID
fi

# 2. Start Frontend Next.js
if lsof -i :3000 >/dev/null 2>&1; then
    echo "Frontend already running on port 3000."
else
    echo "Starting frontend on http://localhost:3000..."
    cd "$BASE_DIR/frontend"
    nohup npm run start -- -p 3000 > "$BASE_DIR/frontend.log" 2>&1 &
    FRONTEND_PID=$!
    echo $FRONTEND_PID > "$BASE_DIR/.frontend.pid"
    disown $FRONTEND_PID
    cd "$BASE_DIR"
fi

# Wait up to 5 seconds for health
echo "Waiting for services to become ready..."
for i in {1..10}; do
    if curl -s http://127.0.0.1:8000/api/health >/dev/null 2>&1 && curl -s http://127.0.0.1:3000 >/dev/null 2>&1; then
        break
    fi
    sleep 0.5
done

echo "=== Services Status ==="
echo "Frontend: http://localhost:3000"
echo "Backend:  http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo "Logs: backend.log, frontend.log"

