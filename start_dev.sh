#!/bin/bash

# Function to kill all background processes on exit
cleanup() {
    echo "Stopping all services..."
    kill $(jobs -p) 2>/dev/null
    exit
}

# Trap SIGINT (Ctrl+C) and call cleanup
trap cleanup SIGINT

echo "🚀 Starting MemeMind Development Environment..."

# 1. Start Backend API
echo "Starting Backend API (Port 8080)..."
lsof -t -i:8080 | xargs kill -9 2>/dev/null || true
cd services/api
uvicorn app.main:app --host 0.0.0.0 --port 8080 &
BACKEND_PID=$!
cd ../..

# 2. Start Backend Worker
echo "Starting Backend Worker..."
pkill -f "python3 -m app.worker" || true
cd services/api
python3 -m app.worker &
WORKER_PID=$!
cd ../..

# Wait a moment for backend to initialize
sleep 3

# 3. Start Mobile App
echo "Starting Mobile App (Expo)..."
cd app-mobile
npx expo start -c
