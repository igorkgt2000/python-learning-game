#!/bin/bash
# Python Learning Game - Startup Script

echo "🎮 Python Learning Game - Startup Check"
echo "========================================"

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo "❌ Error: main.py not found. Please run this from the game directory."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $PYTHON_VERSION"

# Check for Tkinter
echo "Checking Tkinter..."
if python -c "import tkinter" 2>/dev/null; then
    echo "✓ Tkinter is installed"
else
    echo "❌ Tkinter is NOT installed"
    echo ""
    echo "Please install Tkinter with:"
    echo "  sudo pacman -S tk"
    echo ""
    exit 1
fi

# Check for Pygame
echo "Checking Pygame..."
if python -c "import pygame" 2>/dev/null; then
    echo "✓ Pygame is installed"
else
    echo "❌ Pygame is NOT installed"
    echo ""
    echo "Please install dependencies with:"
    echo "  pip install -r requirements.txt"
    echo ""
    exit 1
fi

echo ""
echo "✅ All dependencies satisfied!"
echo ""
echo "Starting Python Learning Game..."
echo ""

# Run the game
python main.py

