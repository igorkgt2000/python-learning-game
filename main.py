#!/usr/bin/env python3
"""
Python Learning Game - Main Entry Point
A comprehensive Python learning game with progressive levels from beginner to expert.
"""

import sys
import os
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from ui.main_window import MainWindow

def main():
    """Main entry point for the Python Learning Game."""
    try:
        # Create and run the main window
        app = MainWindow()
        app.run()
        
    except KeyboardInterrupt:
        print("\nGame interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
