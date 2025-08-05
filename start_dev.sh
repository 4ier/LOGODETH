#!/bin/bash

# LOGODETH Development Startup Script

echo "🤘 Starting LOGODETH Development Environment..."

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  Creating .env file from template..."
    cp .env.example .env
    echo "📝 Please edit .env file with your API keys before continuing."
    echo "   Especially: OPENAI_API_KEY=your_actual_key_here"
    exit 1
fi

# Check if Redis is running
echo "🔍 Checking Redis connection..."
if ! redis-cli ping > /dev/null 2>&1; then
    echo "❌ Redis is not running. Starting with Docker..."
    if command -v docker-compose > /dev/null; then
        docker-compose up -d redis
        echo "✅ Redis started with Docker Compose"
    else
        echo "❌ Please start Redis manually: redis-server"
        exit 1
    fi
else
    echo "✅ Redis is running"
fi

# Create logs directory
mkdir -p logs

# Install dependencies if needed
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

echo "📦 Activating virtual environment..."
source venv/bin/activate

echo "📦 Installing dependencies..."
pip install -r requirements_multimodal.txt > /dev/null 2>&1

# Test API connection
echo "🧪 Testing API server connection..."
python test_api.py

echo ""
echo "🚀 Starting LOGODETH API server..."
echo "   Backend: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo "   Frontend: Open index.html in your browser"
echo ""

# Start the API server
python run.py