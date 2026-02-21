#!/bin/bash

echo "========================================"
echo "  AI-NutriCurator Backend Server"
echo "========================================"
echo ""

echo "[1/2] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python is not installed or not in PATH"
    exit 1
fi
python3 --version
echo ""

echo "[2/2] Starting FastAPI server..."
echo "Server will run on http://localhost:8000"
echo "Press Ctrl+C to stop the server"
echo ""
echo "API Documentation: http://localhost:8000/docs"
echo ""

cd backend
python3 app.py
