#!/bin/bash
# Quick Start Guide for Multi-Tenant Notes API

echo "🚀 Multi-Tenant Notes API - Quick Start Guide"
echo "================================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

echo "📦 Installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt
echo "✅ Dependencies installed"
echo ""

echo "🗄️  MongoDB Setup Required"
echo "=========================="
echo "You need MongoDB running. Choose one option:"
echo ""
echo "Option 1: Use Docker (if available)"
echo "  docker run -d -p 27017:27017 --name mongodb \\"
echo "    -e MONGO_INITDB_ROOT_USERNAME=admin \\"
echo "    -e MONGO_INITDB_ROOT_PASSWORD=password \\"
echo "    mongo:7.0"
echo ""
echo "Option 2: Use Docker Compose"
echo "  docker compose up -d mongodb"
echo ""
echo "Option 3: Install MongoDB locally"
echo "  Follow: https://www.mongodb.com/docs/manual/installation/"
echo ""
echo "Option 4: Use MongoDB Atlas (cloud)"
echo "  1. Create free cluster at https://www.mongodb.com/cloud/atlas"
echo "  2. Update MONGODB_URL in .env file"
echo ""

read -p "Press Enter once MongoDB is running..."
echo ""

echo "🚀 Starting FastAPI Application..."
echo "==================================="
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

