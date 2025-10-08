#!/bin/bash

# Startup script for Product Facet Parser API

echo "Starting Product Facet Parser API..."
echo ""

# Check if Poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "❌ Poetry is not installed!"
    echo ""
    echo "Install Poetry with:"
    echo "  curl -sSL https://install.python-poetry.org | python3 -"
    echo ""
    echo "Or visit: https://python-poetry.org/docs/#installation"
    exit 1
fi

echo "✓ Poetry is installed"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo ""
    echo "Please create a .env file with your OPENAI_API_KEY"
    echo "You can copy env.example to .env and fill in your key:"
    echo "  cp env.example .env"
    echo ""
    exit 1
fi

echo "✓ .env file found"
echo ""

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

# Check if OpenAI API key is set
if [ -z "$OPENAI_API_KEY" ] || [ "$OPENAI_API_KEY" = "your-openai-api-key-here" ]; then
    echo "❌ OPENAI_API_KEY is not configured in .env file"
    echo ""
    echo "Please edit .env and add your OpenAI API key"
    exit 1
fi

echo "✓ OPENAI_API_KEY configured"
echo ""

# Check if dependencies are installed
if [ ! -d ".venv" ]; then
    echo "⚠️  Virtual environment not found. Installing dependencies..."
    poetry install
    echo ""
fi

# Start the API
echo "Starting FastAPI server on ${API_HOST:-0.0.0.0}:${API_PORT:-8000}..."
echo ""
echo "📡 API will be available at:"
echo "   - Swagger UI: http://localhost:${API_PORT:-8000}/docs"
echo "   - ReDoc: http://localhost:${API_PORT:-8000}/redoc"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

poetry run python api.py
