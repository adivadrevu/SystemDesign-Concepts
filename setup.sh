#!/bin/bash

# System Design Concepts - Setup and Run Script

echo "🚀 System Design Concepts - Environment Setup"
echo "=============================================="

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed. Please install it first:"
    echo "   curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Setup virtual environment
echo "📦 Setting up virtual environment..."
uv sync --dev

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

echo ""
echo "✅ Environment ready! You can now run any chapter:"
echo ""
echo "📚 Available Chapters:"
echo "   Chapter 1 - Load Balancer:"
echo "     cd Chapter-01-Load-Balancer && python load_balancer.py"
echo ""
echo "   Chapter 2 - Cache:"
echo "     cd Chapter-02-Cache && python simple_cache.py"
echo "     cd Chapter-02-Cache && uvicorn cache:app --reload"
echo ""
echo "   Chapter 4 - Rate Limiting:"
echo "     cd Chapter-04-Rate-Limiting/Token-Bucket && python test_simple.py"
echo "     cd Chapter-04-Rate-Limiting/Token-Bucket && python demo.py"
echo ""
echo "🔧 Environment Management:"
echo "   Activate: source .venv/bin/activate"
echo "   Deactivate: deactivate"
echo "   Update deps: uv sync --dev"
echo "   List packages: uv pip list"
