"""
Configuration Settings - Central configuration for all game systems.

This module contains the Config class which stores all game settings in one place.
Using a dataclass makes it easy to create, modify, and pass configuration throughout
the application. All systems (rendering, gameplay, code execution) reference this.

Design Pattern:
    Configuration Object - Single source of truth for all settings
    
Architecture:
    - Config is instantiated once at game startup
    - Passed to all subsystems that need settings
    - Can be modified at runtime (e.g., for settings menu)
    - Uses dataclass for clean syntax and default values

Usage Example:
    >>> config = Config()
    >>> config.WINDOW_WIDTH
    1200
    >>> config.TILE_SIZE = 64  # Modify for larger sprites
    >>> print(config.ASSETS_DIR)
    /path/to/project/assets

Author: Python Learning Game Team
Version: 2.0
Last Modified: October 2, 2025
"""

import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import Tuple, List

@dataclass
class Config:
    """
    Global configuration settings for the entire game.
    
    This dataclass holds all configurable values used throughout the game.
    Settings are organized by category (window, gameplay, colors, paths, security).
    
    Using a dataclass provides:
        - Type hints for all settings
        - Default values
        - Automatic __init__ and __repr__
        - Field-level customization with field()
    
    Categories:
        - Window: Display size and title
        - Game: Grid size, tile size, animation timing
        - Colors: RGB values for all game elements (fallback if sprites missing)
        - File Paths: Asset, level, and data directories
        - Database: Storage for achievements and progress
        - Security: Code execution limits and restrictions
    
    Note:
        All paths are absolute and computed relative to this file's location.
        This ensures the game works regardless of where it's run from.
    
    Example:
        >>> config = Config()
        >>> config.GRID_SIZE = 15  # Larger grid
        >>> config.ANIMATION_SPEED = 0.3  # Faster animations
    """
    
    # ==================== WINDOW SETTINGS ====================
    # These control the Pygame display window
    
    WINDOW_WIDTH: int = 1200  # Window width in pixels (was 800, increased for split-screen UI)
    WINDOW_HEIGHT: int = 800  # Window height in pixels (standard HD)
    WINDOW_TITLE: str = "Python Learning Game"  # Title bar text
    
    # ==================== GAME SETTINGS ====================
    # Core gameplay parameters
    
    GRID_SIZE: int = 10  # Default grid size (10x10 tiles)
                        # Individual levels can override this
                        # Typical range: 5-20 tiles
    
    TILE_SIZE: int = 40  # Size of each grid tile in pixels
                        # Sprite images are scaled to this size
                        # Larger = more detailed but fewer tiles visible
                        # Typical values: 32 (small), 40 (medium), 64 (large)
    
    ANIMATION_SPEED: float = 0.5  # Duration of each action animation in seconds
                                  # Lower = faster (0.2-0.3 for quick)
                                  # Higher = slower (0.5-1.0 for educational)
                                  # This affects move_forward(), turn_left(), etc.
    
    # ==================== COLORS (RGB TUPLES) ====================
    # Fallback colors if pixel art sprites are missing or for UI elements
    # Format: (Red, Green, Blue) each 0-255
    
    BACKGROUND_COLOR: Tuple[int, int, int] = (240, 240, 240)  # Light gray (almost white)
    GRID_COLOR: Tuple[int, int, int] = (200, 200, 200)        # Medium gray for grid lines
    PLAYER_COLOR: Tuple[int, int, int] = (0, 100, 200)        # Blue (robot theme)
    WALL_COLOR: Tuple[int, int, int] = (100, 100, 100)        # Dark gray for walls
    GEM_COLOR: Tuple[int, int, int] = (255, 215, 0)           # Gold color
    GOAL_COLOR: Tuple[int, int, int] = (0, 200, 0)            # Bright green
    
    # ==================== FILE PATHS ====================
    # All paths computed relative to project structure for portability
    # Using Path() for cross-platform compatibility (Windows/Mac/Linux)
    
    # Project structure:
    # python_learning_game/
    # ├── src/core/config.py  <-- This file
    # ├── assets/             <-- Sprites, sounds, music
    # ├── src/levels/         <-- Level JSON files
    # └── src/data/           <-- Saved games, achievements
    
    ASSETS_DIR: Path = Path(__file__).parent.parent.parent / "assets"  # Up 3 levels to project root, then into assets
    LEVELS_DIR: Path = Path(__file__).parent.parent / "levels"         # Up 2 levels to src/, then into levels
    DATA_DIR: Path = Path(__file__).parent.parent / "data"             # Up 2 levels to src/, then into data
    
    # ==================== DATABASE SETTINGS ====================
    # SQLite database for persistent storage
    
    DATABASE_PATH: str = "game_data.db"  # Relative path in current directory
                                         # Stores: achievements, level progress, statistics
                                         # TODO: Move to DATA_DIR for better organization
    
    # ==================== CODE EXECUTION SECURITY ====================
    # Critical security settings for running user-submitted Python code
    
    MAX_EXECUTION_TIME: float = 5.0  # Maximum seconds before timing out user code
                                     # Prevents infinite loops from freezing the game
                                     # 5 seconds is generous for educational purposes
                                     # Actual well-optimized solutions take < 1 second
    
    ALLOWED_IMPORTS: List[str] = field(default_factory=list)  # List of allowed import statements
                                                               # Empty by default = NO IMPORTS ALLOWED
                                                               # This is critical for security
                                                               # Users can't import os, sys, etc.
                                                               # field(default_factory=list) needed for mutable defaults
    
    def __post_init__(self):
        """
        Post-initialization hook called after dataclass __init__.
        
        This method runs automatically after the Config object is created.
        We use it to ensure all necessary directories exist before the
        game tries to load assets or save data.
        
        Creates:
            - ASSETS_DIR if it doesn't exist (for sprites, sounds)
            - LEVELS_DIR if it doesn't exist (for level JSON files)
            - DATA_DIR if it doesn't exist (for saves, achievements)
        
        Args:
            None (called automatically by dataclass)
        
        Side Effects:
            - Creates directories on filesystem
            - Uses parents=True to create intermediate dirs if needed
            - Uses exist_ok=True to avoid errors if dirs already exist
        
        Note:
            This is safe to call multiple times - it won't overwrite existing files.
        """
        # Create asset directory if it doesn't exist
        # parents=True: create parent directories if needed
        # exist_ok=True: don't raise error if directory already exists
        self.ASSETS_DIR.mkdir(parents=True, exist_ok=True)
        
        # Create levels directory for JSON level files
        self.LEVELS_DIR.mkdir(parents=True, exist_ok=True)
        
        # Create data directory for user progress and achievements
        self.DATA_DIR.mkdir(parents=True, exist_ok=True)
