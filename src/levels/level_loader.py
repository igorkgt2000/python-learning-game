"""
Level loading and management system.
"""

import json
from pathlib import Path
from typing import List, Dict, Optional
from core.level import Level

class LevelLoader:
    """Handles loading and managing game levels."""
    
    def __init__(self, levels_dir: Path):
        """Initialize level loader with levels directory."""
        self.levels_dir = Path(levels_dir)
        self.levels_dir.mkdir(parents=True, exist_ok=True)
        self.levels: List[Level] = []
        self._load_all_levels()
    
    def _load_all_levels(self):
        """Load all available levels."""
        # Create some default levels if none exist
        if not any(self.levels_dir.glob("*.json")):
            self._create_default_levels()
        
        # Load all JSON level files
        for level_file in sorted(self.levels_dir.glob("*.json")):
            try:
                level = self._load_level_from_file(level_file)
                if level:
                    self.levels.append(level)
            except Exception as e:
                print(f"Error loading level {level_file}: {e}")
    
    def _load_level_from_file(self, file_path: Path) -> Optional[Level]:
        """Load a single level from JSON file."""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            return Level.from_dict(data)
        except Exception as e:
            print(f"Error loading level from {file_path}: {e}")
            return None
    
    def _create_default_levels(self):
        """Create default beginner levels."""
        default_levels = [
            {
                "name": "Level 1: First Steps",
                "start_pos": [0, 0],
                "goal_pos": [2, 0],
                "obstacles": [],
                "gems": [],
                "grid_size": 3,
                "hint": "Use move_forward() to reach the green goal!"
            },
            {
                "name": "Level 2: Turn Right",
                "start_pos": [0, 0],
                "goal_pos": [1, 1],
                "obstacles": [],
                "gems": [],
                "grid_size": 3,
                "hint": "Move forward, then turn right, then move forward again!"
            },
            {
                "name": "Level 3: Collect Gems",
                "start_pos": [0, 0],
                "goal_pos": [2, 2],
                "obstacles": [],
                "gems": [[1, 1]],
                "grid_size": 3,
                "hint": "Collect the yellow gem before reaching the goal!"
            },
            {
                "name": "Level 4: Simple Loop",
                "start_pos": [0, 0],
                "goal_pos": [4, 0],
                "obstacles": [],
                "gems": [],
                "grid_size": 5,
                "hint": "Use a for loop to move forward 4 times!"
            },
            {
                "name": "Level 5: Square Path",
                "start_pos": [0, 0],
                "goal_pos": [0, 0],
                "obstacles": [],
                "gems": [],
                "grid_size": 3,
                "hint": "Make a complete square: forward, right, forward, right, forward, right, forward, right!"
            }
        ]
        
        for i, level_data in enumerate(default_levels, 1):
            level_file = self.levels_dir / f"level_{i:02d}.json"
            with open(level_file, 'w') as f:
                json.dump(level_data, f, indent=2)
    
    def get_level(self, index: int) -> Optional[Level]:
        """Get level by index."""
        if 0 <= index < len(self.levels):
            return self.levels[index]
        return None
    
    def get_level_count(self) -> int:
        """Get total number of levels."""
        return len(self.levels)
    
    def get_level_names(self) -> List[str]:
        """Get list of all level names."""
        return [level.name for level in self.levels]
