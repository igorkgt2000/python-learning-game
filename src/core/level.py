"""
Level System - Defines individual game levels with objectives and layout.

This module contains the Level class which represents a single playable level.
Each level defines the grid layout, starting position, obstacles, collectibles,
and victory conditions. Levels can be loaded from JSON files or created procedurally.

Architecture:
    - Level owns a Grid instance with the level's layout
    - Level defines victory conditions (reach goal + collect all gems)
    - Levels are loaded by LevelLoader from JSON files
    - Each level has a hint to guide the player

Level Data Structure:
    {
        "name": "Level 1: First Steps",
        "start_pos": [0, 0],
        "goal_pos": [9, 9],
        "obstacles": [[5, 5], [5, 6], ...],  # Wall positions
        "gems": [[3, 3], [7, 7]],            # Gem positions
        "grid_size": 10,                     # 10x10 grid
        "hint": "Use move_forward() to reach the goal!"
    }

Usage Example:
    >>> level = Level(start_pos=(0, 0), goal_pos=(5, 5),
    ...               obstacles=[], gems=[(2, 2)],
    ...               grid_size=6, hint="Collect the gem!")
    >>> level.is_completed(player, grid)
    False
    >>> level.get_total_gems()
    1

Author: Python Learning Game Team
Version: 2.0
Last Modified: October 2, 2025
"""

from typing import List, Tuple, Optional
from .grid import Grid, TileType
from .player import Player

class Level:
    """
    Represents a single playable game level.
    
    A Level defines:
        - Grid size and layout (obstacles, gems, goal)
        - Starting position and direction for player
        - Victory conditions (reach goal + collect all gems)
        - Hint text to help players
        - Optimal solution metrics (for star ratings)
    
    Attributes:
        start_pos (Tuple[int, int]): Player starting position (x, y)
        goal_pos (Tuple[int, int]): Goal tile position (x, y)
        obstacles (List[Tuple[int, int]]): Positions of wall tiles
        gems (List[Tuple[int, int]]): Positions of collectible gems
        grid_size (int): Size of square grid (grid_size × grid_size)
        hint (str): Hint text displayed to player
        name (str): Level name/title
        grid (Grid): The actual grid instance for this level
    
    Victory Conditions:
        1. Player must reach goal_pos
        2. Player must collect all gems
        (Both conditions must be met)
    
    Example:
        >>> level = Level((0, 0), (9, 9), [], [], 10, "Move forward!")
        >>> level.grid_size
        10
        >>> level.get_total_gems()
        0
    """
    
    def __init__(self, start_pos: Tuple[int, int], goal_pos: Tuple[int, int], 
                 obstacles: List[Tuple[int, int]], gems: List[Tuple[int, int]], 
                 grid_size: int, hint: str = "", name: str = ""):
        """
        Initialize a new level with layout and objectives.
        
        Creates the level grid and populates it with obstacles, gems, and goal.
        The grid is automatically set up by calling _setup_level().
        
        Args:
            start_pos (Tuple[int, int]): Starting (x, y) position for player
            goal_pos (Tuple[int, int]): Goal tile (x, y) position
            obstacles (List[Tuple[int, int]]): List of wall positions
            gems (List[Tuple[int, int]]): List of gem positions
            grid_size (int): Size of square grid (typically 5-20)
            hint (str): Optional hint text for the player
            name (str): Optional level name (auto-generated if empty)
        
        Note:
            Positions outside grid bounds are silently ignored during setup.
            This allows levels to be designed without strict validation.
        
        Example:
            >>> level = Level(
            ...     start_pos=(0, 0),
            ...     goal_pos=(5, 5),
            ...     obstacles=[(2, 2), (3, 2)],
            ...     gems=[(1, 1)],
            ...     grid_size=6,
            ...     hint="Navigate around the walls"
            ... )
        """
        # Store level configuration
        self.start_pos = start_pos  # Where player begins
        self.goal_pos = goal_pos    # Where player must reach
        self.obstacles = obstacles  # List of wall positions
        self.gems = gems           # List of gem positions
        self.grid_size = grid_size # Grid dimensions (N×N)
        self.hint = hint           # Hint text for player
        
        # Generate level name if not provided
        self.name = name or f"Level {grid_size}x{grid_size}"
        
        # Create the grid instance for this level
        # Grid size is always square (grid_size × grid_size)
        self.grid = Grid(grid_size, grid_size)
        
        # Populate grid with obstacles, gems, and goal
        self._setup_level()
    
    def _setup_level(self):
        """
        Internal method to populate the grid with level elements.
        
        Called automatically during __init__. Places all obstacles, gems,
        and the goal tile onto the grid. Positions outside grid bounds
        are silently skipped.
        
        Setup Order:
            1. Place obstacles (walls)
            2. Place gems
            3. Place goal
        
        Side Effects:
            - Modifies self.grid by setting tiles
            - Updates grid's special tracking lists (gems, goals)
        
        Note:
            This is a private method (indicated by leading underscore).
            It should only be called once during level initialization.
        """
        # Place obstacles (walls) first
        # Walls block player movement
        for x, y in self.obstacles:
            # Validate position is within grid bounds
            if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
                self.grid.set_tile(x, y, TileType.WALL)
        
        # Place gems second
        # Gems must be collected for level completion
        for x, y in self.gems:
            # Validate position is within grid bounds
            if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
                self.grid.set_tile(x, y, TileType.GEM)
        
        # Place goal last
        # Player must reach this tile to complete level
        if 0 <= self.goal_pos[0] < self.grid_size and 0 <= self.goal_pos[1] < self.grid_size:
            self.grid.set_tile(self.goal_pos[0], self.goal_pos[1], TileType.GOAL)
    
    def is_completed(self, player: Player, grid: Grid) -> bool:
        """
        Check if the player has completed this level.
        
        Victory requires TWO conditions:
            1. Player must be standing on the goal tile
            2. Player must have collected ALL gems
        
        Args:
            player (Player): The player instance to check
            grid (Grid): The current game grid (should match self.grid)
        
        Returns:
            bool: True if level is complete, False otherwise
        
        Example:
            >>> level = Level((0, 0), (5, 5), [], [(2, 2)], 6)
            >>> player = Player(5, 5, "north")
            >>> level.is_completed(player, grid)  # Player at goal but no gem
            False
            >>> player.collect_gem((2, 2))
            >>> level.is_completed(player, grid)  # Has gem and at goal
            True
        """
        # Condition 1: Player must be at goal position
        if player.get_position() != self.goal_pos:
            return False  # Not at goal yet
        
        # Condition 2: Player must have collected all gems
        # Compare number of gems collected vs. number in level
        if len(player.get_collected_gems()) < len(self.gems):
            return False  # Haven't collected all gems yet
        
        # Both conditions met - level complete!
        return True
    
    def get_total_gems(self) -> int:
        """
        Get the total number of gems in this level.
        
        This is the number of gems that must be collected for completion.
        
        Returns:
            int: Total gem count
        
        Example:
            >>> level = Level((0, 0), (5, 5), [], [(1, 1), (2, 2)], 6)
            >>> level.get_total_gems()
            2
        """
        return len(self.gems)
    
    def get_remaining_gems(self, player: Player) -> int:
        """
        Calculate how many gems the player still needs to collect.
        
        Args:
            player (Player): The player to check
        
        Returns:
            int: Number of gems not yet collected
        
        Example:
            >>> level = Level((0, 0), (5, 5), [], [(1, 1), (2, 2)], 6)
            >>> player = Player(0, 0, "north")
            >>> level.get_remaining_gems(player)
            2
            >>> player.collect_gem((1, 1))
            >>> level.get_remaining_gems(player)
            1
        """
        # Total gems minus collected gems
        return len(self.gems) - len(player.get_collected_gems())
    
    def is_valid_start_position(self, x: int, y: int) -> bool:
        """
        Check if a position is valid for starting the player.
        
        A valid start position must be:
            - Within grid bounds
            - On an EMPTY tile (not wall, gem, or goal)
        
        Args:
            x (int): X coordinate to check
            y (int): Y coordinate to check
        
        Returns:
            bool: True if valid start position, False otherwise
        
        Note:
            Currently level design typically uses fixed start_pos,
            but this method allows validation if start position changes.
        
        Example:
            >>> level = Level((0, 0), (5, 5), [(2, 2)], [], 6)
            >>> level.is_valid_start_position(0, 0)
            True
            >>> level.is_valid_start_position(2, 2)  # Wall
            False
        """
        # Check bounds first
        if not (0 <= x < self.grid_size and 0 <= y < self.grid_size):
            return False  # Out of bounds
        
        # Can't start on obstacle, gem, or goal
        # Must be an empty tile
        tile_type = self.grid.get_tile(x, y)
        return tile_type == TileType.EMPTY
    
    def get_hint(self) -> str:
        """
        Get the hint text for this level.
        
        Hints are displayed to help players understand what they need to do.
        They typically suggest which Python concepts to use.
        
        Returns:
            str: Hint text (may be empty string)
        
        Example:
            >>> level = Level((0, 0), (5, 5), [], [], 6,
            ...               hint="Use move_forward() 5 times")
            >>> level.get_hint()
            'Use move_forward() 5 times'
        """
        return self.hint
    
    def to_dict(self) -> dict:
        """
        Convert level to dictionary for JSON serialization.
        
        This allows levels to be saved to JSON files for persistence
        and sharing. The format matches the structure used by level files.
        
        Returns:
            dict: Dictionary with all level data
        
        Example:
            >>> level = Level((0, 0), (5, 5), [], [], 6, "Go forward!")
            >>> level.to_dict()
            {
                'name': 'Level 6x6',
                'start_pos': (0, 0),
                'goal_pos': (5, 5),
                'obstacles': [],
                'gems': [],
                'grid_size': 6,
                'hint': 'Go forward!'
            }
        """
        return {
            "name": self.name,
            "start_pos": self.start_pos,
            "goal_pos": self.goal_pos,
            "obstacles": self.obstacles,
            "gems": self.gems,
            "grid_size": self.grid_size,
            "hint": self.hint
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Level':
        """
        Create a Level instance from a dictionary (JSON data).
        
        This is a class method that acts as an alternative constructor.
        It's used by the level loader to create Level objects from JSON files.
        
        Args:
            data (dict): Dictionary containing level data (from JSON)
        
        Returns:
            Level: New Level instance created from the data
        
        Note:
            hint and name are optional fields with empty string defaults.
        
        Example:
            >>> data = {
            ...     "start_pos": [0, 0],
            ...     "goal_pos": [5, 5],
            ...     "obstacles": [[2, 2]],
            ...     "gems": [],
            ...     "grid_size": 6,
            ...     "hint": "Navigate the obstacle"
            ... }
            >>> level = Level.from_dict(data)
            >>> level.grid_size
            6
        """
        return cls(
            start_pos=tuple(data["start_pos"]),  # Convert list to tuple
            goal_pos=tuple(data["goal_pos"]),    # Convert list to tuple
            obstacles=[tuple(pos) for pos in data["obstacles"]],  # Convert lists to tuples
            gems=[tuple(pos) for pos in data["gems"]],            # Convert lists to tuples
            grid_size=data["grid_size"],
            hint=data.get("hint", ""),  # Optional field with default
            name=data.get("name", "")   # Optional field with default
        )
