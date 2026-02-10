#!/bin/bash

echo "========================================"
echo "  AI-NutriCurator Frontend Server"
echo "========================================"
echo ""

echo "Starting Python HTTP server..."
echo "Frontend will run on http://localhost:3000"
echo "Press Ctrl+C to stop the server"
echo ""

python3 -m http.server 3000
